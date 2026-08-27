---
name: powerbi-data-modeling
description: >-
  Use this skill to design, validate, and optimize Power BI semantic data models using Kimball Star Schema methodology. Covers Fact & Dimension table classification, relationship cardinality, snowflake-to-star flattening, role-playing date dimensions, and VertiPaq engine optimization.
---

# Power BI Data Modeling (Star Schema) Skill

This skill guides the design of enterprise-grade, performant, and maintainable dimensional models in Power BI.

## Core Modeling Principles

### 1. Star Schema over Snowflake & Flat Tables
- **Why**: Power BI's in-memory columnar database (VertiPaq) is optimized for star schemas. Star schemas minimize memory consumption, maximize relationship traversal speed, and simplify DAX measures.
- **Action**: Denormalize/flatten snowflake chains (e.g., merge `Categories` and `Brands` directly into `Dim_Product`).

### 2. Fact vs Dimension Classification
- **Fact Tables** (`Fact_*`):
  - Contain numeric measurements, transactional events, metrics, and foreign keys.
  - Examples: `Fact_Sales` (from `orders` + `order_items`), `Fact_Inventory` (`stocks`).
  - Best Practice: Hide all surrogate/foreign keys in Fact tables from Report View. Never use naked columns from Fact tables in visuals; use explicit DAX measures instead.
- **Dimension Tables** (`Dim_*`):
  - Contain descriptive attributes, hierarchies, categories, geographic data, and customer demographics used for filtering, slicing, and grouping.
  - Examples: `Dim_Customer`, `Dim_Product`, `Dim_Store`, `Dim_Staff`, `Dim_Date`.
  - Must have a clean unique Primary Key (PK).

### 3. Relationship Golden Rules
1. **Direction**: **Single Direction (`1:*`)** from Dimension to Fact.
   - ⚠️ **NEVER** use Bi-Directional filtering (`<->`) unless solving a specific M2M bridge scenario with strict justification. Bi-directional filtering causes ambiguity, incorrect totals, and severe performance degradation.
2. **Cardinality**: Ensure **One-to-Many (`1:*`)**. 
3. **Role-Playing Dimensions**:
   - For multiple dates (e.g. `Order Date`, `Required Date`, `Shipped Date`), use ONE `Dim_Date` table.
   - Keep the primary relationship active (`Fact_Sales[Order Date] -> Dim_Date[Date]`).
   - Create inactive relationships for the others, activated on demand via `USERELATIONSHIP()` in DAX measures.

### 4. Date Dimension Requirement
Always create a dedicated `Dim_Date` (Calendar) table marked as an official Date Table in Power BI. Do not rely on Auto Date/Time hierarchies (disable "Auto Date/Time" in Options).

## Reference Guides
- Detailed Star Schema transformation guide: [star_schema_guide.md](./references/star_schema_guide.md)
- Relationship cardinality & VertiPaq performance rules: [relationship_rules.md](./references/relationship_rules.md)
