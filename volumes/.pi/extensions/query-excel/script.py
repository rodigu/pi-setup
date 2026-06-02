#!/usr/bin/env python3
"""Query Excel files with SQL using Polars."""

import argparse
import json
import os
import sys

import polars as pl


def normalize_sheet_name(name: str) -> str:
    """Convert sheet name to valid SQL table name.

    Replaces spaces and hyphens with underscores so the name can be
    used as a Polars SQL table identifier.

    Args:
        name: Original Excel sheet name.

    Returns:
        Normalized name safe for use in SQL queries.
    """
    return name.replace(" ", "_").replace("-", "_")


def build_table_map(dfs: dict[str, pl.DataFrame]) -> dict[str, pl.DataFrame]:
    """Build a mapping of normalized sheet names to DataFrames.

    Disambiguates collisions by appending _2, _3, etc. when multiple
    sheets normalize to the same name.

    Args:
        dfs: Mapping of original sheet names to DataFrames.

    Returns:
        Mapping of unique normalized table names to DataFrames.
    """
    table_map: dict[str, pl.DataFrame] = {}
    seen_counts: dict[str, int] = {}

    for sheet_name, df in dfs.items():
        base = normalize_sheet_name(sheet_name)

        if base in seen_counts:
            seen_counts[base] += 1
            table_name = f"{base}_{seen_counts[base]}"
        else:
            seen_counts[base] = 1
            table_name = base

        table_map[table_name] = df

    return table_map


def add_sheets_meta_table(table_map: dict[str, pl.DataFrame]) -> dict[str, pl.DataFrame]:
    """Add a meta table listing available sheet names.

    Args:
        table_map: Mapping of table names to DataFrames (mutated in place).

    Returns:
        The same table_map with the added _AVAILABLE_SHEETS entry.
    """
    table_map["_AVAILABLE_SHEETS"] = pl.DataFrame({
        "Sheets_Name": list(table_map.keys())
    })
    return table_map


def validate_path(filepath: str) -> tuple[bool, str]:
    """Validate file path for safety.

    Checks that the path does not contain traversal sequences and
    resolves to an actual file on disk.

    Args:
        filepath: Path string to validate.

    Returns:
        A tuple of (is_valid, resolved_path_or_error). When valid, the
        second element is the resolved absolute path. When invalid, it
        is an error message string.
    """
    # Reject path traversal
    if ".." in filepath:
        return False, "Path traversal not allowed (..)"

    # Resolve to absolute path
    resolved = os.path.realpath(filepath)

    # Must be a real file
    if not os.path.isfile(resolved):
        return False, f"Not a file: {filepath}"

    return True, resolved


def check_file_size(filepath: str, max_bytes: int = 50 * 1024 * 1024) -> tuple[bool, str]:
    """Check that file size is under the allowed limit.

    Args:
        filepath: Absolute path to the file.
        max_bytes: Maximum allowed size in bytes. Defaults to 50 MB.

    Returns:
        A tuple of (is_valid, error_message). When valid, the error
        message is an empty string.
    """
    size = os.path.getsize(filepath)
    if size > max_bytes:
        return False, f"File too large: {size / 1024 / 1024:.1f}MB (max 50MB)"
    return True, ""


def main():
    """Entry point for the query_excel CLI.

    Parses command-line arguments, validates the file, reads all sheets
    into Polars DataFrames, executes the SQL query, applies output
    restrictions (max 5 rows, max 5 columns), and prints the result
    as JSON to stdout.

    Exit Codes:
        0: Success.
        1: Validation or query error.
    """
    parser = argparse.ArgumentParser(description="Query Excel files with SQL")
    parser.add_argument("--filepath", required=True, help="Path to Excel file")
    parser.add_argument("--query", required=True, help="SQL query to execute")
    args = parser.parse_args()

    # Validate path
    valid, result = validate_path(args.filepath)
    if not valid:
        print(json.dumps({"error": result}))
        sys.exit(1)

    filepath = result

    # Check file size
    valid, error = check_file_size(filepath)
    if not valid:
        print(json.dumps({"error": error}))
        sys.exit(1)

    # Read all sheets
    try:
        dfs = pl.read_excel(filepath, sheet_id=0)
    except Exception as e:
        print(json.dumps({"error": f"Failed to read Excel: {str(e)[:200]}"}))
        sys.exit(1)

    # Check total row count
    total_rows = sum(df.shape[0] for df in dfs.values())
    if total_rows > 1_000_000:
        print(json.dumps({
            "error": f"Too many rows: {total_rows:,} (max 1M). Filter or specify sheets."
        }))
        sys.exit(1)

    # Normalize sheet names and load into SQL context
    table_map = build_table_map(dfs)
    add_sheets_meta_table(table_map)

    ctx = pl.SQLContext(**table_map)

    # Execute query
    try:
        result = ctx.execute(args.query).collect()
    except Exception as e:
        print(json.dumps({"error": f"Query error: {str(e)[:200]}"}))
        sys.exit(1)

    # Apply restrictions
    warnings = []

    # Limit columns to 5
    if result.shape[1] > 5:
        dropped = result.columns[5:]
        result = result.select(result.columns[:5])
        warnings.append(f"Dropped columns: {', '.join(dropped)}")

    # Sample 5 rows
    if result.shape[0] > 5:
        original_rows = result.shape[0]
        result = result.sample(5)
        warnings.append(f"Sampled 5 of {original_rows} rows")

    # Convert to output
    output = {
        "data": result.to_dicts(),
        "columns": result.columns,
        "row_count": result.shape[0],
    }

    if warnings:
        output["warnings"] = warnings

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
