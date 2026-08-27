#!/usr/bin/env python3
"""
Power BI Model.bim Generator
Generates a complete, standards-compliant TMSL model.bim file for Power BI Desktop PBIP.
"""

import os
import json

def generate_model_bim(output_path="BikeStore_Analytics.SemanticModel/model.bim"):
    model_bim = {
        "name": "BikeStore_Analytics",
        "compatibilityLevel": 1567,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "sourceQueryCulture": "en-US",
            "expressions": [
                {
                    "name": "FilePath",
                    "kind": "m",
                    "expression": [
                        "\"C:\\\\Users\\\\minle\\\\Downloads\\\\power bi\\\\BikeStore.xlsx\" meta [IsParameterQuery=true, Type=\"Text\", IsParameterQueryRequired=true]"
                    ],
                    "lineageTag": "a73f8b91-4e20-41fa-8a50-019918239011",
                    "annotations": [
                        {
                            "name": "PBI_NavigationStepName",
                            "value": "Navigation"
                        },
                        {
                            "name": "PBI_ResultType",
                            "value": "Text"
                        }
                    ]
                }
            ],
            "tables": [
                {
                    "name": "_Measures",
                    "columns": [
                        {
                            "name": "MeasurePlaceholder",
                            "dataType": "string",
                            "isHidden": True,
                            "sourceColumn": "MeasurePlaceholder",
                            "summarizeBy": "none"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "_Measures",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText(\"i44FAA==\", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [MeasurePlaceholder = _t])",
                                    "in",
                                    "    Source"
                                ]
                            }
                        }
                    ],
                    "measures": [
                        {
                            "name": "Total Gross Revenue",
                            "expression": "SUMX(Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[Unit_Price])",
                            "formatString": "$#,##0",
                            "displayFolder": "01. Financial & Revenue KPIs"
                        },
                        {
                            "name": "Total Discount Amount",
                            "expression": "SUMX(Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[Unit_Price] * Fact_Sales[Discount_Rate])",
                            "formatString": "$#,##0",
                            "displayFolder": "01. Financial & Revenue KPIs"
                        },
                        {
                            "name": "Total Net Revenue",
                            "expression": "[Total Gross Revenue] - [Total Discount Amount]",
                            "formatString": "$#,##0",
                            "displayFolder": "01. Financial & Revenue KPIs"
                        },
                        {
                            "name": "Average Discount %",
                            "expression": "DIVIDE([Total Discount Amount], [Total Gross Revenue], 0)",
                            "formatString": "0.0%",
                            "displayFolder": "01. Financial & Revenue KPIs"
                        },
                        {
                            "name": "Total Orders",
                            "expression": "DISTINCTCOUNT(Fact_Sales[Order_ID])",
                            "formatString": "#,##0",
                            "displayFolder": "02. Volume & Orders"
                        },
                        {
                            "name": "Total Units Sold",
                            "expression": "SUM(Fact_Sales[Quantity])",
                            "formatString": "#,##0",
                            "displayFolder": "02. Volume & Orders"
                        },
                        {
                            "name": "Average Order Value",
                            "expression": "DIVIDE([Total Net Revenue], [Total Orders], BLANK())",
                            "formatString": "$#,##0.00",
                            "displayFolder": "02. Volume & Orders"
                        },
                        {
                            "name": "Units Per Order",
                            "expression": "DIVIDE([Total Units Sold], [Total Orders], BLANK())",
                            "formatString": "0.0",
                            "displayFolder": "02. Volume & Orders"
                        },
                        {
                            "name": "Net Revenue SPLY",
                            "expression": "CALCULATE([Total Net Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))",
                            "formatString": "$#,##0",
                            "displayFolder": "03. Time Intelligence (YoY / MoM / YTD)"
                        },
                        {
                            "name": "YoY Net Revenue Delta",
                            "expression": "VAR CurrentRev = [Total Net Revenue]\nVAR PriorRev = [Net Revenue SPLY]\nRETURN IF(NOT ISBLANK(CurrentRev) && NOT ISBLANK(PriorRev), CurrentRev - PriorRev, BLANK())",
                            "formatString": "$#,##0",
                            "displayFolder": "03. Time Intelligence (YoY / MoM / YTD)"
                        },
                        {
                            "name": "YoY Net Revenue Growth %",
                            "expression": "VAR CurrentRev = [Total Net Revenue]\nVAR PriorRev = [Net Revenue SPLY]\nRETURN DIVIDE(CurrentRev - PriorRev, PriorRev, BLANK())",
                            "formatString": "+0.0%;-0.0%;0.0%",
                            "displayFolder": "03. Time Intelligence (YoY / MoM / YTD)"
                        },
                        {
                            "name": "Net Revenue YTD",
                            "expression": "CALCULATE([Total Net Revenue], DATESYTD(Dim_Date[Date]))",
                            "formatString": "$#,##0",
                            "displayFolder": "03. Time Intelligence (YoY / MoM / YTD)"
                        },
                        {
                            "name": "Total Active Customers",
                            "expression": "DISTINCTCOUNT(Fact_Sales[Customer_ID])",
                            "formatString": "#,##0",
                            "displayFolder": "04. Customer Analytics"
                        },
                        {
                            "name": "Revenue Per Customer",
                            "expression": "DIVIDE([Total Net Revenue], [Total Active Customers], BLANK())",
                            "formatString": "$#,##0.00",
                            "displayFolder": "04. Customer Analytics"
                        },
                        {
                            "name": "Total Stock Quantity",
                            "expression": "SUM(Fact_Inventory[Quantity_In_Stock])",
                            "formatString": "#,##0",
                            "displayFolder": "05. Inventory & Supply Chain"
                        },
                        {
                            "name": "Total Stock Value",
                            "expression": "SUMX(Fact_Inventory, Fact_Inventory[Quantity_In_Stock] * RELATED(Dim_Product[List_Price]))",
                            "formatString": "$#,##0",
                            "displayFolder": "05. Inventory & Supply Chain"
                        }
                    ]
                },
                {
                    "name": "Dim_Date",
                    "dataCategory": "Time",
                    "columns": [
                        {
                            "name": "Date",
                            "dataType": "dateTime",
                            "isKey": True,
                            "formatString": "yyyy-MM-dd",
                            "sourceColumn": "Date",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Year",
                            "dataType": "int64",
                            "formatString": "0",
                            "sourceColumn": "Year",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Quarter",
                            "dataType": "string",
                            "sourceColumn": "Quarter",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Month",
                            "dataType": "int64",
                            "formatString": "0",
                            "sourceColumn": "Month",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "MonthName",
                            "dataType": "string",
                            "sortByColumn": "Month",
                            "sourceColumn": "MonthName",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "YearMonth",
                            "dataType": "string",
                            "sortByColumn": "YearMonthSort",
                            "sourceColumn": "YearMonth",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "YearMonthSort",
                            "dataType": "int64",
                            "isHidden": True,
                            "sourceColumn": "YearMonthSort",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "DayOfWeek",
                            "dataType": "string",
                            "sourceColumn": "DayOfWeek",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "IsWeekend",
                            "dataType": "int64",
                            "formatString": "0",
                            "sourceColumn": "IsWeekend",
                            "summarizeBy": "none"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Date",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    StartDate = #date(2016, 1, 1),",
                                    "    EndDate = #date(2019, 12, 31),",
                                    "    DayCount = Duration.Days(EndDate - StartDate) + 1,",
                                    "    DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),",
                                    "    #\"Converted to Table\" = Table.FromList(DateList, Splitter.SplitByNothing(), {\"Date\"}, null, ExtraValues.Error),",
                                    "    #\"Changed Type\" = Table.TransformColumnTypes(#\"Converted to Table\", {{\"Date\", type date}}),",
                                    "    #\"Added Year\" = Table.AddColumn(#\"Changed Type\", \"Year\", each Date.Year([Date]), Int64.Type),",
                                    "    #\"Added Quarter\" = Table.AddColumn(#\"Added Year\", \"Quarter\", each \"Q\" & Text.From(Date.QuarterOfYear([Date])), type text),",
                                    "    #\"Added Month\" = Table.AddColumn(#\"Added Quarter\", \"Month\", each Date.Month([Date]), Int64.Type),",
                                    "    #\"Added Month Name\" = Table.AddColumn(#\"Added Month\", \"MonthName\", each Date.MonthName([Date]), type text),",
                                    "    #\"Added YearMonth\" = Table.AddColumn(#\"Added Month Name\", \"YearMonth\", each Date.ToText([Date], \"yyyy-MM\"), type text),",
                                    "    #\"Added YearMonthSort\" = Table.AddColumn(#\"Added YearMonth\", \"YearMonthSort\", each Date.Year([Date]) * 100 + Date.Month([Date]), Int64.Type),",
                                    "    #\"Added DayOfWeek\" = Table.AddColumn(#\"Added YearMonthSort\", \"DayOfWeek\", each Date.DayOfWeekName([Date]), type text),",
                                    "    #\"Added IsWeekend\" = Table.AddColumn(#\"Added DayOfWeek\", \"IsWeekend\", each if Date.DayOfWeek([Date], Day.Monday) >= 5 then 1 else 0, Int64.Type)",
                                    "in",
                                    "    #\"Added IsWeekend\""
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Dim_Product",
                    "columns": [
                        {
                            "name": "Product_ID",
                            "dataType": "int64",
                            "isKey": True,
                            "formatString": "0",
                            "sourceColumn": "Product_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Product_Name",
                            "dataType": "string",
                            "sourceColumn": "Product_Name",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Brand_ID",
                            "dataType": "int64",
                            "isHidden": True,
                            "formatString": "0",
                            "sourceColumn": "Brand_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Brand_Name",
                            "dataType": "string",
                            "sourceColumn": "Brand_Name",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Category_ID",
                            "dataType": "int64",
                            "isHidden": True,
                            "formatString": "0",
                            "sourceColumn": "Category_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Category_Name",
                            "dataType": "string",
                            "sourceColumn": "Category_Name",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Model_Year",
                            "dataType": "int64",
                            "formatString": "0",
                            "sourceColumn": "Model_Year",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "List_Price",
                            "dataType": "double",
                            "formatString": "$#,##0.00",
                            "sourceColumn": "List_Price",
                            "summarizeBy": "average"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Product",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    Source = Excel.Workbook(File.Contents(FilePath), null, true),",
                                    "    products_Table = Source{[Item=\"products\",Kind=\"Sheet\"]}[Data],",
                                    "    #\"Promoted Products\" = Table.PromoteHeaders(products_Table, [PromoteAllScalars=true]),",
                                    "    #\"Filtered Products\" = Table.SelectRows(#\"Promoted Products\", each [product_id] <> null and [product_id] <> \"\"),",
                                    "    brands_Table = Source{[Item=\"brands\",Kind=\"Sheet\"]}[Data],",
                                    "    #\"Promoted Brands\" = Table.PromoteHeaders(brands_Table, [PromoteAllScalars=true]),",
                                    "    #\"Filtered Brands\" = Table.SelectRows(#\"Promoted Brands\", each [brand_id] <> null and [brand_id] <> \"\"),",
                                    "    #\"Merged Brands\" = Table.NestedJoin(#\"Filtered Products\", {\"brand_id\"}, #\"Filtered Brands\", {\"brand_id\"}, \"BrandTable\", JoinKind.LeftOuter),",
                                    "    #\"Expanded Brands\" = Table.ExpandTableColumn(#\"Merged Brands\", \"BrandTable\", {\"brand_name\"}, {\"Brand_Name\"}),",
                                    "    categories_Table = Source{[Item=\"categories\",Kind=\"Sheet\"]}[Data],",
                                    "    #\"Promoted Categories\" = Table.PromoteHeaders(categories_Table, [PromoteAllScalars=true]),",
                                    "    #\"Filtered Categories\" = Table.SelectRows(#\"Promoted Categories\", each [category_id] <> null and [category_id] <> \"\"),",
                                    "    #\"Merged Categories\" = Table.NestedJoin(#\"Expanded Brands\", {\"category_id\"}, #\"Filtered Categories\", {\"category_id\"}, \"CatTable\", JoinKind.LeftOuter),",
                                    "    #\"Expanded Categories\" = Table.ExpandTableColumn(#\"Merged Categories\", \"CatTable\", {\"category_name\"}, {\"Category_Name\"}),",
                                    "    #\"Renamed Columns\" = Table.RenameColumns(#\"Expanded Categories\", {{\"product_id\", \"Product_ID\"}, {\"product_name\", \"Product_Name\"}, {\"brand_id\", \"Brand_ID\"}, {\"category_id\", \"Category_ID\"}, {\"model_year\", \"Model_Year\"}, {\"list_price\", \"List_Price\"}}),",
                                    "    #\"Changed Types\" = Table.TransformColumnTypes(#\"Renamed Columns\", {{\"Product_ID\", Int64.Type}, {\"Product_Name\", type text}, {\"Brand_ID\", Int64.Type}, {\"Brand_Name\", type text}, {\"Category_ID\", Int64.Type}, {\"Category_Name\", type text}, {\"Model_Year\", Int64.Type}, {\"List_Price\", type number}})",
                                    "in",
                                    "    #\"Changed Types\""
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Dim_Customer",
                    "columns": [
                        {
                            "name": "Customer_ID",
                            "dataType": "int64",
                            "isKey": True,
                            "formatString": "0",
                            "sourceColumn": "Customer_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Customer_Name",
                            "dataType": "string",
                            "sourceColumn": "Customer_Name",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Email",
                            "dataType": "string",
                            "sourceColumn": "Email",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Phone",
                            "dataType": "string",
                            "sourceColumn": "Phone",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Street",
                            "dataType": "string",
                            "sourceColumn": "Street",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "City",
                            "dataType": "string",
                            "dataCategory": "City",
                            "sourceColumn": "City",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "State",
                            "dataType": "string",
                            "dataCategory": "StateOrProvince",
                            "sourceColumn": "State",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Zip_Code",
                            "dataType": "string",
                            "dataCategory": "PostalCode",
                            "sourceColumn": "Zip_Code",
                            "summarizeBy": "none"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Customer",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    Source = Excel.Workbook(File.Contents(FilePath), null, true),",
                                    "    customers_Table = Source{[Item=\"customers\",Kind=\"Sheet\"]}[Data],",
                                    "    #\"Promoted Headers\" = Table.PromoteHeaders(customers_Table, [PromoteAllScalars=true]),",
                                    "    #\"Filtered Blank Rows\" = Table.SelectRows(#\"Promoted Headers\", each [customer_id] <> null and [customer_id] <> \"\"),",
                                    "    #\"Added FullName\" = Table.AddColumn(#\"Filtered Blank Rows\", \"Customer_Name\", each [first_name] & \" \" & [last_name], type text),",
                                    "    #\"Renamed Columns\" = Table.RenameColumns(#\"Added FullName\", {{\"customer_id\", \"Customer_ID\"}, {\"email\", \"Email\"}, {\"phone\", \"Phone\"}, {\"street\", \"Street\"}, {\"city\", \"City\"}, {\"state\", \"State\"}, {\"zip_code\", \"Zip_Code\"}}),",
                                    "    #\"Changed Types\" = Table.TransformColumnTypes(#\"Renamed Columns\", {{\"Customer_ID\", Int64.Type}, {\"Customer_Name\", type text}, {\"Email\", type text}, {\"Phone\", type text}, {\"Street\", type text}, {\"City\", type text}, {\"State\", type text}, {\"Zip_Code\", type text}})",
                                    "in",
                                    "    #\"Changed Types\""
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Dim_Store",
                    "columns": [
                        {
                            "name": "Store_ID",
                            "dataType": "int64",
                            "isKey": True,
                            "formatString": "0",
                            "sourceColumn": "Store_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Store_Name",
                            "dataType": "string",
                            "sourceColumn": "Store_Name",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Phone",
                            "dataType": "string",
                            "sourceColumn": "Phone",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Email",
                            "dataType": "string",
                            "sourceColumn": "Email",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "City",
                            "dataType": "string",
                            "dataCategory": "City",
                            "sourceColumn": "City",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "State",
                            "dataType": "string",
                            "dataCategory": "StateOrProvince",
                            "sourceColumn": "State",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Zip_Code",
                            "dataType": "string",
                            "dataCategory": "PostalCode",
                            "sourceColumn": "Zip_Code",
                            "summarizeBy": "none"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Store",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    Source = Excel.Workbook(File.Contents(FilePath), null, true),",
                                    "    stores_Table = Source{[Item=\"stores\",Kind=\"Sheet\"]}[Data],",
                                    "    #\"Promoted Headers\" = Table.PromoteHeaders(stores_Table, [PromoteAllScalars=true]),",
                                    "    #\"Filtered Blank Rows\" = Table.SelectRows(#\"Promoted Headers\", each [store_id] <> null and [store_id] <> \"\"),",
                                    "    #\"Renamed Columns\" = Table.RenameColumns(#\"Filtered Blank Rows\", {{\"store_id\", \"Store_ID\"}, {\"store_name\", \"Store_Name\"}, {\"phone\", \"Phone\"}, {\"email\", \"Email\"}, {\"street\", \"Street\"}, {\"city\", \"City\"}, {\"state\", \"State\"}, {\"zip_code\", \"Zip_Code\"}}),",
                                    "    #\"Changed Types\" = Table.TransformColumnTypes(#\"Renamed Columns\", {{\"Store_ID\", Int64.Type}, {\"Store_Name\", type text}, {\"Phone\", type text}, {\"Email\", type text}, {\"Street\", type text}, {\"City\", type text}, {\"State\", type text}, {\"Zip_Code\", type text}})",
                                    "in",
                                    "    #\"Changed Types\""
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Dim_Staff",
                    "columns": [
                        {
                            "name": "Staff_ID",
                            "dataType": "int64",
                            "isKey": True,
                            "formatString": "0",
                            "sourceColumn": "Staff_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Staff_Name",
                            "dataType": "string",
                            "sourceColumn": "Staff_Name",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Email",
                            "dataType": "string",
                            "sourceColumn": "Email",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Phone",
                            "dataType": "string",
                            "sourceColumn": "Phone",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Active_Status",
                            "dataType": "int64",
                            "formatString": "0",
                            "sourceColumn": "Active_Status",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Store_ID",
                            "dataType": "int64",
                            "formatString": "0",
                            "sourceColumn": "Store_ID",
                            "summarizeBy": "none"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Staff",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    Source = Excel.Workbook(File.Contents(FilePath), null, true),",
                                    "    staffs_Table = Source{[Item=\"staffs\",Kind=\"Sheet\"]}[Data],",
                                    "    #\"Promoted Headers\" = Table.PromoteHeaders(staffs_Table, [PromoteAllScalars=true]),",
                                    "    #\"Filtered Blank Rows\" = Table.SelectRows(#\"Promoted Headers\", each [staff_id] <> null and [staff_id] <> \"\"),",
                                    "    #\"Added FullName\" = Table.AddColumn(#\"Filtered Blank Rows\", \"Staff_Name\", each [first_name] & \" \" & [last_name], type text),",
                                    "    #\"Renamed Columns\" = Table.RenameColumns(#\"Added FullName\", {{\"staff_id\", \"Staff_ID\"}, {\"email\", \"Email\"}, {\"phone\", \"Phone\"}, {\"active\", \"Active_Status\"}, {\"store_id\", \"Store_ID\"}}),",
                                    "    #\"Changed Types\" = Table.TransformColumnTypes(#\"Renamed Columns\", {{\"Staff_ID\", Int64.Type}, {\"Staff_Name\", type text}, {\"Email\", type text}, {\"Phone\", type text}, {\"Active_Status\", Int64.Type}, {\"Store_ID\", Int64.Type}})",
                                    "in",
                                    "    #\"Changed Types\""
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Sales",
                    "columns": [
                        {
                            "name": "Order_ID",
                            "dataType": "int64",
                            "formatString": "0",
                            "sourceColumn": "Order_ID",
                            "summarizeBy": "count"
                        },
                        {
                            "name": "Line_Item_ID",
                            "dataType": "int64",
                            "isHidden": True,
                            "formatString": "0",
                            "sourceColumn": "Line_Item_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Customer_ID",
                            "dataType": "int64",
                            "isHidden": True,
                            "formatString": "0",
                            "sourceColumn": "Customer_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Store_ID",
                            "dataType": "int64",
                            "isHidden": True,
                            "formatString": "0",
                            "sourceColumn": "Store_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Staff_ID",
                            "dataType": "int64",
                            "isHidden": True,
                            "formatString": "0",
                            "sourceColumn": "Staff_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Product_ID",
                            "dataType": "int64",
                            "isHidden": True,
                            "formatString": "0",
                            "sourceColumn": "Product_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Order_Date",
                            "dataType": "dateTime",
                            "formatString": "yyyy-MM-dd",
                            "sourceColumn": "Order_Date",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Required_Date",
                            "dataType": "dateTime",
                            "formatString": "yyyy-MM-dd",
                            "sourceColumn": "Required_Date",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Shipped_Date",
                            "dataType": "dateTime",
                            "formatString": "yyyy-MM-dd",
                            "sourceColumn": "Shipped_Date",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Order_Status",
                            "dataType": "string",
                            "sourceColumn": "Order_Status",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Quantity",
                            "dataType": "int64",
                            "formatString": "#,##0",
                            "sourceColumn": "Quantity",
                            "summarizeBy": "sum"
                        },
                        {
                            "name": "Unit_Price",
                            "dataType": "double",
                            "formatString": "$#,##0.00",
                            "sourceColumn": "Unit_Price",
                            "summarizeBy": "average"
                        },
                        {
                            "name": "Discount_Rate",
                            "dataType": "double",
                            "formatString": "0.0%",
                            "sourceColumn": "Discount_Rate",
                            "summarizeBy": "average"
                        },
                        {
                            "name": "Gross_Amount",
                            "dataType": "double",
                            "formatString": "$#,##0.00",
                            "sourceColumn": "Gross_Amount",
                            "summarizeBy": "sum"
                        },
                        {
                            "name": "Discount_Amount",
                            "dataType": "double",
                            "formatString": "$#,##0.00",
                            "sourceColumn": "Discount_Amount",
                            "summarizeBy": "sum"
                        },
                        {
                            "name": "Net_Amount",
                            "dataType": "double",
                            "formatString": "$#,##0.00",
                            "sourceColumn": "Net_Amount",
                            "summarizeBy": "sum"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Fact_Sales",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    Source = Excel.Workbook(File.Contents(FilePath), null, true),",
                                    "    order_items_Table = Source{[Item=\"order_items\",Kind=\"Sheet\"]}[Data],",
                                    "    #\"Promoted Items\" = Table.PromoteHeaders(order_items_Table, [PromoteAllScalars=true]),",
                                    "    #\"Filtered Items\" = Table.SelectRows(#\"Promoted Items\", each [order_id] <> null and [order_id] <> \"\"),",
                                    "    orders_Table = Source{[Item=\"orders\",Kind=\"Sheet\"]}[Data],",
                                    "    #\"Promoted Orders\" = Table.PromoteHeaders(orders_Table, [PromoteAllScalars=true]),",
                                    "    #\"Filtered Orders\" = Table.SelectRows(#\"Promoted Orders\", each [order_id] <> null and [order_id] <> \"\"),",
                                    "    #\"Merged Orders\" = Table.NestedJoin(#\"Filtered Items\", {\"order_id\"}, #\"Filtered Orders\", {\"order_id\"}, \"OrderHeader\", JoinKind.Inner),",
                                    "    #\"Expanded Orders\" = Table.ExpandTableColumn(#\"Merged Orders\", \"OrderHeader\", {\"customer_id\", \"order_status\", \"order_date\", \"required_date\", \"shipped_date\", \"store_id\", \"staff_id\"}, {\"Customer_ID\", \"Order_Status_Code\", \"Order_Date\", \"Required_Date\", \"Shipped_Date\", \"Store_ID\", \"Staff_ID\"}),",
                                    "    #\"Added Status\" = Table.AddColumn(#\"Expanded Orders\", \"Order_Status\", each if [Order_Status_Code] = 1 then \"Pending\" else if [Order_Status_Code] = 2 then \"Processing\" else if [Order_Status_Code] = 3 then \"Rejected\" else if [Order_Status_Code] = 4 then \"Completed\" else \"Unknown\", type text),",
                                    "    #\"Added Gross\" = Table.AddColumn(#\"Added Status\", \"Gross_Amount\", each [quantity] * [list_price], type number),",
                                    "    #\"Added Disc\" = Table.AddColumn(#\"Added Gross\", \"Discount_Amount\", each [Gross_Amount] * [discount], type number),",
                                    "    #\"Added Net\" = Table.AddColumn(#\"Added Disc\", \"Net_Amount\", each [Gross_Amount] - [Discount_Amount], type number),",
                                    "    #\"Renamed Cols\" = Table.RenameColumns(#\"Added Net\", {{\"order_id\", \"Order_ID\"}, {\"item_id\", \"Line_Item_ID\"}, {\"product_id\", \"Product_ID\"}, {\"quantity\", \"Quantity\"}, {\"list_price\", \"Unit_Price\"}, {\"discount\", \"Discount_Rate\"}}),",
                                    "    #\"Changed Types\" = Table.TransformColumnTypes(#\"Renamed Cols\", {{\"Order_ID\", Int64.Type}, {\"Line_Item_ID\", Int64.Type}, {\"Product_ID\", Int64.Type}, {\"Customer_ID\", Int64.Type}, {\"Store_ID\", Int64.Type}, {\"Staff_ID\", Int64.Type}, {\"Order_Status\", type text}, {\"Order_Date\", type date}, {\"Required_Date\", type date}, {\"Shipped_Date\", type date}, {\"Quantity\", Int64.Type}, {\"Unit_Price\", type number}, {\"Discount_Rate\", type number}, {\"Gross_Amount\", type number}, {\"Discount_Amount\", type number}, {\"Net_Amount\", type number}})",
                                    "in",
                                    "    #\"Changed Types\""
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Inventory",
                    "columns": [
                        {
                            "name": "Store_ID",
                            "dataType": "int64",
                            "isHidden": True,
                            "formatString": "0",
                            "sourceColumn": "Store_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Product_ID",
                            "dataType": "int64",
                            "isHidden": True,
                            "formatString": "0",
                            "sourceColumn": "Product_ID",
                            "summarizeBy": "none"
                        },
                        {
                            "name": "Quantity_In_Stock",
                            "dataType": "int64",
                            "formatString": "#,##0",
                            "sourceColumn": "Quantity_In_Stock",
                            "summarizeBy": "sum"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Fact_Inventory",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    Source = Excel.Workbook(File.Contents(FilePath), null, true),",
                                    "    stocks_Table = Source{[Item=\"stocks\",Kind=\"Sheet\"]}[Data],",
                                    "    #\"Promoted Headers\" = Table.PromoteHeaders(stocks_Table, [PromoteAllScalars=true]),",
                                    "    #\"Filtered Blank Rows\" = Table.SelectRows(#\"Promoted Headers\", each [store_id] <> null and [store_id] <> \"\"),",
                                    "    #\"Renamed Columns\" = Table.RenameColumns(#\"Filtered Blank Rows\", {{\"store_id\", \"Store_ID\"}, {\"product_id\", \"Product_ID\"}, {\"quantity\", \"Quantity_In_Stock\"}}),",
                                    "    #\"Changed Types\" = Table.TransformColumnTypes(#\"Renamed Columns\", {{\"Store_ID\", Int64.Type}, {\"Product_ID\", Int64.Type}, {\"Quantity_In_Stock\", Int64.Type}})",
                                    "in",
                                    "    #\"Changed Types\""
                                ]
                            }
                        }
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "rel_Sales_Customer",
                    "fromTable": "Fact_Sales",
                    "fromColumn": "Customer_ID",
                    "toTable": "Dim_Customer",
                    "toColumn": "Customer_ID"
                },
                {
                    "name": "rel_Sales_Product",
                    "fromTable": "Fact_Sales",
                    "fromColumn": "Product_ID",
                    "toTable": "Dim_Product",
                    "toColumn": "Product_ID"
                },
                {
                    "name": "rel_Sales_Store",
                    "fromTable": "Fact_Sales",
                    "fromColumn": "Store_ID",
                    "toTable": "Dim_Store",
                    "toColumn": "Store_ID"
                },
                {
                    "name": "rel_Sales_Staff",
                    "fromTable": "Fact_Sales",
                    "fromColumn": "Staff_ID",
                    "toTable": "Dim_Staff",
                    "toColumn": "Staff_ID"
                },
                {
                    "name": "rel_Sales_OrderDate",
                    "fromTable": "Fact_Sales",
                    "fromColumn": "Order_Date",
                    "toTable": "Dim_Date",
                    "toColumn": "Date"
                },
                {
                    "name": "rel_Sales_ShippedDate",
                    "isActive": False,
                    "fromTable": "Fact_Sales",
                    "fromColumn": "Shipped_Date",
                    "toTable": "Dim_Date",
                    "toColumn": "Date"
                },
                {
                    "name": "rel_Sales_RequiredDate",
                    "isActive": False,
                    "fromTable": "Fact_Sales",
                    "fromColumn": "Required_Date",
                    "toTable": "Dim_Date",
                    "toColumn": "Date"
                },
                {
                    "name": "rel_Inventory_Store",
                    "fromTable": "Fact_Inventory",
                    "fromColumn": "Store_ID",
                    "toTable": "Dim_Store",
                    "toColumn": "Store_ID"
                },
                {
                    "name": "rel_Inventory_Product",
                    "fromTable": "Fact_Inventory",
                    "fromColumn": "Product_ID",
                    "toTable": "Dim_Product",
                    "toColumn": "Product_ID"
                }
            ],
            "annotations": [
                {
                    "name": "__PBI_TimeIntelligenceEnabled",
                    "value": "0"
                },
                {
                    "name": "PBIDesktopVersion",
                    "value": "2.138.1452.0 (24.11)"
                }
            ]
        }
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(model_bim, f, indent=2)
    print(f"Successfully created: {output_path}")

if __name__ == "__main__":
    generate_model_bim()
