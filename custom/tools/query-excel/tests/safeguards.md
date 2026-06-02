# Safeguards

## Context
- File: `custom/tools/query-excel/example.xlsx`
- Tool: `query_excel` (parameters: `filepath`, `query`)
- Verify `details.columns`, `details.row_count`, `details.warnings` on success
- Verify `isError: true` on errors
- Write results to `custom/tools/query-excel/tests/safeguards.result.md`

---

- [ ] **Path traversal** — provide filepath with `../` — returns `isError: true` with error about path traversal
- [ ] **Non-existent file** — provide path to non-existent file — returns `isError: true` with file not found error
- [ ] **Non-Excel file** — provide path to a `.txt` file — returns `isError: true` with read error
- [ ] **Invalid SQL** — `SELEC * FORM Retail_Inventory` — returns `isError: true` with error truncated to 200 chars
