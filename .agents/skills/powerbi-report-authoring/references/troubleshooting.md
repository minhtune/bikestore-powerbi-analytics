# Troubleshooting PBIP & PBIR Report Authoring

This document catalogues the most frequent errors encountered when programmatically generating or modifying Power BI reports (`report.json` or PBIR), their root causes, and verified solutions.

---

## 1. Error: "Can't display this visual" (Column / Measure Not Found)

### Symptom
Power BI Desktop opens the report, but visuals show an error icon with the message:
`The column 'ColumnName' does not exist in table 'TableName'` or `Query error: Table '_Measures' does not contain measure 'MeasureName'`.

### Root Cause
1. **Naming Inconsistencies**: Speculative or human-friendly column names with spaces were used (e.g., `Dim_Product[Brand Name]`) when the underlying Semantic Model actually defines underscore naming (`Dim_Product[Brand_Name]`).
2. **Missing Measures**: The visual container references a measure that does not exist in the `_Measures` table (e.g., `Completed Orders Count` instead of `Total Units Sold`).

### Solution & Prevention
- **Inspect Before Generating**: Always run a schema check or inspect `_Measures.tmdl` / `model.bim` before defining visuals.
- Verify exact case and character match:
  - `Dim_Product`: `Product_ID`, `Product_Name`, `Brand_Name`, `Category_Name`, `Model_Year`, `List_Price`
  - `Dim_Customer`: `Customer_ID`, `Customer_Name`, `Email`, `City`, `State`, `Zip_Code`
  - `Dim_Store`: `Store_ID`, `Store_Name`, `City`, `State`
  - `Dim_Staff`: `Staff_ID`, `Staff_Name`, `Active_Status`
  - `Dim_Date`: `Date`, `Year`, `Quarter`, `Month`, `MonthName`, `YearMonth`
  - `Fact_Sales`: `Order_ID`, `Item_ID`, `Order_Status`, `Gross_Amount`, `Discount_Amount`, `Net_Amount`

---

## 2. Error: Corrupted Report or Visual Containers Ignored

### Symptom
Power BI Desktop reports `The report definition is invalid` or silently ignores visual containers added to `report.json`.

### Root Cause
In PBIP format v1.0 (`report.json`), the `config` field inside `visualContainers` must be a **JSON-escaped string**, NOT a nested JSON object:
- ❌ **Incorrect (Nested Object)**:
```json
{
  "x": 20, "y": 20, "width": 200, "height": 100,
  "config": { "name": "abc", "singleVisual": { ... } }
}
```
- ✅ **Correct (Escaped String)**:
```json
{
  "x": 20, "y": 20, "width": 200, "height": 100,
  "config": "{\"name\":\"abc\",\"singleVisual\":{...}}"
}
```

---

## 3. Error: UTF-8 BOM Parsing and Git Diff Noise

### Symptom
Power BI Desktop displays XML/JSON parser errors on opening, or `git diff` displays binary file warnings / unexpected header characters (`\ufeff`).

### Root Cause
Windows PowerShell 5.1 `Out-File` or `Set-Content` defaults to UTF-16 LE or UTF-8 with BOM (Byte Order Mark).

### Solution
Use explicit UTF-8 without BOM via .NET:
```powershell
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Resolve-Path $reportPath).Path, $finalJson, $utf8NoBom)
```

---

## 4. Error: Python Not Found on Windows (`App Execution Aliases`)

### Symptom
Executing `python script.py` returns:
`Python was not found; run without arguments to install from the Microsoft Store...`

### Root Cause
Windows development environments may not have Python in the system PATH, or corporate policies restrict Python execution.

### Solution
Provide a native PowerShell generator script (`.ps1`) using `[Security.Cryptography.RNGCryptoServiceProvider]` and `ConvertTo-Json`. PowerShell is pre-installed on 100% of modern Windows workstations.

---

## 5. Dual Query Binding Failure (`prototypeQuery` vs `projections`)

### Symptom
Visual renders as blank or throws `Visual query binding mismatch`.

### Root Cause
The `queryRef` in `projections` does not match the `Name` attribute in `prototypeQuery.Select`:
- In `projections.Values`: `[{"queryRef": "_Measures.Total Net Revenue"}]`
- In `prototypeQuery.Select`: Must have `{"Name": "_Measures.Total Net Revenue", ...}`
If there is a typo or mismatch between `queryRef` and `Name`, Power BI cannot map the data role to the query column.
