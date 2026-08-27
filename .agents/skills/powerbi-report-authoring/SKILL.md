---
name: powerbi-report-authoring
description: >-
  Create, modify, and troubleshoot Power BI report files in PBIR/PBIP format. Covers visual containers, query bindings, prototypeQuery structure, schema alignment with Semantic Model, UTF-8 BOM prevention, and native Windows automation.
---

# Power BI Report Authoring Skill (PBIP & PBIR Format)

This skill enables programmatic reading, editing, generation, and troubleshooting of Power BI report definition files in **PBIP (Power BI Project - `report.json`)** and **PBIR (Enhanced Report Format)**.

## Core Rules & Production Mandates

### 1. Strict Schema Alignment (NO Speculative Naming)
Every visual field binding (`queryRef`, `Select`, `From`) **MUST match exactly** with the Semantic Model (`model.bim` / TMDL):
- ❌ Do NOT use friendly names with spaces (e.g. `Brand Name`, `Category Name`, `Customer Full Name`) if the model defined them as `Brand_Name`, `Category_Name`, `Customer_Name`.
- ❌ Do NOT reference non-existent measures. Visuals bound to missing measures will fail silently or display "Can't display this visual" with query failure.
- ✅ Always inspect `_Measures.tmdl` or `model.bim` first to obtain the exact measure catalog.

### 2. PBIP v1.0 `report.json` Escaped Config String Mandate
In PBIP format v1.0 (`report.json`), the `config` property of each container is **NOT a raw nested JSON object**—it is a **stringified JSON**:
```json
{
  "x": 20,
  "y": 20,
  "z": 1000,
  "width": 230,
  "height": 95,
  "config": "{\"name\":\"a60b0b5a213bafff0553\",\"layouts\":[...],\"singleVisual\":{...}}"
}
```
- In Python: `"config": json.dumps(config_obj, ensure_ascii=False)`
- In PowerShell: `$configJson = $configObj | ConvertTo-Json -Depth 10 -Compress`

If serialized as a raw nested object, Power BI Desktop will fail to parse the visual container.

### 3. Dual Query Binding (`projections` + `prototypeQuery`)
Every visual container must define both:
1. `projections`: Maps data roles (e.g. `Values`, `Category`, `Y`, `Rows`) to query references.
2. `prototypeQuery`: Contains `From` (alias mappings) and `Select` (measures and columns).
The `queryRef` in `projections` MUST equal the `Name` attribute in `Select`.

### 4. File Encoding: UTF-8 Without BOM Mandate
Power BI Desktop parsers and Git tracking require standard UTF-8 without Byte Order Mark (BOM).
In PowerShell 5.1, `Out-File` and `Set-Content` default to UTF-16 LE or UTF-8 with BOM, which causes file corruption or git noise.
- ✅ Always write report JSON using:
```powershell
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Resolve-Path $reportPath).Path, $finalJson, $utf8NoBom)
```

### 5. Windows Native Automation Priority (PowerShell vs Python)
On Windows developer machines or corporate environments, Python may not be installed or configured in system PATH (triggering Microsoft Store execution alias warnings).
- **Rule**: When automating Power BI report authoring on Windows, always provide a native PowerShell script (`.ps1`) alongside or as the primary tool. PowerShell requires zero installations and runs natively.

## Visual Type Mapping Reference

| Visual Type | PBIP `visualType` | Primary Roles | Query Structure |
|---|---|---|---|
| Card | `card` | `Values` | Single Measure |
| Clustered Bar | `clusteredBarChart` | `Category`, `Y` | Dimension Column + Measure |
| Line Chart | `lineChart` | `Category`, `Y` | Date Dimension Column + Measure |
| Table / Matrix | `tableEx` / `pivotTable` | `Values` | Multiple Columns & Measures |
| Slicer | `slicer` | `Values` | Slicing Dimension Column |

## Reference Guides
- [Authoring Guide](./references/authoring.md)
- [Troubleshooting & Common Errors](./references/troubleshooting.md)
- [Card Visuals](./references/card.md)
- [Cartesian Charts](./references/cartesian.md)
- [Tables & Matrices](./references/table.md)
- [Expressions & Query Trees](./references/expressions.md)
- [Slicers](./references/slicers.md)
