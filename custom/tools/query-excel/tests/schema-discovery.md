# Schema Discovery

## Context
- File: `custom/tools/query-excel/example.xlsx`
- Tool: `query_excel` (parameters: `filepath`, `query`)
- Verify `details.columns`, `details.row_count`, `details.warnings` on success
- Verify `isError: true` on errors
- Write results to `custom/tools/query-excel/tests/schema-discovery.result.md`

---

- [ ] **DESCRIBE** — `DESCRIBE Retail_Inventory` — returns column names and types
- [ ] **SHOW COLUMNS** — `SHOW COLUMNS FROM Retail_Inventory` — returns column names
- [ ] **DESCRIBE second sheet** — `DESCRIBE E_Commerce_Orders` — returns different column set (12 columns)
- [ ] **AVAILABLE SHEETS** — `SELECT * FROM _AVAILABLE_SHEETS` — returns list of all sheet names (Retail_Inventory, E_Commerce_Orders)
- [ ] **SHOW TABLES** — `SHOW TABLES` — returns list of available tables
