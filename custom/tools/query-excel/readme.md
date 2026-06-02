# query excel tool

Name: `query_excel`
Description: tool for quering excel with SQL

Used for quick and easy excel file data analysis.

## `pi.registerTool()`

These are suggestions and may be expanded upon further.
Look at the fields for other tools for reference.

- `description`: query excel files with SQL
- `promptSnippet`: query excel files with SQL
- `promptGuidelines`:
  - provide `filepath` and `query`
  - `query` should be in Polars SQL
  - always use it in place of read or bash, as excel files are binary and not well suited to those tools
  - dataframes are named after sheets:
    - excel files with multiple sheets are read into tables with formatted names (e.g. `Sheet_0` for `Sheet 0` and so on)
  - tool returns a sample of 5 rows
  - tool returns at most 5 columns at a time
  - use agregates (groupings) or filters to get exactly what you need
    - use where filters
    - use sums and averages

## input

`filepath`: File name with full absolute path.
`query`: A SQL query.

## output

The result of the query.
If result is more than 5 rows, a warning that result is limited.
If result has more than 5 columns, a warning with what columns were dropped.
If there is an error, return the error message truncated to 200 characters.

## restrictions

Returns `query_result.sample(5)` before returning the output. Also limits the return to 5 columns.

This is to prevent model context polution from the output of the excel data.

## safeguards

- **File size cap:** Reject files over 50MB. Large Excel files will hang the process.
- **Timeout:** Kill the python subprocess after 30 seconds. A bad cartesian join on large sheets will block indefinitely.
- **Row limit before query:** After reading sheets, if total rows across all sheets exceed 1M, reject with a message asking the user to filter or specify sheets.
- **No path traversal:** Validate that `filepath` resolves to an actual file and reject paths with `../` or symlinks.

## implementation

Tool is implemented as a pi extension with a Python subprocess.

### file structure

```
.pi/extensions/query-excel/
├── index.ts      # TypeScript extension
└── script.py     # Python script
```

### python script

Reads all sheets with polars (using fastexcel engine) and executes SQL via `pl.SQLContext`.

```py
dfs = pl.read_excel(filepath, sheet_id=0)
ctx = pl.SQLContext(
    **{
        k.replace(' ', '_').replace('-','_'): v
        for k, v in dfs.items()
    }
)
```

The python script is called as a subprocess from `index.ts` with args `--filepath` and `--query`.
