# Cartesian Visual Specifications (Bar & Line Charts)

Cartesian charts represent comparisons, distributions, and trends over time.

## 1. Clustered Bar Chart (`clusteredBarChart`)
Used for categorical comparisons (e.g. Revenue by Category, Orders by Store).

### Projections Mapping
- `Category`: `[{"queryRef": "Dim_Product.Category_Name", "active": true}]`
- `Y`: `[{"queryRef": "_Measures.Total Net Revenue"}]`

### Prototype Query
```json
{
  "Version": 2,
  "From": [
    {"Name": "c", "Entity": "Dim_Product", "Type": 0},
    {"Name": "m", "Entity": "_Measures", "Type": 0}
  ],
  "Select": [
    {
      "Column": {
        "Expression": {"SourceRef": {"Source": "c"}},
        "Property": "Category_Name"
      },
      "Name": "Dim_Product.Category_Name"
    },
    {
      "Measure": {
        "Expression": {"SourceRef": {"Source": "m"}},
        "Property": "Total Net Revenue"
      },
      "Name": "_Measures.Total Net Revenue"
    }
  ]
}
```

---

## 2. Line Chart (`lineChart`)
Used for chronological time intelligence and trend lines.

### Projections Mapping
- `Category`: `[{"queryRef": "Dim_Date.YearMonth", "active": true}]`
- `Y`: `[{"queryRef": "_Measures.Total Net Revenue"}]`

### Recommended Sizing
- Full width: `1240px` (or half width `600px - 730px`)
- Height: `310px`
