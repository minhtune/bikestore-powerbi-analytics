# Power BI Project Guidelines

When operating in this project, follow the **Power BI Analytics Plugin** standards:

1. **Star Schema Architecture**: Denormalize dimensions into clean Star Schemas (`Dim_Product`, `Dim_Customer`, `Dim_Store`, `Dim_Staff`, `Dim_Date`) and Fact tables (`Fact_Sales`, `Fact_Inventory`).
2. **1-to-Many Single Filter Direction**: Always ensure relationships flow 1:* from Dimension to Fact.
3. **Explicit DAX Measures**: Use `VAR / RETURN` syntax, `DIVIDE()`, and store measures in the `_Measures` table with Display Folders.
4. **Power Query ETL**: Provide complete `let ... in` scripts with explicit typing and parameterized file paths.
5. **Interactive UI/UX**: Use executive KPI card layouts, 16:9 canvas grids, and consistent color palettes.
