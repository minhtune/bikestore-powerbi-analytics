---
name: powerbi-dashboard-design
description: >-
  Use this skill to design professional, enterprise-grade Power BI dashboard layouts, visual hierarchy, UX/UI theming, chart selection, interactive navigation (bookmarks, drill-through, tooltips), and generate Power BI Theme JSON files and dashboard blueprints.
---

# Power BI Dashboard UI/UX & Visual Design Skill

This skill guides the design of aesthetic, user-friendly, and actionable Power BI dashboards.

## Core UI/UX Architecture

### 1. Canvas Standard & Grid System
- Standard Canvas: **16:9 widescreen (1280x720 or 1920x1080)**.
- Margins: 16px to 24px consistent outer padding.
- Card Spacing: 12px to 16px gutter between visual containers.
- Container Style: Subtle rounded corners (8px radius), clean background cards (`#FFFFFF` on `#F4F6F9` background or modern Dark Mode `#1E222B` on `#14171F`), subtle 1px border or soft drop shadow.

### 2. Information Hierarchy (F-Pattern / Z-Pattern)
1. **Top Header**: Dynamic Title, Global Slicers (Date Range, Store, Brand/Category), Reset Filters Button.
2. **Top Row (KPI Summary Cards)**: 4 to 5 core high-level metrics with YoY Variance indicators and sparklines:
   - `Total Net Revenue` + YoY %
   - `Total Orders` + YoY %
   - `Average Order Value (AOV)`
   - `Units Sold`
   - `Active Customers`
3. **Middle Section (Primary Trends & Drivers)**:
   - Left (60% width): Monthly Revenue Trend vs SPLY (Line / Area Chart).
   - Right (40% width): Revenue by Category / Brand (Horizontal Bar Chart).
4. **Bottom Section (Granular Breakdown & Matrix)**:
   - Store / Staff Leaderboard (Matrix with Data Bars).
   - Top 10 Products by Revenue & Stock status.

### 3. Visual Selection Matrix
| Analytic Question | Recommended Visual | Visual to Avoid |
| :--- | :--- | :--- |
| Metric summary & YoY status | **New Card (Preview)** with reference labels | Default single number card |
| Trend over time | **Line Chart** or **Area Chart** | Multi-colored bar chart with 50 bars |
| Category composition | **Horizontal Bar Chart** or **Treemap** | Pie / Donut chart with > 5 slices |
| Target vs Actual | **Bullet Chart** or **Line Chart with Target Line** | Gauge visual (takes too much space) |
| Multi-attribute detailed table | **Matrix** with conditional formatting / data bars | Unformatted raw table |
| Correlation / Outliers | **Scatter Plot** | Clustered column |

### 4. PBIP/PBIR Implementation & Error Prevention
When translating designs to code (`report.json` / PBIR):
- **Exact Schema Alignment**: Visual field bindings must match exact column/measure names in the model (e.g. `Brand_Name` instead of `Brand Name`).
- **Stringified JSON in PBIP v1.0**: The `config` property of each `visualContainer` in `report.json` must be a JSON-escaped string.
- **UTF-8 No BOM**: Always write report JSON files without BOM.
- **Native Automation**: Provide native PowerShell `.ps1` alongside Python scripts for friction-free execution on Windows.

## Theme & Blueprint Resources
- Power BI Theme JSON: [powerbi_theme.json](./resources/powerbi_theme.json)
- Dashboard Layout Architecture: [layout_and_ui_ux.md](./references/layout_and_ui_ux.md)
- Export Interactive Blueprint: `python3 .agents/skills/powerbi-dashboard-design/scripts/export_blueprint.py`
- Report Authoring & PBIP Troubleshooting: [powerbi-report-authoring](../powerbi-report-authoring/SKILL.md)
