# Table & Matrix Visual Specifications (`tableEx` / `pivotTable`)

Tables and matrices provide detailed record inspection and multi-attribute leaderboards.

## 1. Table Visual (`tableEx`)
Combines Dimension columns and DAX measures into a tabular list.

### Projections Mapping
All items (columns and measures) are mapped into `Values`:
```json
"projections": {
  "Values": [
    {"queryRef": "Dim_Store.Store_Name"},
    {"queryRef": "Dim_Store.City"},
    {"queryRef": "Dim_Store.State"},
    {"queryRef": "_Measures.Total Orders"},
    {"queryRef": "_Measures.Total Net Revenue"}
  ]
}
```

### Prototype Query
Each source entity is assigned an alias in `From` (`t0`, `t1`, `m`), and each field is added to `Select`:
```json
{
  "Version": 2,
  "From": [
    {"Name": "t0", "Entity": "Dim_Store", "Type": 0},
    {"Name": "m", "Entity": "_Measures", "Type": 0}
  ],
  "Select": [
    {
      "Column": {
        "Expression": {"SourceRef": {"Source": "t0"}},
        "Property": "Store_Name"
      },
      "Name": "Dim_Store.Store_Name"
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

### Sizing Guidelines
- Standard Bottom Row Table: `width: 1240px`, `height: 240px` (or split half `width: 620px`).
