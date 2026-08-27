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

### 2. High Cardinality Columns
- Columns with high uniqueness (e.g., GUIDs, high-precision timestamps `YYYY-MM-DD HH:MM:SS`, row IDs) consume the vast majority of memory in VertiPaq.
- **Rules**:
  - Split DateTime columns into separate `Date` and `Time` columns.
  - Remove unwanted primary keys or transactional detail IDs from Fact tables if not needed for drill-through.
  - Format columns strictly: integer IDs instead of string IDs whenever possible.

### 3. Dedicated Measure Table (`_Measures`)
- Never leave DAX measures scattered inside Fact or Dimension tables.
- Create a dedicated blank table: `_Measures = { BLANK() }`
- Move all explicit measures to `_Measures` and organize them into **Display Folders**:
  - `01. Core Sales & Volume`
  - `02. Profitability & Margins`
  - `03. Time Intelligence (YoY / MoM / YTD)`
  - `04. Customer Analytics`
  - `05. Inventory & Operations`
  - `06. Dynamic UI / Formatting`
