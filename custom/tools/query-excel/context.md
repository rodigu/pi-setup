# Implementation Context

## Dependencies

- Python: `polars` with `fastexcel` engine (pre-installed in Docker image)
- The python script must be self-contained; assume no pre-installed packages beyond standard lib

## Python Script

The script receives `--filepath` and `--query` args, performs safeguards checks, then:

1. Check file size (reject > 50MB)
2. Validate path (no `../`, must be a real file)
3. Read all sheets with `pl.read_excel(filepath, sheet_id=0)`
4. Check total row count (reject > 1M)
5. Normalize sheet names for SQL table names (spaces/hyphens → underscores)
6. Execute query via `pl.SQLContext`
7. Apply restrictions: `.sample(5)`, limit to 5 columns
8. Output JSON to stdout (result or error)

Exit codes: 0 for success, 1 for errors. All output on stdout as JSON.

## File Structure

```
.pi/extensions/query-excel/
├── index.ts      # TypeScript extension (registers tool, spawns Python)
└── script.py     # Python script (reads Excel, executes SQL)
```

## TypeScript Integration

The tool is registered as a pi extension using `pi.registerTool()`. See:
- `docs/extensions.md` for the full API
- `examples/extensions/dynamic-tools.ts` for a working example

Parameters schema defines `filepath` (string, required) and `query` (string, required).

## Subprocess Invocation

The Python script is spawned via `child_process.spawn` from `index.ts`. It receives `--filepath` and `--query` args. Stdout contains the JSON result. The 30-second timeout is enforced from the TypeScript side — do not rely on Python to kill itself.
