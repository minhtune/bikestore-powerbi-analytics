# Expressions & Query Trees Reference

Power BI report visuals evaluate data via prototype queries (`prototypeQuery`).

## 1. Prototype Query Structure
```json
"prototypeQuery": {
  "Version": 2,
  "From": [
    {
      "Name": "alias",
      "Entity": "TableName",
      "Type": 0
    }
  ],
  "Select": [
    {
      "Column": {
        "Expression": {
          "SourceRef": {
            "Source": "alias"
          }
        },
        "Property": "ColumnName"
      },
      "Name": "TableName.ColumnName"
    },
    {
      "Measure": {
        "Expression": {
          "SourceRef": {
            "Source": "alias"
          }
        },
        "Property": "MeasureName"
      },
      "Name": "TableName.MeasureName"
    }
  ]
}
```

## 2. SourceRef Aliases
Assign simple, unique short alias identifiers:
- `m` for `_Measures`
- `d` for `Dim_Date`
- `c` for primary categorical table
- `t0`, `t1` for multi-table references
