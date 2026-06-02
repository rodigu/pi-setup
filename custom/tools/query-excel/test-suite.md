# query_excel Test Suite

Each test should be executed by the LLM using the `query_excel` tool. Report pass/fail and any unexpected behavior.

## Prerequisites

- Test file: `custom/tools/query-excel/example.xlsx`

---

## Response Validation

**Successful responses** must include:
- `details.columns` — array of column names
- `details.row_count` — number of rows returned
- `content[0].text` — formatted table output

**Error responses** must include:
- `isError: true`
- `content[0].text` — error message starting with "Error:"

**Warnings** (when applicable):
- `details.warnings` — array of warning strings
- `content[0].text` — lines starting with `⚠️`

---

## Test Files

- [basic-functionality.md](tests/basic-functionality.md)
- [multi-sheet.md](tests/multi-sheet.md)
- [schema-discovery.md](tests/schema-discovery.md)
- [output-restrictions.md](tests/output-restrictions.md)
- [safeguards.md](tests/safeguards.md)
- [edge-cases.md](tests/edge-cases.md)


