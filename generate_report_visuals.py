#!/usr/bin/env python3
"""
Power BI Visual Containers Generator for PBIP (report.json)
Generates complete visual dashboards for all 4 pages:
1. Executive Overview
2. Products & Inventory
3. Customers & Geography
4. Fulfillment & Operations
"""

import json
import secrets
import shutil
import os

def random_id():
    return secrets.token_hex(10)

def make_card(x, y, width, height, measure_name, z=1000):
    v_id = random_id()
    config_obj = {
        "name": v_id,
        "layouts": [{
            "id": 0,
            "position": {
                "x": x,
                "y": y,
                "z": z,
                "width": width,
                "height": height,
                "tabOrder": z
            }
        }],
        "singleVisual": {
            "visualType": "card",
            "projections": {
                "Values": [{
                    "queryRef": f"_Measures.{measure_name}"
                }]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{
                    "Name": "m",
                    "Entity": "_Measures",
                    "Type": 0
                }],
                "Select": [{
                    "Measure": {
                        "Expression": {
                            "SourceRef": {
                                "Source": "m"
                            }
                        },
                        "Property": measure_name
                    },
                    "Name": f"_Measures.{measure_name}"
                }]
            }
        }
    }
    
    return {
        "x": x,
        "y": y,
        "z": z,
        "width": width,
        "height": height,
        "config": json.dumps(config_obj, ensure_ascii=False)
    }

def make_bar_chart(x, y, width, height, cat_table, cat_col, measure_name, title=None, z=1000):
    v_id = random_id()
    config_obj = {
        "name": v_id,
        "layouts": [{
            "id": 0,
            "position": {
                "x": x,
                "y": y,
                "z": z,
                "width": width,
                "height": height,
                "tabOrder": z
            }
        }],
        "singleVisual": {
            "visualType": "clusteredBarChart",
            "projections": {
                "Category": [{
                    "queryRef": f"{cat_table}.{cat_col}",
                    "active": True
                }],
                "Y": [{
                    "queryRef": f"_Measures.{measure_name}"
                }]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {
                        "Name": "c",
                        "Entity": cat_table,
                        "Type": 0
                    },
                    {
                        "Name": "m",
                        "Entity": "_Measures",
                        "Type": 0
                    }
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {
                                "SourceRef": {
                                    "Source": "c"
                                }
                            },
                            "Property": cat_col
                        },
                        "Name": f"{cat_table}.{cat_col}"
                    },
                    {
                        "Measure": {
                            "Expression": {
                                "SourceRef": {
                                    "Source": "m"
                                }
                            },
                            "Property": measure_name
                        },
                        "Name": f"_Measures.{measure_name}"
                    }
                ],
                "OrderBy": [
                    {
                        "Direction": 2,
                        "Expression": {
                            "Measure": {
                                "Expression": {
                                    "SourceRef": {
                                        "Source": "m"
                                    }
                                },
                                "Property": measure_name
                            }
                        }
                    }
                ]
            }
        }
    }
    
    return {
        "x": x,
        "y": y,
        "z": z,
        "width": width,
        "height": height,
        "config": json.dumps(config_obj, ensure_ascii=False)
    }

def make_line_chart(x, y, width, height, date_table, date_col, measure_name, z=1000):
    v_id = random_id()
    config_obj = {
        "name": v_id,
        "layouts": [{
            "id": 0,
            "position": {
                "x": x,
                "y": y,
                "z": z,
                "width": width,
                "height": height,
                "tabOrder": z
            }
        }],
        "singleVisual": {
            "visualType": "lineChart",
            "projections": {
                "Category": [{
                    "queryRef": f"{date_table}.{date_col}",
                    "active": True
                }],
                "Y": [{
                    "queryRef": f"_Measures.{measure_name}"
                }]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {
                        "Name": "d",
                        "Entity": date_table,
                        "Type": 0
                    },
                    {
                        "Name": "m",
                        "Entity": "_Measures",
                        "Type": 0
                    }
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {
                                "SourceRef": {
                                    "Source": "d"
                                }
                            },
                            "Property": date_col
                        },
                        "Name": f"{date_table}.{date_col}"
                    },
                    {
                        "Measure": {
                            "Expression": {
                                "SourceRef": {
                                    "Source": "m"
                                }
                            },
                            "Property": measure_name
                        },
                        "Name": f"_Measures.{measure_name}"
                    }
                ]
            }
        }
    }
    
    return {
        "x": x,
        "y": y,
        "z": z,
        "width": width,
        "height": height,
        "config": json.dumps(config_obj, ensure_ascii=False)
    }

def make_table(x, y, width, height, columns, measures, z=1000):
    v_id = random_id()
    projections = []
    from_list = []
    select_list = []
    
    tables_seen = {}
    
    for tbl, col in columns:
        if tbl not in tables_seen:
            alias = f"t{len(tables_seen)}"
            tables_seen[tbl] = alias
            from_list.append({"Name": alias, "Entity": tbl, "Type": 0})
        alias = tables_seen[tbl]
        q_ref = f"{tbl}.{col}"
        projections.append({"queryRef": q_ref})
        select_list.append({
            "Column": {
                "Expression": {
                    "SourceRef": {
                        "Source": alias
                    }
                },
                "Property": col
            },
            "Name": q_ref
        })
        
    if measures:
        if "_Measures" not in tables_seen:
            alias = "m"
            tables_seen["_Measures"] = alias
            from_list.append({"Name": alias, "Entity": "_Measures", "Type": 0})
        alias = tables_seen["_Measures"]
        for m in measures:
            q_ref = f"_Measures.{m}"
            projections.append({"queryRef": q_ref})
            select_list.append({
                "Measure": {
                    "Expression": {
                        "SourceRef": {
                            "Source": alias
                        }
                    },
                    "Property": m
                },
                "Name": q_ref
            })
            
    config_obj = {
        "name": v_id,
        "layouts": [{
            "id": 0,
            "position": {
                "x": x,
                "y": y,
                "z": z,
                "width": width,
                "height": height,
                "tabOrder": z
            }
        }],
        "singleVisual": {
            "visualType": "tableEx",
            "projections": {
                "Values": projections
            },
            "prototypeQuery": {
                "Version": 2,
                "From": from_list,
                "Select": select_list
            }
        }
    }
    
    return {
        "x": x,
        "y": y,
        "z": z,
        "width": width,
        "height": height,
        "config": json.dumps(config_obj, ensure_ascii=False)
    }

def generate_all_dashboards(report_json_path):
    # Backup existing
    if os.path.exists(report_json_path):
        shutil.copy(report_json_path, report_json_path + ".bak")
        
    with open(report_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Build sections
    # -------------------------------------------------------------
    # 1. Executive Overview
    # -------------------------------------------------------------
    sec1_visuals = [
        # Top KPI cards row (5 cards)
        make_card(20, 20, 230, 95, "Total Net Revenue", z=1000),
        make_card(270, 20, 230, 95, "Total Orders", z=1010),
        make_card(520, 20, 230, 95, "Average Order Value", z=1020),
        make_card(770, 20, 230, 95, "Total Units Sold", z=1030),
        make_card(1020, 20, 240, 95, "Total Active Customers", z=1040),
        
        # Middle row
        # Left: Monthly Revenue Trend
        make_line_chart(20, 130, 730, 310, "Dim_Date", "YearMonth", "Total Net Revenue", z=2000),
        # Right: Revenue by Category
        make_bar_chart(770, 130, 490, 310, "Dim_Product", "Category_Name", "Total Net Revenue", z=2010),
        
        # Bottom row
        # Left: Top Selling Brands
        make_bar_chart(20, 460, 600, 240, "Dim_Product", "Brand_Name", "Total Net Revenue", z=3000),
        # Right: Store Contribution Table
        make_table(640, 460, 620, 240, [("Dim_Store", "Store_Name"), ("Dim_Store", "State")], ["Total Net Revenue", "Total Orders"], z=3010)
    ]
    
    # -------------------------------------------------------------
    # 2. Products & Inventory
    # -------------------------------------------------------------
    sec2_visuals = [
        # KPI Cards (4 cards)
        make_card(20, 20, 290, 95, "Total Stock Quantity", z=1000),
        make_card(330, 20, 290, 95, "Total Stock Value", z=1010),
        make_card(640, 20, 290, 95, "Total Units Sold", z=1020),
        make_card(950, 20, 310, 95, "Total Net Revenue", z=1030),
        
        # Middle row
        # Left: Stock by Product Category
        make_bar_chart(20, 130, 600, 310, "Dim_Product", "Category_Name", "Total Stock Quantity", z=2000),
        # Right: Stock by Store
        make_bar_chart(640, 130, 620, 310, "Dim_Store", "Store_Name", "Total Stock Quantity", z=2010),
        
        # Bottom Table: Product Inventory Health
        make_table(20, 460, 1240, 240, 
                   [("Dim_Product", "Product_Name"), ("Dim_Product", "Brand_Name"), ("Dim_Product", "Category_Name")],
                   ["Total Stock Quantity", "Total Units Sold", "Total Net Revenue"], z=3000)
    ]
    
    # -------------------------------------------------------------
    # 3. Customers & Geography
    # -------------------------------------------------------------
    sec3_visuals = [
        # KPI Cards (4 cards)
        make_card(20, 20, 290, 95, "Total Active Customers", z=1000),
        make_card(330, 20, 290, 95, "Total Net Revenue", z=1010),
        make_card(640, 20, 290, 95, "Average Order Value", z=1020),
        make_card(950, 20, 310, 95, "Revenue Per Customer", z=1030),
        
        # Middle row
        # Left: Revenue by State
        make_bar_chart(20, 130, 600, 310, "Dim_Customer", "State", "Total Net Revenue", z=2000),
        # Right: Staff Leaderboard
        make_bar_chart(640, 130, 620, 310, "Dim_Staff", "Staff_Name", "Total Net Revenue", z=2010),
        
        # Bottom Table: Customer Top Buyers
        make_table(20, 460, 1240, 240,
                   [("Dim_Customer", "Customer_Name"), ("Dim_Customer", "City"), ("Dim_Customer", "State")],
                   ["Total Net Revenue", "Total Orders"], z=3000)
    ]
    
    # -------------------------------------------------------------
    # 4. Fulfillment & Operations
    # -------------------------------------------------------------
    sec4_visuals = [
        # KPI Cards (4 cards)
        make_card(20, 20, 290, 95, "Total Orders", z=1000),
        make_card(330, 20, 290, 95, "Total Units Sold", z=1010),
        make_card(640, 20, 290, 95, "Total Gross Revenue", z=1020),
        make_card(950, 20, 310, 95, "Average Discount %", z=1030),
        
        # Middle row: Order Status Breakdown
        make_bar_chart(20, 130, 600, 310, "Fact_Sales", "Order_Status", "Total Orders", z=2000),
        # Middle right: Store Sales & Volume
        make_bar_chart(640, 130, 620, 310, "Dim_Store", "Store_Name", "Total Orders", z=2010),
        
        # Bottom Table: Operations Store Performance
        make_table(20, 460, 1240, 240,
                   [("Dim_Store", "Store_Name"), ("Dim_Store", "City"), ("Dim_Store", "State")],
                   ["Total Orders", "Total Net Revenue", "Average Discount %"], z=3000)
    ]
    
    data["sections"][0]["visualContainers"] = sec1_visuals
    data["sections"][1]["visualContainers"] = sec2_visuals
    data["sections"][2]["visualContainers"] = sec3_visuals
    data["sections"][3]["visualContainers"] = sec4_visuals
    
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated visual containers for all 4 pages in {report_json_path}!")
    print(f"Page 1 (Executive Overview): {len(sec1_visuals)} visuals")
    print(f"Page 2 (Products & Inventory): {len(sec2_visuals)} visuals")
    print(f"Page 3 (Customers & Geography): {len(sec3_visuals)} visuals")
    print(f"Page 4 (Fulfillment & Operations): {len(sec4_visuals)} visuals")

if __name__ == "__main__":
    rep_path = "BikeStore_Analytics.Report/report.json"
    generate_all_dashboards(rep_path)
