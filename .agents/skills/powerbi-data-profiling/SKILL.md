---
name: powerbi-data-profiling
description: >-
  Use this skill to inspect, profile, and perform Exploratory Data Analysis (EDA) on raw tabular data (Excel, CSV, SQL, Parquet) for Power BI projects. It analyzes schema, data types, null rates, cardinality, primary/foreign key relationships, and business grain.
---

# Power BI Data Profiling & Schema Discovery Skill

This skill guides the rapid inspection, quality assessment, and schema discovery of raw datasets before importing them into Power BI.

## When to Use
- When receiving a new dataset (e.g., `BikeStore.xlsx`, CSV exports, or database tables).
- When discovering relationships, primary keys, foreign keys, and grain for Dimensional Modeling.
- When identifying data quality anomalies (null values, negative prices, orphaned keys, date formats).

## Profiling Workflow

### 1. Run Automated Profiling
Execute the automated dataset profiler script:
```bash
python3 .agents/skills/powerbi-data-profiling/scripts/profile_dataset.py --file "<path-to-excel-or-csv>"
```

### 2. Analyze Structural Characteristics
Check the following dimensions for each table:
1. **Grain**: What does a single row represent? (e.g., an individual line item in an order, a customer record, a daily inventory snapshot).
2. **Key Candidates**: Identify Unique Primary Keys (PK) and Foreign Keys (FK) linking tables.
3. **Cardinality**: Check distinct value counts to detect low-cardinality slicer dimensions vs high-cardinality attributes.
4. **Data Types**: Verify numeric formats (currency, quantity, discount rates), dates (order_date, shipped_date), and text fields.

### 3. Data Quality Checks & Common Traps
- **Trailing Blank Rows**: Excel sheets frequently contain empty formatted rows that produce blank strings `""` or `null`s, breaking numeric conversions (`DataFormat.Error`) and destroying 1:* relationship cardinality.
- **Excel Sheet vs Table Structure**: Check if data is stored in standard Worksheets (`Kind="Sheet"`) or official Excel Tables (`Kind="Table"`) to prevent `KeyNotFoundException` during Power Query navigation.
- **Key Integrity**: Ensure primary key candidates have 0 null/blank values and 100% uniqueness before modeling.

### 4. Output Requirements
Always provide the user with:
- **Entity Relationship Summary**: Tables, row counts, and primary-foreign key links.
- **Fact vs Dimension Classification**:
  - **Fact Candidates**: Tables containing transactional metrics, events, and numerical measures (`orders`, `order_items`, `stocks`).
  - **Dimension Candidates**: Tables containing descriptive attributes, master data, hierarchies (`customers`, `products`, `stores`, `staffs`, `categories`, `brands`).
- **Data Quality Alerts & ETL Guidance**: Warnings about trailing blank rows, Sheet vs Table navigation, parameterization recommendations, and date parsing anomalies.
