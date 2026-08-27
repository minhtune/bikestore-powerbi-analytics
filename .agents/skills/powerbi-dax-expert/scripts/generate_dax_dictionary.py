#!/usr/bin/env python3
"""
Power BI DAX Measure Catalog Generator
Outputs a structured DAX measure script ready to be executed in Tabular Editor,
DAX Studio, or copy-pasted into Power BI Desktop.
"""

import os
import sys
import json
import argparse

DAX_CATALOG = [
    {
        "table": "_Measures",
        "folder": "01. Financial & Revenue KPIs",
        "name": "Total Gross Revenue",
        "dax": "SUMX(Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[Unit_Price])",
        "format": "$#,##0",
        "description": "Total revenue before applying discounts."
    },
    {
        "table": "_Measures",
        "folder": "01. Financial & Revenue KPIs",
        "name": "Total Discount Amount",
        "dax": "SUMX(Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[Unit_Price] * Fact_Sales[Discount_Rate])",
        "format": "$#,##0",
        "description": "Total monetary discount granted across all sales."
    },
    {
        "table": "_Measures",
        "folder": "01. Financial & Revenue KPIs",
        "name": "Total Net Revenue",
        "dax": "[Total Gross Revenue] - [Total Discount Amount]",
        "format": "$#,##0",
        "description": "Net realized sales revenue after deducting discounts."
    },
    {
        "table": "_Measures",
        "folder": "01. Financial & Revenue KPIs",
        "name": "Average Discount %",
        "dax": "DIVIDE([Total Discount Amount], [Total Gross Revenue], 0)",
        "format": "0.0%",
        "description": "Effective average discount percentage."
    },
    {
        "table": "_Measures",
        "folder": "02. Volume & Orders",
        "name": "Total Orders",
        "dax": "DISTINCTCOUNT(Fact_Sales[Order_ID])",
        "format": "#,##0",
        "description": "Unique count of orders placed."
    },
    {
        "table": "_Measures",
        "folder": "02. Volume & Orders",
        "name": "Total Units Sold",
        "dax": "SUM(Fact_Sales[Quantity])",
        "format": "#,##0",
        "description": "Total physical items sold."
    },
    {
        "table": "_Measures",
        "folder": "02. Volume & Orders",
        "name": "Average Order Value",
        "dax": "DIVIDE([Total Net Revenue], [Total Orders], BLANK())",
        "format": "$#,##0.00",
        "description": "Average revenue generated per order."
    },
    {
        "table": "_Measures",
        "folder": "02. Volume & Orders",
        "name": "Units Per Order",
        "dax": "DIVIDE([Total Units Sold], [Total Orders], BLANK())",
        "format": "0.0",
        "description": "Average quantity of items in a single transaction."
    },
    {
        "table": "_Measures",
        "folder": "03. Time Intelligence (YoY / MoM / YTD)",
        "name": "Net Revenue SPLY",
        "dax": "CALCULATE([Total Net Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))",
        "format": "$#,##0",
        "description": "Net revenue for the same period in the prior year."
    },
    {
        "table": "_Measures",
        "folder": "03. Time Intelligence (YoY / MoM / YTD)",
        "name": "YoY Net Revenue Delta",
        "dax": "VAR CurrentRev = [Total Net Revenue]\nVAR PriorRev = [Net Revenue SPLY]\nRETURN IF(NOT ISBLANK(CurrentRev) && NOT ISBLANK(PriorRev), CurrentRev - PriorRev, BLANK())",
        "format": "$#,##0",
        "description": "Absolute dollar variance compared to same period last year."
    },
    {
        "table": "_Measures",
        "folder": "03. Time Intelligence (YoY / MoM / YTD)",
        "name": "YoY Net Revenue Growth %",
        "dax": "VAR CurrentRev = [Total Net Revenue]\nVAR PriorRev = [Net Revenue SPLY]\nRETURN DIVIDE(CurrentRev - PriorRev, PriorRev, BLANK())",
        "format": "+0.0%;-0.0%;0.0%",
        "description": "Percentage growth compared to prior year."
    },
    {
        "table": "_Measures",
        "folder": "03. Time Intelligence (YoY / MoM / YTD)",
        "name": "Net Revenue YTD",
        "dax": "CALCULATE([Total Net Revenue], DATESYTD(Dim_Date[Date]))",
        "format": "$#,##0",
        "description": "Cumulative net revenue Year-to-Date."
    },
    {
        "table": "_Measures",
        "folder": "04. Customer Analytics",
        "name": "Total Active Customers",
        "dax": "DISTINCTCOUNT(Fact_Sales[Customer_ID])",
        "format": "#,##0",
        "description": "Count of unique purchasing customers."
    },
    {
        "table": "_Measures",
        "folder": "04. Customer Analytics",
        "name": "Revenue Per Customer",
        "dax": "DIVIDE([Total Net Revenue], [Total Active Customers], BLANK())",
        "format": "$#,##0.00",
        "description": "Average net revenue per active customer."
    },
    {
        "table": "_Measures",
        "folder": "05. Inventory & Supply Chain",
        "name": "Total Stock Quantity",
        "dax": "SUM(Fact_Inventory[Quantity_In_Stock])",
        "format": "#,##0",
        "description": "Total units currently held across store inventories."
    },
    {
        "table": "_Measures",
        "folder": "05. Inventory & Supply Chain",
        "name": "Total Stock Value",
        "dax": "SUMX(Fact_Inventory, Fact_Inventory[Quantity_In_Stock] * RELATED(Dim_Product[List_Price]))",
        "format": "$#,##0",
        "description": "Monetary value of current stock at list price."
    },
    {
        "table": "_Measures",
        "folder": "06. Dynamic UI & Formatting",
        "name": "Dynamic Dashboard Title",
        "dax": "VAR SelectedYear = SELECTEDVALUE(Dim_Date[Year], \"All Years\")\nVAR SelectedBrand = SELECTEDVALUE(Dim_Product[Brand_Name], \"All Brands\")\nRETURN \"Executive Performance Overview - \" & SelectedBrand & \" (\" & SelectedYear & \")\"",
        "format": "Text",
        "description": "Dynamic header text for report canvases."
    }
]

def export_dax_dictionary(output_format="markdown", output_file=None):
    if output_format == "markdown":
        lines = ["# Power BI DAX Measure Catalog\n"]
        current_folder = None
        for m in DAX_CATALOG:
            if m["folder"] != current_folder:
                current_folder = m["folder"]
                lines.append(f"\n## 📁 Folder: `{current_folder}`\n")
            lines.append(f"### `{m['name']}`")
            lines.append(f"- **Description**: {m['description']}")
            lines.append(f"- **Format String**: `{m['format']}`")
            lines.append("```dax")
            lines.append(f"{m['name']} = \n{m['dax']}")
            lines.append("```\n")
        content = "\n".join(lines)
    elif output_format == "tabular_editor":
        # Tabular Editor C# Script to auto-create all measures
        lines = ["// Tabular Editor C# Script to Auto-Create Measures\n"]
        lines.append('var measureTable = Model.Tables["_Measures"];')
        for m in DAX_CATALOG:
            escaped_dax = m["dax"].replace('"', '""').replace("\n", " ")
            lines.append(f'var m_{m["name"].replace(" ", "_")} = measureTable.AddMeasure("{m["name"]}", "{escaped_dax}", "{m["folder"]}");')
            lines.append(f'm_{m["name"].replace(" ", "_")}.FormatString = "{m["format"]}";')
            lines.append(f'm_{m["name"].replace(" ", "_")}.Description = "{m["description"]}";')
        content = "\n".join(lines)
    else:
        content = json.dumps(DAX_CATALOG, indent=2)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"DAX Measure Catalog successfully written to: {output_file}")
    else:
        print(content)

def main():
    parser = argparse.ArgumentParser(description="Export DAX Measure Catalog")
    parser.add_argument("--format", "-f", choices=["markdown", "tabular_editor", "json"], default="markdown")
    parser.add_argument("--output", "-o", default=None, help="Output destination file")
    args = parser.parse_args()
    export_dax_dictionary(args.format, args.output)

if __name__ == "__main__":
    main()
