#!/usr/bin/env python3
"""
Power BI Project (.PBIP) Builder
Generates a complete Microsoft Power BI Project (PBIP) with TMDL Semantic Model,
Star Schema tables, relationships, DAX measures, and PBIR Report definition.
"""

import os
import json

def create_pbip_project(project_name="BikeStore_Analytics", base_dir="."):
    report_folder = os.path.join(base_dir, f"{project_name}.Report")
    model_folder = os.path.join(base_dir, f"{project_name}.SemanticModel")
    tmdl_dir = os.path.join(model_folder, "definition")
    tables_dir = os.path.join(tmdl_dir, "tables")
    cultures_dir = os.path.join(tmdl_dir, "cultures")
    
    os.makedirs(report_folder, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(cultures_dir, exist_ok=True)
    
    # 1. Root .pbip file
    pbip_content = {
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": f"{project_name}.Report"
                }
            }
        ],
        "settings": {
            "enableAutoRecovery": True
        }
    }
    with open(os.path.join(base_dir, f"{project_name}.pbip"), "w", encoding="utf-8") as f:
        json.dump(pbip_content, f, indent=2)
        
    # 2. Report/definition.pbir
    pbir_content = {
        "version": "1.0",
        "datasetReference": {
            "byPath": {
                "path": f"../{project_name}.SemanticModel"
            },
            "byConnection": None
        }
    }
    with open(os.path.join(report_folder, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump(pbir_content, f, indent=2)

    # 3. Report/report.json
    report_json_content = {
        "config": json.dumps({
            "version": "5.68",
            "themeCollection": {
                "baseTheme": {
                    "name": "CY25SU11",
                    "version": {"visual": "2.4.0", "report": "3.0.0", "page": "2.3.0"},
                    "type": 2
                }
            },
            "activeSectionIndex": 0,
            "settings": {
                "useNewFilterPaneExperience": True,
                "allowChangeFilterTypes": True
            }
        }),
        "layoutOptimization": 0,
        "sections": [
            {
                "displayName": "Executive Overview",
                "name": "Section_Executive_Overview",
                "width": 1280,
                "height": 720,
                "visualContainers": []
            },
            {
                "displayName": "Products & Inventory",
                "name": "Section_Products_Inventory",
                "width": 1280,
                "height": 720,
                "visualContainers": []
            },
            {
                "displayName": "Customers & Geography",
                "name": "Section_Customers_Geography",
                "width": 1280,
                "height": 720,
                "visualContainers": []
            },
            {
                "displayName": "Fulfillment & Operations",
                "name": "Section_Fulfillment_Operations",
                "width": 1280,
                "height": 720,
                "visualContainers": []
            }
        ]
    }
    with open(os.path.join(report_folder, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report_json_content, f, indent=2)
        
    # 4. SemanticModel/definition.pbism
    pbism_content = {
        "version": "1.0",
        "settings": {}
    }
    with open(os.path.join(model_folder, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump(pbism_content, f, indent=2)
        
    # 5. SemanticModel/definition/database.tmdl
    with open(os.path.join(tmdl_dir, "database.tmdl"), "w", encoding="utf-8") as f:
        f.write(f"""database {project_name}
	compatibilityLevel: 1567
""")

    # 6. SemanticModel/definition/model.tmdl
    with open(os.path.join(tmdl_dir, "model.tmdl"), "w", encoding="utf-8") as f:
        f.write("""model Model
	culture: en-US
	defaultPowerBIDataSourceVersion: powerBI_V3
	sourceQueryCulture: en-US
	dataAccessOptions
		legacyRedirects
		returnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 0

annotation PBIDesktopVersion = 2.138.1452.0 (24.11)

ref table _Measures
ref table Dim_Date
ref table Dim_Product
ref table Dim_Customer
ref table Dim_Store
ref table Dim_Staff
ref table Fact_Sales
ref table Fact_Inventory

ref cultureInfo en-US
""")

    # 7. SemanticModel/definition/cultures/en-US.tmdl
    with open(os.path.join(cultures_dir, "en-US.tmdl"), "w", encoding="utf-8") as f:
        f.write("""cultureInfo en-US
""")

    # 8. SemanticModel/definition/relationships.tmdl
    with open(os.path.join(tmdl_dir, "relationships.tmdl"), "w", encoding="utf-8") as f:
        f.write("""relationship rel_Sales_Customer
	fromColumn: Fact_Sales.Customer_ID
	toColumn: Dim_Customer.Customer_ID

relationship rel_Sales_Product
	fromColumn: Fact_Sales.Product_ID
	toColumn: Dim_Product.Product_ID

relationship rel_Sales_Store
	fromColumn: Fact_Sales.Store_ID
	toColumn: Dim_Store.Store_ID

relationship rel_Sales_Staff
	fromColumn: Fact_Sales.Staff_ID
	toColumn: Dim_Staff.Staff_ID

relationship rel_Sales_OrderDate
	fromColumn: Fact_Sales.Order_Date
	toColumn: Dim_Date.Date

relationship rel_Sales_ShippedDate
	isActive: false
	fromColumn: Fact_Sales.Shipped_Date
	toColumn: Dim_Date.Date

relationship rel_Sales_RequiredDate
	isActive: false
	fromColumn: Fact_Sales.Required_Date
	toColumn: Dim_Date.Date

relationship rel_Inventory_Store
	fromColumn: Fact_Inventory.Store_ID
	toColumn: Dim_Store.Store_ID

relationship rel_Inventory_Product
	fromColumn: Fact_Inventory.Product_ID
	toColumn: Dim_Product.Product_ID
""")

    # 9. TABLES
    # 9.1 _Measures Table
    with open(os.path.join(tables_dir, "_Measures.tmdl"), "w", encoding="utf-8") as f:
        f.write("""table _Measures
	lineageTag: 71e48810-7212-4214-bf03-882299100001

	measure 'Total Gross Revenue' = SUMX(Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[Unit_Price])
		formatString: "$#,##0"
		displayFolder: 01. Financial & Revenue KPIs
		lineageTag: 71e48810-7212-4214-bf03-882299100002

	measure 'Total Discount Amount' = SUMX(Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[Unit_Price] * Fact_Sales[Discount_Rate])
		formatString: "$#,##0"
		displayFolder: 01. Financial & Revenue KPIs
		lineageTag: 71e48810-7212-4214-bf03-882299100003

	measure 'Total Net Revenue' = [Total Gross Revenue] - [Total Discount Amount]
		formatString: "$#,##0"
		displayFolder: 01. Financial & Revenue KPIs
		lineageTag: 71e48810-7212-4214-bf03-882299100004

	measure 'Average Discount %' = DIVIDE([Total Discount Amount], [Total Gross Revenue], 0)
		formatString: 0.0%
		displayFolder: 01. Financial & Revenue KPIs
		lineageTag: 71e48810-7212-4214-bf03-882299100005

	measure 'Total Orders' = DISTINCTCOUNT(Fact_Sales[Order_ID])
		formatString: #,##0
		displayFolder: 02. Volume & Orders
		lineageTag: 71e48810-7212-4214-bf03-882299100006

	measure 'Total Units Sold' = SUM(Fact_Sales[Quantity])
		formatString: #,##0
		displayFolder: 02. Volume & Orders
		lineageTag: 71e48810-7212-4214-bf03-882299100007

	measure 'Average Order Value' = DIVIDE([Total Net Revenue], [Total Orders], BLANK())
		formatString: "$#,##0.00"
		displayFolder: 02. Volume & Orders
		lineageTag: 71e48810-7212-4214-bf03-882299100008

	measure 'Units Per Order' = DIVIDE([Total Units Sold], [Total Orders], BLANK())
		formatString: 0.0
		displayFolder: 02. Volume & Orders
		lineageTag: 71e48810-7212-4214-bf03-882299100009

	measure 'Net Revenue SPLY' = CALCULATE([Total Net Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))
		formatString: "$#,##0"
		displayFolder: 03. Time Intelligence (YoY / MoM / YTD)
		lineageTag: 71e48810-7212-4214-bf03-882299100010

	measure 'YoY Net Revenue Delta' = VAR CurrentRev = [Total Net Revenue] VAR PriorRev = [Net Revenue SPLY] RETURN IF(NOT ISBLANK(CurrentRev) && NOT ISBLANK(PriorRev), CurrentRev - PriorRev, BLANK())
		formatString: "$#,##0"
		displayFolder: 03. Time Intelligence (YoY / MoM / YTD)
		lineageTag: 71e48810-7212-4214-bf03-882299100011

	measure 'YoY Net Revenue Growth %' = VAR CurrentRev = [Total Net Revenue] VAR PriorRev = [Net Revenue SPLY] RETURN DIVIDE(CurrentRev - PriorRev, PriorRev, BLANK())
		formatString: "+0.0%;-0.0%;0.0%"
		displayFolder: 03. Time Intelligence (YoY / MoM / YTD)
		lineageTag: 71e48810-7212-4214-bf03-882299100012

	measure 'Net Revenue YTD' = CALCULATE([Total Net Revenue], DATESYTD(Dim_Date[Date]))
		formatString: "$#,##0"
		displayFolder: 03. Time Intelligence (YoY / MoM / YTD)
		lineageTag: 71e48810-7212-4214-bf03-882299100013

	measure 'Total Active Customers' = DISTINCTCOUNT(Fact_Sales[Customer_ID])
		formatString: #,##0
		displayFolder: 04. Customer Analytics
		lineageTag: 71e48810-7212-4214-bf03-882299100014

	measure 'Revenue Per Customer' = DIVIDE([Total Net Revenue], [Total Active Customers], BLANK())
		formatString: "$#,##0.00"
		displayFolder: 04. Customer Analytics
		lineageTag: 71e48810-7212-4214-bf03-882299100015

	measure 'Total Stock Quantity' = SUM(Fact_Inventory[Quantity_In_Stock])
		formatString: #,##0
		displayFolder: 05. Inventory & Supply Chain
		lineageTag: 71e48810-7212-4214-bf03-882299100016

	measure 'Total Stock Value' = SUMX(Fact_Inventory, Fact_Inventory[Quantity_In_Stock] * RELATED(Dim_Product[List_Price]))
		formatString: "$#,##0"
		displayFolder: 05. Inventory & Supply Chain
		lineageTag: 71e48810-7212-4214-bf03-882299100017

	column MeasurePlaceholder
		dataType: string
		isHidden
		lineageTag: 71e48810-7212-4214-bf03-882299100018
		summarizeBy: none
		sourceColumn: MeasurePlaceholder

	partition _Measures = m
		mode: import
		source = 
			let
				Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [MeasurePlaceholder = _t])
			in
				Source
""")

    # 9.2 Dim_Date Table
    with open(os.path.join(tables_dir, "Dim_Date.tmdl"), "w", encoding="utf-8") as f:
        f.write("""table Dim_Date
	lineageTag: 81e48810-7212-4214-bf03-882299200001
	dataCategory: Time

	column Date
		dataType: dateTime
		isKey
		formatString: yyyy-MM-dd
		lineageTag: 81e48810-7212-4214-bf03-882299200002
		summarizeBy: none
		sourceColumn: Date

	column Year
		dataType: int64
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299200003
		summarizeBy: none
		sourceColumn: Year

	column Quarter
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299200004
		summarizeBy: none
		sourceColumn: Quarter

	column Month
		dataType: int64
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299200005
		summarizeBy: none
		sourceColumn: Month

	column MonthName
		dataType: string
		sortByColumn: Month
		lineageTag: 81e48810-7212-4214-bf03-882299200006
		summarizeBy: none
		sourceColumn: MonthName

	column YearMonth
		dataType: string
		sortByColumn: YearMonthSort
		lineageTag: 81e48810-7212-4214-bf03-882299200007
		summarizeBy: none
		sourceColumn: YearMonth

	column YearMonthSort
		dataType: int64
		isHidden
		lineageTag: 81e48810-7212-4214-bf03-882299200008
		summarizeBy: none
		sourceColumn: YearMonthSort

	column DayOfWeek
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299200009
		summarizeBy: none
		sourceColumn: DayOfWeek

	column IsWeekend
		dataType: int64
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299200010
		summarizeBy: none
		sourceColumn: IsWeekend

	partition Dim_Date = m
		mode: import
		source = 
			let
				StartDate = #date(2016, 1, 1),
				EndDate = #date(2019, 12, 31),
				DayCount = Duration.Days(EndDate - StartDate) + 1,
				DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
				#"Converted to Table" = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
				#"Changed Type" = Table.TransformColumnTypes(#"Converted to Table", {{"Date", type date}}),
				#"Added Year" = Table.AddColumn(#"Changed Type", "Year", each Date.Year([Date]), Int64.Type),
				#"Added Quarter" = Table.AddColumn(#"Added Year", "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
				#"Added Month" = Table.AddColumn(#"Added Quarter", "Month", each Date.Month([Date]), Int64.Type),
				#"Added Month Name" = Table.AddColumn(#"Added Month", "MonthName", each Date.MonthName([Date]), type text),
				#"Added YearMonth" = Table.AddColumn(#"Added Month Name", "YearMonth", each Date.ToText([Date], "yyyy-MM"), type text),
				#"Added YearMonthSort" = Table.AddColumn(#"Added YearMonth", "YearMonthSort", each Date.Year([Date]) * 100 + Date.Month([Date]), Int64.Type),
				#"Added DayOfWeek" = Table.AddColumn(#"Added YearMonthSort", "DayOfWeek", each Date.DayOfWeekName([Date]), type text),
				#"Added IsWeekend" = Table.AddColumn(#"Added DayOfWeek", "IsWeekend", each if Date.DayOfWeek([Date], Day.Monday) >= 5 then 1 else 0, Int64.Type)
			in
				#"Added IsWeekend"
""")

    # 9.3 Dim_Product Table
    with open(os.path.join(tables_dir, "Dim_Product.tmdl"), "w", encoding="utf-8") as f:
        f.write("""table Dim_Product
	lineageTag: 81e48810-7212-4214-bf03-882299300001

	column Product_ID
		dataType: int64
		isKey
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299300002
		summarizeBy: none
		sourceColumn: Product_ID

	column Product_Name
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299300003
		summarizeBy: none
		sourceColumn: Product_Name

	column Brand_ID
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299300004
		summarizeBy: none
		sourceColumn: Brand_ID

	column Brand_Name
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299300005
		summarizeBy: none
		sourceColumn: Brand_Name

	column Category_ID
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299300006
		summarizeBy: none
		sourceColumn: Category_ID

	column Category_Name
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299300007
		summarizeBy: none
		sourceColumn: Category_Name

	column Model_Year
		dataType: int64
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299300008
		summarizeBy: none
		sourceColumn: Model_Year

	column List_Price
		dataType: double
		formatString: "$#,##0.00"
		lineageTag: 81e48810-7212-4214-bf03-882299300009
		summarizeBy: average
		sourceColumn: List_Price

	partition Dim_Product = m
		mode: import
		source = 
			let
				Source = Excel.Workbook(File.Contents("BikeStore.xlsx"), null, true),
				products_Table = Source{[Item="products",Kind="Table"]}[Data],
				#"Promoted Products" = Table.PromoteHeaders(products_Table, [PromoteAllScalars=true]),
				brands_Table = Source{[Item="brands",Kind="Table"]}[Data],
				#"Promoted Brands" = Table.PromoteHeaders(brands_Table, [PromoteAllScalars=true]),
				#"Merged Brands" = Table.NestedJoin(#"Promoted Products", {"brand_id"}, #"Promoted Brands", {"brand_id"}, "BrandTable", JoinKind.LeftOuter),
				#"Expanded Brands" = Table.ExpandTableColumn(#"Merged Brands", "BrandTable", {"brand_name"}, {"Brand_Name"}),
				categories_Table = Source{[Item="categories",Kind="Table"]}[Data],
				#"Promoted Categories" = Table.PromoteHeaders(categories_Table, [PromoteAllScalars=true]),
				#"Merged Categories" = Table.NestedJoin(#"Expanded Brands", {"category_id"}, #"Promoted Categories", {"category_id"}, "CatTable", JoinKind.LeftOuter),
				#"Expanded Categories" = Table.ExpandTableColumn(#"Merged Categories", "CatTable", {"category_name"}, {"Category_Name"}),
				#"Renamed Columns" = Table.RenameColumns(#"Expanded Categories", {{"product_id", "Product_ID"}, {"product_name", "Product_Name"}, {"brand_id", "Brand_ID"}, {"category_id", "Category_ID"}, {"model_year", "Model_Year"}, {"list_price", "List_Price"}}),
				#"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns", {{"Product_ID", Int64.Type}, {"Product_Name", type text}, {"Brand_ID", Int64.Type}, {"Brand_Name", type text}, {"Category_ID", Int64.Type}, {"Category_Name", type text}, {"Model_Year", Int64.Type}, {"List_Price", type number}})
			in
				#"Changed Types"
""")

    # 9.4 Dim_Customer Table
    with open(os.path.join(tables_dir, "Dim_Customer.tmdl"), "w", encoding="utf-8") as f:
        f.write("""table Dim_Customer
	lineageTag: 81e48810-7212-4214-bf03-882299400001

	column Customer_ID
		dataType: int64
		isKey
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299400002
		summarizeBy: none
		sourceColumn: Customer_ID

	column Customer_Name
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299400003
		summarizeBy: none
		sourceColumn: Customer_Name

	column Email
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299400004
		summarizeBy: none
		sourceColumn: Email

	column Phone
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299400005
		summarizeBy: none
		sourceColumn: Phone

	column Street
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299400006
		summarizeBy: none
		sourceColumn: Street

	column City
		dataType: string
		dataCategory: City
		lineageTag: 81e48810-7212-4214-bf03-882299400007
		summarizeBy: none
		sourceColumn: City

	column State
		dataType: string
		dataCategory: StateOrProvince
		lineageTag: 81e48810-7212-4214-bf03-882299400008
		summarizeBy: none
		sourceColumn: State

	column Zip_Code
		dataType: string
		dataCategory: PostalCode
		lineageTag: 81e48810-7212-4214-bf03-882299400009
		summarizeBy: none
		sourceColumn: Zip_Code

	partition Dim_Customer = m
		mode: import
		source = 
			let
				Source = Excel.Workbook(File.Contents("BikeStore.xlsx"), null, true),
				customers_Table = Source{[Item="customers",Kind="Table"]}[Data],
				#"Promoted Headers" = Table.PromoteHeaders(customers_Table, [PromoteAllScalars=true]),
				#"Added FullName" = Table.AddColumn(#"Promoted Headers", "Customer_Name", each [first_name] & " " & [last_name], type text),
				#"Renamed Columns" = Table.RenameColumns(#"Added FullName", {{"customer_id", "Customer_ID"}, {"email", "Email"}, {"phone", "Phone"}, {"street", "Street"}, {"city", "City"}, {"state", "State"}, {"zip_code", "Zip_Code"}}),
				#"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns", {{"Customer_ID", Int64.Type}, {"Customer_Name", type text}, {"Email", type text}, {"Phone", type text}, {"Street", type text}, {"City", type text}, {"State", type text}, {"Zip_Code", type text}})
			in
				#"Changed Types"
""")

    # 9.5 Dim_Store Table
    with open(os.path.join(tables_dir, "Dim_Store.tmdl"), "w", encoding="utf-8") as f:
        f.write("""table Dim_Store
	lineageTag: 81e48810-7212-4214-bf03-882299500001

	column Store_ID
		dataType: int64
		isKey
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299500002
		summarizeBy: none
		sourceColumn: Store_ID

	column Store_Name
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299500003
		summarizeBy: none
		sourceColumn: Store_Name

	column Phone
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299500004
		summarizeBy: none
		sourceColumn: Phone

	column Email
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299500005
		summarizeBy: none
		sourceColumn: Email

	column City
		dataType: string
		dataCategory: City
		lineageTag: 81e48810-7212-4214-bf03-882299500006
		summarizeBy: none
		sourceColumn: City

	column State
		dataType: string
		dataCategory: StateOrProvince
		lineageTag: 81e48810-7212-4214-bf03-882299500007
		summarizeBy: none
		sourceColumn: State

	column Zip_Code
		dataType: string
		dataCategory: PostalCode
		lineageTag: 81e48810-7212-4214-bf03-882299500008
		summarizeBy: none
		sourceColumn: Zip_Code

	partition Dim_Store = m
		mode: import
		source = 
			let
				Source = Excel.Workbook(File.Contents("BikeStore.xlsx"), null, true),
				stores_Table = Source{[Item="stores",Kind="Table"]}[Data],
				#"Promoted Headers" = Table.PromoteHeaders(stores_Table, [PromoteAllScalars=true]),
				#"Renamed Columns" = Table.RenameColumns(#"Promoted Headers", {{"store_id", "Store_ID"}, {"store_name", "Store_Name"}, {"phone", "Phone"}, {"email", "Email"}, {"street", "Street"}, {"city", "City"}, {"state", "State"}, {"zip_code", "Zip_Code"}}),
				#"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns", {{"Store_ID", Int64.Type}, {"Store_Name", type text}, {"Phone", type text}, {"Email", type text}, {"Street", type text}, {"City", type text}, {"State", type text}, {"Zip_Code", type text}})
			in
				#"Changed Types"
""")

    # 9.6 Dim_Staff Table
    with open(os.path.join(tables_dir, "Dim_Staff.tmdl"), "w", encoding="utf-8") as f:
        f.write("""table Dim_Staff
	lineageTag: 81e48810-7212-4214-bf03-882299600001

	column Staff_ID
		dataType: int64
		isKey
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299600002
		summarizeBy: none
		sourceColumn: Staff_ID

	column Staff_Name
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299600003
		summarizeBy: none
		sourceColumn: Staff_Name

	column Email
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299600004
		summarizeBy: none
		sourceColumn: Email

	column Phone
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299600005
		summarizeBy: none
		sourceColumn: Phone

	column Active_Status
		dataType: int64
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299600006
		summarizeBy: none
		sourceColumn: Active_Status

	column Store_ID
		dataType: int64
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299600007
		summarizeBy: none
		sourceColumn: Store_ID

	partition Dim_Staff = m
		mode: import
		source = 
			let
				Source = Excel.Workbook(File.Contents("BikeStore.xlsx"), null, true),
				staffs_Table = Source{[Item="staffs",Kind="Table"]}[Data],
				#"Promoted Headers" = Table.PromoteHeaders(staffs_Table, [PromoteAllScalars=true]),
				#"Added FullName" = Table.AddColumn(#"Promoted Headers", "Staff_Name", each [first_name] & " " & [last_name], type text),
				#"Renamed Columns" = Table.RenameColumns(#"Added FullName", {{"staff_id", "Staff_ID"}, {"email", "Email"}, {"phone", "Phone"}, {"active", "Active_Status"}, {"store_id", "Store_ID"}}),
				#"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns", {{"Staff_ID", Int64.Type}, {"Staff_Name", type text}, {"Email", type text}, {"Phone", type text}, {"Active_Status", Int64.Type}, {"Store_ID", Int64.Type}})
			in
				#"Changed Types"
""")

    # 9.7 Fact_Sales Table
    with open(os.path.join(tables_dir, "Fact_Sales.tmdl"), "w", encoding="utf-8") as f:
        f.write("""table Fact_Sales
	lineageTag: 81e48810-7212-4214-bf03-882299700001

	column Order_ID
		dataType: int64
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299700002
		summarizeBy: count
		sourceColumn: Order_ID

	column Line_Item_ID
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299700003
		summarizeBy: none
		sourceColumn: Line_Item_ID

	column Customer_ID
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299700004
		summarizeBy: none
		sourceColumn: Customer_ID

	column Store_ID
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299700005
		summarizeBy: none
		sourceColumn: Store_ID

	column Staff_ID
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299700006
		summarizeBy: none
		sourceColumn: Staff_ID

	column Product_ID
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299700007
		summarizeBy: none
		sourceColumn: Product_ID

	column Order_Date
		dataType: dateTime
		formatString: yyyy-MM-dd
		lineageTag: 81e48810-7212-4214-bf03-882299700008
		summarizeBy: none
		sourceColumn: Order_Date

	column Required_Date
		dataType: dateTime
		formatString: yyyy-MM-dd
		lineageTag: 81e48810-7212-4214-bf03-882299700009
		summarizeBy: none
		sourceColumn: Required_Date

	column Shipped_Date
		dataType: dateTime
		formatString: yyyy-MM-dd
		lineageTag: 81e48810-7212-4214-bf03-882299700010
		summarizeBy: none
		sourceColumn: Shipped_Date

	column Order_Status
		dataType: string
		lineageTag: 81e48810-7212-4214-bf03-882299700011
		summarizeBy: none
		sourceColumn: Order_Status

	column Quantity
		dataType: int64
		formatString: #,##0
		lineageTag: 81e48810-7212-4214-bf03-882299700012
		summarizeBy: sum
		sourceColumn: Quantity

	column Unit_Price
		dataType: double
		formatString: "$#,##0.00"
		lineageTag: 81e48810-7212-4214-bf03-882299700013
		summarizeBy: average
		sourceColumn: Unit_Price

	column Discount_Rate
		dataType: double
		formatString: 0.0%
		lineageTag: 81e48810-7212-4214-bf03-882299700014
		summarizeBy: average
		sourceColumn: Discount_Rate

	column Gross_Amount
		dataType: double
		formatString: "$#,##0.00"
		lineageTag: 81e48810-7212-4214-bf03-882299700015
		summarizeBy: sum
		sourceColumn: Gross_Amount

	column Discount_Amount
		dataType: double
		formatString: "$#,##0.00"
		lineageTag: 81e48810-7212-4214-bf03-882299700016
		summarizeBy: sum
		sourceColumn: Discount_Amount

	column Net_Amount
		dataType: double
		formatString: "$#,##0.00"
		lineageTag: 81e48810-7212-4214-bf03-882299700017
		summarizeBy: sum
		sourceColumn: Net_Amount

	partition Fact_Sales = m
		mode: import
		source = 
			let
				Source = Excel.Workbook(File.Contents("BikeStore.xlsx"), null, true),
				order_items_Table = Source{[Item="order_items",Kind="Table"]}[Data],
				#"Promoted Items" = Table.PromoteHeaders(order_items_Table, [PromoteAllScalars=true]),
				orders_Table = Source{[Item="orders",Kind="Table"]}[Data],
				#"Promoted Orders" = Table.PromoteHeaders(orders_Table, [PromoteAllScalars=true]),
				#"Merged Orders" = Table.NestedJoin(#"Promoted Items", {"order_id"}, #"Promoted Orders", {"order_id"}, "OrderHeader", JoinKind.Inner),
				#"Expanded Orders" = Table.ExpandTableColumn(#"Merged Orders", "OrderHeader", {"customer_id", "order_status", "order_date", "required_date", "shipped_date", "store_id", "staff_id"}, {"Customer_ID", "Order_Status_Code", "Order_Date", "Required_Date", "Shipped_Date", "Store_ID", "Staff_ID"}),
				#"Added Status" = Table.AddColumn(#"Expanded Orders", "Order_Status", each if [Order_Status_Code] = 1 then "Pending" else if [Order_Status_Code] = 2 then "Processing" else if [Order_Status_Code] = 3 then "Rejected" else if [Order_Status_Code] = 4 then "Completed" else "Unknown", type text),
				#"Added Gross" = Table.AddColumn(#"Added Status", "Gross_Amount", each [quantity] * [list_price], type number),
				#"Added Disc" = Table.AddColumn(#"Added Gross", "Discount_Amount", each [Gross_Amount] * [discount], type number),
				#"Added Net" = Table.AddColumn(#"Added Disc", "Net_Amount", each [Gross_Amount] - [Discount_Amount], type number),
				#"Renamed Cols" = Table.RenameColumns(#"Added Net", {{"order_id", "Order_ID"}, {"item_id", "Line_Item_ID"}, {"product_id", "Product_ID"}, {"quantity", "Quantity"}, {"list_price", "Unit_Price"}, {"discount", "Discount_Rate"}}),
				#"Changed Types" = Table.TransformColumnTypes(#"Renamed Cols", {{"Order_ID", Int64.Type}, {"Line_Item_ID", Int64.Type}, {"Product_ID", Int64.Type}, {"Customer_ID", Int64.Type}, {"Store_ID", Int64.Type}, {"Staff_ID", Int64.Type}, {"Order_Status", type text}, {"Order_Date", type date}, {"Required_Date", type date}, {"Shipped_Date", type date}, {"Quantity", Int64.Type}, {"Unit_Price", type number}, {"Discount_Rate", type number}, {"Gross_Amount", type number}, {"Discount_Amount", type number}, {"Net_Amount", type number}})
			in
				#"Changed Types"
""")

    # 9.8 Fact_Inventory Table
    with open(os.path.join(tables_dir, "Fact_Inventory.tmdl"), "w", encoding="utf-8") as f:
        f.write("""table Fact_Inventory
	lineageTag: 81e48810-7212-4214-bf03-882299800001

	column Store_ID
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299800002
		summarizeBy: none
		sourceColumn: Store_ID

	column Product_ID
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 81e48810-7212-4214-bf03-882299800003
		summarizeBy: none
		sourceColumn: Product_ID

	column Quantity_In_Stock
		dataType: int64
		formatString: #,##0
		lineageTag: 81e48810-7212-4214-bf03-882299800004
		summarizeBy: sum
		sourceColumn: Quantity_In_Stock

	partition Fact_Inventory = m
		mode: import
		source = 
			let
				Source = Excel.Workbook(File.Contents("BikeStore.xlsx"), null, true),
				stocks_Table = Source{[Item="stocks",Kind="Table"]}[Data],
				#"Promoted Headers" = Table.PromoteHeaders(stocks_Table, [PromoteAllScalars=true]),
				#"Renamed Columns" = Table.RenameColumns(#"Promoted Headers", {{"store_id", "Store_ID"}, {"product_id", "Product_ID"}, {"quantity", "Quantity_In_Stock"}}),
				#"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns", {{"Store_ID", Int64.Type}, {"Product_ID", Int64.Type}, {"Quantity_In_Stock", Int64.Type}})
			in
				#"Changed Types"
""")

    print(f"Successfully generated Power BI Project: {project_name}.pbip")

if __name__ == "__main__":
    create_pbip_project()
