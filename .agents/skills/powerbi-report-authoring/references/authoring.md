# PBIR & PBIP Visual Authoring Guide

## Core Mechanics

In Power BI Project (`.pbip`), visuals are defined in either:
1. **PBIR (version 4.0)**: Individual JSON files per visual in `definition/pages/<pageId>/visuals/<visualId>/visual.json`.
2. **Standard PBIP (version 1.0)**: A single `report.json` with an array of `visualContainers` per section.

### Visual Container Specification (Standard PBIP report.json)

```json
{
  "x": 20,
  "y": 80,
  "z": 1000,
  "width": 280,
  "height": 110,
  "config": "{\"name\":\"<visual_id>\",\"layouts\":[{\"id\":0,\"position\":{\"x\":20,\"y\":80,\"z\":1000,\"width\":280,\"height\":110}}],\"singleVisual\":{...}}"
}
```

### Visual Specifications
- `card`: Single measure display for KPIs (`Total Net Revenue`, `Total Orders`, `AOV`, `Active Customers`).
- `clusteredBarChart`: Comparison of categories and brands.
- `lineChart`: Time series trend by Month/Year.
- `pivotTable` / `tableEx`: Store performance and inventory breakdown.
