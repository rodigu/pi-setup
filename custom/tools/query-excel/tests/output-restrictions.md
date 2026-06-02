# Output Restrictions

## Context
- File: `custom/tools/query-excel/example.xlsx`
- Tool: `query_excel` (parameters: `filepath`, `query`)
- Verify `details.columns`, `details.row_count`, `details.warnings` on success
- Verify `isError: true` on errors
- Write results to `custom/tools/query-excel/tests/output-restrictions.result.md`

---

- [ ] **Column limit** — `SELECT * FROM Retail_Inventory` (11 columns) — returns 5 columns with warning listing dropped columns
- [ ] **Row sampling** — `SELECT * FROM Retail_Inventory` (1000 rows) — returns 5 rows with warning showing original count
- [ ] **Both limits** — `SELECT * FROM E_Commerce_Orders` (12 cols, 1000 rows) — returns 5 columns AND 5 rows with both warnings
