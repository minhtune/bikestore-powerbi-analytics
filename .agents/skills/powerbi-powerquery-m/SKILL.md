---
name: powerbi-powerquery-m
description: >-
  Use this skill for authoring, refactoring, and optimizing Power Query (M Language) scripts in Power BI. Includes automated ETL pipelines, data source parameterization, schema transformation, denormalization joins, column typing, error handling, and M-based Date table generation.
---

# Power Query (M) Authoring & Optimization Skill

This skill provides ready-to-use Power Query M code templates, best practices, and ETL transformations.

## Core Transformation Rules in M

### 1. Source Parameterization
Always define a parameter for local file paths or server endpoints:
```powerquery
// FilePath Parameter definition
#"FilePath" = "C:\Data\BikeStore.xlsx" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```
This enables zero-friction portability across machines and deployment pipelines.

### 2. Standard ETL Pipeline Sequence
Structure every query cleanly in the Advanced Editor:
1. **Source Loading**: `Excel.Workbook(File.Contents(FilePath), null, true)` or `Csv.Document(...)`
2. **Navigation**: Select table / sheet.
3. **Promote Headers**: `Table.PromoteHeaders(..., [PromoteAllScalars=true])`
4. **Data Cleansing**: Trim, clean text, replace whitespace anomalies.
5. **Merge / Denormalize**: Perform Left Outer Joins on dimensions (e.g., merge Brand and Category into Product).
6. **Explicit Type Assignment**: Set rigorous types at the final step (`Int64.Type`, `type number`, `type date`, `type text`). Never leave types as `any`.
7. **Column Pruning & Renaming**: Remove technical staging keys, rename fields to business-friendly names.

### 3. Star Schema Query Architecture
In Power Query:
- Group queries in folders:
  - `00. Parameters`
  - `01. Staging (Hidden / Disable Load)`
  - `02. Dimensions (Load Enabled)`
  - `03. Facts (Load Enabled)`

## Reference Guide
- Complete M scripts for dimensional models & M Date Dimension: [powerquery_patterns.md](./references/powerquery_patterns.md)
