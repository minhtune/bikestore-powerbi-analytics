# Power BI Project Engineering Rules

These rules apply to all data analysis, data modeling, DAX authoring, and dashboard construction tasks within this workspace.

## 1. Data Modeling (Kimball Star Schema)
- Always transform raw tables into a Star Schema with distinct Fact tables (`Fact_Sales`, `Fact_Inventory`) and Dimension tables (`Dim_Product`, `Dim_Customer`, `Dim_Store`, `Dim_Staff`, `Dim_Date`).
- Relationships must always be **One-to-Many (`1:*`) with Single Cross-Filter Direction** from Dimension to Fact.
- Never use Bi-directional relationships unless specifically required and approved for M2M bridge scenarios.
- All foreign keys and surrogate keys in Fact tables must be hidden from Report View.

## 2. Power Query (M Language)
- Always specify explicit data types on all columns in the final transformation step.
- Denormalize snowflake hierarchies (e.g. Brands and Categories into Product) directly in Power Query.
- Never leave local file paths hardcoded across multiple queries; use a shared `FilePath` parameter.

## 3. DAX Authoring Standards
- Always author **Explicit Measures**; never use implicit column aggregations in report visuals.
- Always use `VAR ... RETURN` syntax for readability and engine optimization.
- Always protect division with `DIVIDE(Numerator, Denominator, [AlternateResult])`.
- Store all measures inside a dedicated `_Measures` table organized into structured Display Folders.
- For Time Intelligence, use standard functions against the dedicated `Dim_Date` table.

## 4. Dashboard UI/UX Standards
- Canvas standard: 16:9 widescreen.
- Standard visual structure: Top Header + KPI Summary strip + 2-column or 3-column analytical body + granular breakdown table/matrix.
- Use the project theme located at `.agents/skills/powerbi-dashboard-design/resources/powerbi_theme.json`.
