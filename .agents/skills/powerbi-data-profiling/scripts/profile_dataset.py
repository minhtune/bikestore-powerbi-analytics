#!/usr/bin/env python3
"""
Power BI Data Profiler Script
Inspects Excel and CSV datasets, profiles tables, detects keys, nulls, cardinality,
and suggests dimensional star schema mappings for Power BI.
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np

def profile_dataframe(df: pd.DataFrame, table_name: str) -> dict:
    total_rows = len(df)
    cols_profile = []
    potential_pks = []
    
    # Detect all-blank / empty rows
    completely_blank_rows = int(df.isna().all(axis=1).sum())
    
    for col in df.columns:
        series = df[col]
        # Count NA or empty strings
        is_empty_str = series.astype(str).str.strip().eq("") if series.dtype == object else pd.Series(False, index=series.index)
        null_count = int(series.isna().sum() + is_empty_str.sum())
        null_pct = round((null_count / total_rows * 100) if total_rows > 0 else 0, 2)
        distinct_count = int(series.nunique(dropna=False))
        dtype = str(series.dtype)
        
        is_pk = (null_count == 0) and (distinct_count == total_rows) and total_rows > 0
        if is_pk:
            potential_pks.append(col)
            
        sample_vals = series.dropna().unique()[:3].tolist()
        sample_str = ", ".join(map(str, sample_vals))
        
        min_val, max_val = None, None
        if pd.api.types.is_numeric_dtype(series) and not series.dropna().empty:
            min_val = float(series.min())
            max_val = float(series.max())
        elif pd.api.types.is_datetime64_any_dtype(series) and not series.dropna().empty:
            min_val = str(series.min())
            max_val = str(series.max())
            
        cols_profile.append({
            "column": col,
            "dtype": dtype,
            "null_count": null_count,
            "null_pct": null_pct,
            "distinct_count": distinct_count,
            "is_potential_pk": is_pk,
            "min": min_val,
            "max": max_val,
            "sample_values": sample_str
        })
        
    return {
        "table_name": table_name,
        "row_count": total_rows,
        "col_count": len(df.columns),
        "completely_blank_rows": completely_blank_rows,
        "potential_pks": potential_pks,
        "columns": cols_profile
    }

def main():
    parser = argparse.ArgumentParser(description="Profile Excel/CSV for Power BI Modeling")
    parser.add_argument("--file", "-f", default="BikeStore.xlsx", help="Path to Excel (.xlsx, .xls) or CSV file")
    parser.add_argument("--output", "-o", default=None, help="Output markdown summary file path")
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
        
    print(f"Profiling dataset: {args.file} ...")
    tables = {}
    
    if args.file.endswith((".xlsx", ".xls")):
        xl = pd.ExcelFile(args.file)
        for sheet in xl.sheet_names:
            df = xl.parse(sheet)
            tables[sheet] = df
    else:
        df = pd.read_csv(args.file)
        table_name = os.path.splitext(os.path.basename(args.file))[0]
        tables[table_name] = df
        
    profiles = []
    for name, df in tables.items():
        prof = profile_dataframe(df, name)
        profiles.append(prof)
        
    # Detect potential foreign keys between tables
    relationships = []
    for p1 in profiles:
        t1 = p1["table_name"]
        for c1 in p1["columns"]:
            col1 = c1["column"]
            # Look for matching column names in other tables
            for p2 in profiles:
                t2 = p2["table_name"]
                if t1 != t2:
                    for c2 in p2["columns"]:
                        col2 = c2["column"]
                        if col1 == col2:
                            # If col2 is PK in t2 and col1 is in t1
                            if c2["is_potential_pk"] and not c1["is_potential_pk"]:
                                relationships.append({
                                    "from_table": t1,
                                    "from_col": col1,
                                    "to_table": t2,
                                    "to_col": col2,
                                    "type": "Many-to-One (*:1)"
                                })
                            elif c1["is_potential_pk"] and c2["is_potential_pk"]:
                                relationships.append({
                                    "from_table": t1,
                                    "from_col": col1,
                                    "to_table": t2,
                                    "to_col": col2,
                                    "type": "One-to-One (1:1)"
                                })

    # Generate Markdown Report
    lines = []
    lines.append(f"# Power BI Data Profile Report: `{os.path.basename(args.file)}`\n")
    lines.append("## 1. Executive Summary\n")
    lines.append(f"- **Total Tables / Sheets**: {len(tables)}")
    total_records = sum(p['row_count'] for p in profiles)
    lines.append(f"- **Total Records Across Tables**: {total_records:,}\n")
    
    lines.append("### Table Catalog\n")
    lines.append("| Table Name | Row Count | Column Count | Primary Key Candidate | Suggested Role |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    for p in profiles:
        pk_str = ", ".join(p["potential_pks"]) if p["potential_pks"] else "None (Composite/Transaction)"
        role = "Fact Table" if "order" in p["table_name"] or "stock" in p["table_name"] or "sales" in p["table_name"] or not p["potential_pks"] else "Dimension Table"
        lines.append(f"| **{p['table_name']}** | {p['row_count']:,} | {p['col_count']} | `{pk_str}` | **{role}** |")
    lines.append("\n")

    lines.append("## 2. Detected Relationships (Star Schema Map)\n")
    if relationships:
        lines.append("| Fact / Child Table | Foreign Key | Dimension / Parent Table | Primary Key | Relationship Cardinality |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for r in relationships:
            lines.append(f"| `{r['from_table']}` | `{r['from_col']}` | `{r['to_table']}` | `{r['to_col']}` | **{r['type']}** |")
    else:
        lines.append("No explicit matching column relationships detected automatically.")
    lines.append("\n")

    lines.append("## 3. Table Column Profiles & Quality Checks\n")
    for p in profiles:
        lines.append(f"### Table: `{p['table_name']}` ({p['row_count']:,} rows, {p['col_count']} columns)\n")
        lines.append("| Column | Data Type | Nulls (%) | Distinct Count | Sample Values | Range / Min-Max |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for c in p["columns"]:
            pk_flag = " 🔑 *(PK)*" if c["is_potential_pk"] else ""
            range_str = f"[{c['min']} to {c['max']}]" if c['min'] is not None else "-"
            lines.append(f"| `{c['column']}`{pk_flag} | `{c['dtype']}` | {c['null_pct']}% ({c['null_count']}) | {c['distinct_count']} | {c['sample_values']} | {range_str} |")
    # Detect Quality Alerts
    quality_alerts = []
    for p in profiles:
        if p["completely_blank_rows"] > 0:
            quality_alerts.append(f"- ⚠️ **Table `{p['table_name']}`**: Detected {p['completely_blank_rows']} completely empty rows. **Must filter in Power Query** (`Table.SelectRows`) to avoid `DataFormat.Error` and broken 1:* relationships.")
        for c in p["columns"]:
            if c["null_count"] > 0 and c["column"].lower().endswith("_id"):
                quality_alerts.append(f"- ⚠️ **Table `{p['table_name']}`, Column `{c['column']}`**: Contains {c['null_count']} null/blank ID values. May break relationship cardinality.")

    lines.append("## 4. Data Quality & ETL Recommendations\n")
    if quality_alerts:
        for alert in quality_alerts:
            lines.append(alert)
    else:
        lines.append("- ✅ No severe blank rows or orphan key anomalies detected.")
    lines.append("- 💡 **Excel Sheet Loading**: Use `Kind=\"Sheet\"` with `Table.PromoteHeaders(..., [PromoteAllScalars=true])` if data is stored in standard worksheets.")
    lines.append("- 💡 **Parameterization**: Define a `FilePath` parameter query `meta [IsParameterQuery=true]` for zero-friction portability.")
    lines.append("\n")

    report_content = "\n".join(lines)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"Report written to {args.output}")
    else:
        print(report_content)

if __name__ == "__main__":
    main()
