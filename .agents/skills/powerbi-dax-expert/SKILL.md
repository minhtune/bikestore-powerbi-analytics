---
name: powerbi-dax-expert
description: >-
  Use this skill for writing, debugging, and optimizing enterprise DAX (Data Analysis Expressions) measures in Power BI. Covers Core KPIs, Time Intelligence (YoY, MoM, YTD), Profitability, Customer RFM & Cohorts, Dynamic Formatting, DAX optimization (VAR/RETURN, KEEPFILTERS, CALCULATE filter modifiers), and measure catalog generation.
---

# Power BI DAX Engineering & KPI Mastery Skill

This skill guides the authoring of robust, high-performance DAX calculations for Power BI dashboards.

## Core Rules for Production DAX

### 1. Variables (`VAR` / `RETURN`) Mandate
Always use `VAR` blocks to:
- Improve readability and maintainability.
- Prevent duplicate sub-expression evaluations (improves VertiPaq engine execution).
- Freeze evaluation context at the variable definition point.

```dax
YoY Sales Growth % = 
VAR CurrentSales = [Total Net Revenue]
VAR PriorYearSales = [Sales SPLY]
VAR SalesDelta = CurrentSales - PriorYearSales
RETURN
    DIVIDE(SalesDelta, PriorYearSales, BLANK())
```

### 2. Zero-Division & Null Safety
- **Never** use raw slash `/` for division.
- **Always** use `DIVIDE(Numerator, Denominator, [AlternateResult])` to avoid `#DIV/0!` runtime exceptions.

### 3. Filter Context & Performance Best Practices
- **Never** filter entire tables inside `CALCULATE`:
  - ❌ `CALCULATE([Total Sales], FILTER(Fact_Sales, Fact_Sales[Discount_Rate] > 0))` (Forces full table scan / materialization).
  - ✅ `CALCULATE([Total Sales], KEEPFILTERS(Fact_Sales[Discount_Rate] > 0))` (Pushes predicate to column storage engine).
- **Use Explicit Measures**: Never aggregate naked columns inside visual buckets (`Sum of list_price`). Always reference explicit measures `[Total Net Revenue]`.

## Measure Organization & Schema Synchronization
1. **Dedicated Measure Table**: All measures must be stored in the dedicated `_Measures` table organized into structured Display Folders:
   - `01. Financial & Revenue KPIs`
   - `02. Volume & Orders`
   - `03. Time Intelligence (YoY / MoM / YTD)`
   - `04. Customer Analytics & RFM`
   - `05. Operations & Inventory`
   - `06. Dynamic Titles & Formatting`
2. **Strict Naming Synchronization with Visuals**:
   - Every measure name defined in DAX / TMDL / `model.bim` must match character-for-character with visual bindings in `report.json`.
   - Never rename a measure in the model without updating visual container `prototypeQuery` bindings, or visuals will break with *"Can't display this visual / Table '_Measures' does not contain measure"*.

## Reference Guides & Scripts
- Complete DAX Measure Library: [dax_patterns.md](./references/dax_patterns.md)
- Time Intelligence Patterns: [time_intelligence.md](./references/time_intelligence.md)
- VertiPaq DAX Optimization: [dax_optimization.md](./references/dax_optimization.md)
- Measure Catalog Generator: `python3 .agents/skills/powerbi-dax-expert/scripts/generate_dax_dictionary.py`
