# Multi-Sheet

## Context
- File: `custom/tools/query-excel/example.xlsx`
- Tool: `query_excel` (parameters: `filepath`, `query`)
- Verify `details.columns`, `details.row_count`, `details.warnings` on success
- Verify `isError: true` on errors
- Write results to `custom/tools/query-excel/tests/multi-sheet.result.md`

---

- [ ] **Different sheet** — query `E_Commerce_Orders` table — returns correct sheet data (12 columns, 1000 rows)
- [ ] **Sheet name with hyphens/spaces** — verify "E-Commerce Orders" is accessible as `E_Commerce_Orders`
- [ ] **Both sheets in one query** — join `Retail_Inventory` and `E_Commerce_Orders` on `Product Name` — returns joined results
