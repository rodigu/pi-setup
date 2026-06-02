# Basic Functionality

## Context
- File: `custom/tools/query-excel/example.xlsx`
- Tool: `query_excel` (parameters: `filepath`, `query`)
- Verify `details.columns`, `details.row_count`, `details.warnings` on success
- Verify `isError: true` on errors
- Write results to `custom/tools/query-excel/tests/basic-functionality.result.md`

---

- [ ] **Simple SELECT** — `SELECT * FROM Retail_Inventory LIMIT 10` — returns 5 sampled rows with warning: "Sampled 5 of 10 rows". Check `details.columns`, `details.row_count`, `details.warnings`
- [ ] **Column selection** — `SELECT "Product Name", "Category" FROM Retail_Inventory LIMIT 5` — returns only specified columns. Verify `details.columns` matches query
- [ ] **WHERE filter** — `SELECT * FROM Retail_Inventory WHERE "Unit Cost" > 100` — returns filtered results. Verify `details.row_count` reflects filtered count
- [ ] **Aggregate** — `SELECT COUNT(*), SUM("Units Sold") FROM Retail_Inventory` — returns aggregated result. Verify single row returned
- [ ] **GROUP BY** — `SELECT "Category", COUNT(*) FROM Retail_Inventory GROUP BY "Category"` — returns grouped results. Verify `details.row_count` matches number of groups
