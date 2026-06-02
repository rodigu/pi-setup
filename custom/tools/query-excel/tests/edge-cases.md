# Edge Cases

## Context
- File: `custom/tools/query-excel/example.xlsx`
- Tool: `query_excel` (parameters: `filepath`, `query`)
- Verify `details.columns`, `details.row_count`, `details.warnings` on success
- Verify `isError: true` on errors
- Write results to `custom/tools/query-excel/tests/edge-cases.result.md`

---

- [ ] **NULL handling** — `SELECT * FROM Retail_Inventory WHERE "Stock Status" IS NULL` — returns NULL values (not crash)
- [ ] **Special characters in query** — `SELECT * FROM Retail_Inventory WHERE "Product Name" LIKE '%é%'` — executes correctly
- [ ] **Case sensitivity** — `select * from retail_inventory` vs `SELECT * FROM Retail_Inventory` — Polars SQL is case-insensitive; should return same results
- [ ] **Quoted identifiers** — `SELECT "Product Name" FROM Retail_Inventory` — handles column names with spaces correctly
- [ ] **Very long query** — submit a query string of 1000+ characters — executes without truncation or crash
- [ ] **Cross-sheet query** — `SELECT a."Product Name", b."Total Revenue" FROM Retail_Inventory a JOIN E_Commerce_Orders b ON a."Product Name" = b."Product Name"` — joins work across sheets
