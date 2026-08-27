---
name: powerbi-powerquery-m
description: >-
  Use this skill for authoring, refactoring, and optimizing Power Query (M Language) scripts in Power BI. Includes automated ETL pipelines, data source parameterization, schema transformation, denormalization joins, column typing, error handling, and M-based Date table generation.
---

# Power Query (M) Authoring & Optimization Skill

This skill provides ready-to-use Power Query M code templates, best practices, ETL transformations, and production troubleshooting rules.

## Core Transformation Rules in M

### 1. Source Parameterization
Always define a parameter for local file paths or server endpoints:
```powerquery
// FilePath Parameter definition
#"FilePath" = "C:\Data\BikeStore.xlsx" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```
This enables zero-friction portability across machines and deployment pipelines without modifying downstream table queries.

### 2. Standard ETL Pipeline Sequence
Structure every query cleanly in the Advanced Editor:
1. **Source Loading**: `Excel.Workbook(File.Contents(FilePath), null, true)` or `Csv.Document(...)`
2. **Navigation**: Select table / sheet (`Kind="Sheet"` or `Kind="Table"`).
3. **Promote Headers**: `Table.PromoteHeaders(..., [PromoteAllScalars=true])`
4. **Blank Row Pruning (CRITICAL)**: Filter out trailing empty rows before type conversion (`Table.SelectRows(..., each [id] <> null and [id] <> "")`).
5. **Data Cleansing**: Trim, clean text, replace whitespace anomalies.
6. **Merge / Denormalize**: Perform Left Outer Joins on dimensions (e.g., merge Brand and Category into Product).
7. **Explicit Type Assignment**: Set rigorous types at the final step (`Int64.Type`, `type number`, `type date`, `type text`). Never leave types as `any`.
8. **Column Pruning & Renaming**: Remove technical staging keys, rename fields to business-friendly names.

### 3. Production Gotchas & Best Practices

#### A. Excel Sheet vs. Table Navigation (`KeyNotFoundException`)
- **Problem**: Accessing `Source{[Item="orders", Kind="Table"]}[Data]` fails with `The key didn't match any rows in the table` when Excel data is stored in standard worksheets rather than named Excel Tables (`ListObject`).
- **Solution**: Target `Kind="Sheet"` by default, followed by `Table.PromoteHeaders(..., [PromoteAllScalars=true])`:
```powerquery
orders_Sheet = Source{[Item="orders", Kind="Sheet"]}[Data],
#"Promoted Orders" = Table.PromoteHeaders(orders_Sheet, [PromoteAllScalars=true]),
```

#### B. Trailing Empty Rows Breaking Types & Relationships
- **Problem**: Excel files frequently contain phantom empty rows with formatting or trailing nulls. When converting columns to `Int64.Type`, empty strings `""` cause `DataFormat.Error: We couldn't convert to Number`. Furthermore, blank IDs in Dimension tables violate 1-to-Many relationship constraints in Power BI.
- **Solution**: Immediately after promoting headers, filter on primary/foreign keys:
```powerquery
#"Filtered Blank Rows" = Table.SelectRows(#"Promoted Headers", each [order_id] <> null and [order_id] <> "")
```

#### C. Safe Table Merges & Expansion
- Always filter out null/blank join keys before performing `Table.NestedJoin`.
- Use explicit column selection during `Table.ExpandTableColumn` to prevent accidental schema changes if upstream sources add new columns.

### 4. Star Schema Query Architecture
In Power Query:
- Group queries in folders:
  - `00. Parameters`
  - `01. Staging (Hidden / Disable Load)`
  - `02. Dimensions (Load Enabled)`
  - `03. Facts (Load Enabled)`

## Reference Guide
- Complete M scripts for dimensional models & M Date Dimension: [powerquery_patterns.md](./references/powerquery_patterns.md)
