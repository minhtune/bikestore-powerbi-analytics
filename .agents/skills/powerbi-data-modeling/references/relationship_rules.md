# Power BI Relationships & VertiPaq Performance Rules

## VertiPaq Engine Fundamentals

Power BI uses the **VertiPaq** in-memory columnar engine. To achieve sub-second query latency and minimal memory footprint, follow these strict rules:

### 1. The Single-Direction (1:*) Mandate
- Always filter downstream: Filter flows from the **1-side** (Dimension) to the ***-side** (Fact).
- **Avoid Bi-directional filters**:
  - Creates ambiguous calculation paths.
  - Can drastically inflate query execution plans.
  - Generates cross-filter Cartesian overhead.
- If you need to filter a Dimension by a Fact measure (e.g. show only customers who bought Category X), use a DAX measure with `CALCULATETABLE` or visual-level measure filtering (`[Total Sales] > 0`) instead of enabling bi-directional cross-filtering on relationships.

### 2. Relationship Cardinality & The Blank Key Trap
Power BI validates that the "One" side of a `1:*` relationship contains distinct, unique values.
- **Common Failure**: When importing from Excel worksheets, blank rows at the end of the sheet get converted into blank/null keys. Multiple blank rows destroy the uniqueness of the primary key.
- **Result**: Power BI refuses to create a `1:*` relationship and forces a problematic `Many-to-Many (*:*)` relationship or throws a model validation error.
- **Rule**: In Power Query ETL, prune trailing empty rows on the primary key immediately after promoting headers.

### 3. High Cardinality Columns
- Columns with high uniqueness (e.g., GUIDs, high-precision timestamps `YYYY-MM-DD HH:MM:SS`, row IDs) consume the vast majority of memory in VertiPaq.
- **Rules**:
  - Split DateTime columns into separate `Date` and `Time` columns.
  - Remove unwanted primary keys or transactional detail IDs from Fact tables if not needed for drill-through.
  - Format columns strictly: integer IDs instead of string IDs whenever possible.

### 4. Dedicated Measure Table (`_Measures`)
- Never leave DAX measures scattered inside Fact or Dimension tables.
- Create a dedicated blank table: `_Measures = { BLANK() }`
- Move all explicit measures to `_Measures` and organize them into **Display Folders**:
  - `01. Financial & Revenue KPIs`
  - `02. Volume & Orders`
  - `03. Time Intelligence (YoY / MoM / YTD)`
  - `04. Customer Analytics`
  - `05. Inventory & Operations`
  - `06. Dynamic Titles & Formatting`
