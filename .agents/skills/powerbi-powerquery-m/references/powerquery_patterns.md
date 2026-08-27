# Power Query (M) Script Library & Design Patterns

## 1. Parameterized Data Source Setup

Always establish a parameter query `FilePath` so users can retarget their local files with one click:
```powerquery
let
    FilePath = "C:\Users\Username\Data\BikeStore.xlsx" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
in
    FilePath
```

---

## 2. Dynamic Calendar (Date Dimension) in M

This M query dynamically generates an enterprise Date dimension without external dependencies:

```powerquery
let
    // Configure Start and End Dates or pull dynamically from Fact table
    StartDate = #date(2016, 1, 1),
    EndDate = #date(2019, 12, 31),
    
    // Generate Day List
    DayCount = Duration.Days(EndDate - StartDate) + 1,
    DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    #"Converted to Table" = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    #"Changed Type" = Table.TransformColumnTypes(#"Converted to Table", {{"Date", type date}}),
    
    // Add Calendar Attributes
    #"Added Year" = Table.AddColumn(#"Changed Type", "Year", each Date.Year([Date]), Int64.Type),
    #"Added Quarter" = Table.AddColumn(#"Added Year", "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    #"Added Quarter Number" = Table.AddColumn(#"Added Quarter", "QuarterNumber", each Date.QuarterOfYear([Date]), Int64.Type),
    #"Added Month" = Table.AddColumn(#"Added Quarter Number", "Month", each Date.Month([Date]), Int64.Type),
    #"Added Month Name" = Table.AddColumn(#"Added Month", "MonthName", each Date.MonthName([Date]), type text),
    #"Added Month Short" = Table.AddColumn(#"Added Month Name", "MonthShort", each Date.ToText([Date], "MMM"), type text),
    #"Added Year-Month" = Table.AddColumn(#"Added Month Short", "YearMonth", each Date.ToText([Date], "yyyy-MM"), type text),
    #"Added Year-Month Sort" = Table.AddColumn(#"Added Year-Month", "YearMonthSort", each Date.Year([Date]) * 100 + Date.Month([Date]), Int64.Type),
    #"Added Day of Month" = Table.AddColumn(#"Added Year-Month Sort", "DayOfMonth", each Date.Day([Date]), Int64.Type),
    #"Added Day of Week" = Table.AddColumn(#"Added Day of Month", "DayOfWeek", each Date.DayOfWeekName([Date]), type text),
    #"Added Day of Week Num" = Table.AddColumn(#"Added Day of Week", "DayOfWeekNumber", each Date.DayOfWeek([Date], Day.Monday) + 1, Int64.Type),
    #"Added Is Weekend" = Table.AddColumn(#"Added Day of Week Num", "IsWeekend", each if Date.DayOfWeek([Date], Day.Monday) >= 5 then 1 else 0, Int64.Type),
    #"Added Is Past" = Table.AddColumn(#"Added Is Weekend", "IsPast", each if [Date] <= DateTime.Date(DateTime.LocalNow()) then 1 else 0, Int64.Type)
in
    #"Added Is Past"
```

---

## 3. Denormalized Product Dimension (`Dim_Product`)

Merge `products`, `brands`, and `categories` into a single Star Schema dimension in M.
> **Note**: Uses `Kind="Sheet"` and explicit blank row filtering to prevent null key propagation:

```powerquery
let
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    
    // 1. Load Products Sheet & Filter Blanks
    products_Table = Source{[Item="products", Kind="Sheet"]}[Data],
    #"Promoted Products" = Table.PromoteHeaders(products_Table, [PromoteAllScalars=true]),
    #"Filtered Products" = Table.SelectRows(#"Promoted Products", each [product_id] <> null and [product_id] <> ""),
    
    // 2. Load Brands Sheet & Filter Blanks
    brands_Table = Source{[Item="brands", Kind="Sheet"]}[Data],
    #"Promoted Brands" = Table.PromoteHeaders(brands_Table, [PromoteAllScalars=true]),
    #"Filtered Brands" = Table.SelectRows(#"Promoted Brands", each [brand_id] <> null and [brand_id] <> ""),
    
    // Merge Brands
    #"Merged Brands" = Table.NestedJoin(#"Filtered Products", {"brand_id"}, #"Filtered Brands", {"brand_id"}, "BrandTable", JoinKind.LeftOuter),
    #"Expanded Brands" = Table.ExpandTableColumn(#"Merged Brands", "BrandTable", {"brand_name"}, {"Brand_Name"}),
    
    // 3. Load Categories Sheet & Filter Blanks
    categories_Table = Source{[Item="categories", Kind="Sheet"]}[Data],
    #"Promoted Categories" = Table.PromoteHeaders(categories_Table, [PromoteAllScalars=true]),
    #"Filtered Categories" = Table.SelectRows(#"Promoted Categories", each [category_id] <> null and [category_id] <> ""),
    
    // Merge Categories
    #"Merged Categories" = Table.NestedJoin(#"Expanded Brands", {"category_id"}, #"Filtered Categories", {"category_id"}, "CatTable", JoinKind.LeftOuter),
    #"Expanded Categories" = Table.ExpandTableColumn(#"Merged Categories", "CatTable", {"category_name"}, {"Category_Name"}),
    
    // 4. Rename & Enforce Types
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Categories", {
        {"product_id", "Product_ID"},
        {"product_name", "Product_Name"},
        {"brand_id", "Brand_ID"},
        {"category_id", "Category_ID"},
        {"model_year", "Model_Year"},
        {"list_price", "List_Price"}
    }),
    #"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns", {
        {"Product_ID", Int64.Type},
        {"Product_Name", type text},
        {"Brand_ID", Int64.Type},
        {"Brand_Name", type text},
        {"Category_ID", Int64.Type},
        {"Category_Name", type text},
        {"Model_Year", Int64.Type},
        {"List_Price", type number}
    })
in
    #"Changed Types"
```

---

## 4. Customer Dimension (`Dim_Customer`)

```powerquery
let
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    customers_Table = Source{[Item="customers", Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(customers_Table, [PromoteAllScalars=true]),
    #"Filtered Blank Rows" = Table.SelectRows(#"Promoted Headers", each [customer_id] <> null and [customer_id] <> ""),
    #"Added FullName" = Table.AddColumn(#"Filtered Blank Rows", "Customer_Name", each [first_name] & " " & [last_name], type text),
    #"Renamed Columns" = Table.RenameColumns(#"Added FullName", {
        {"customer_id", "Customer_ID"},
        {"email", "Email"},
        {"phone", "Phone"},
        {"street", "Street"},
        {"city", "City"},
        {"state", "State"},
        {"zip_code", "Zip_Code"}
    }),
    #"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns", {
        {"Customer_ID", Int64.Type},
        {"Customer_Name", type text},
        {"Email", type text},
        {"Phone", type text},
        {"Street", type text},
        {"City", type text},
        {"State", type text},
        {"Zip_Code", type text}
    })
in
    #"Changed Types"
```

---

## 5. Sales Fact Table (`Fact_Sales`)

Combining `orders` and `order_items` into a clean transactional grain fact table:

```powerquery
let
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    
    // 1. Load Order Items & Filter Blanks
    order_items_Table = Source{[Item="order_items", Kind="Sheet"]}[Data],
    #"Promoted Items" = Table.PromoteHeaders(order_items_Table, [PromoteAllScalars=true]),
    #"Filtered Items" = Table.SelectRows(#"Promoted Items", each [order_id] <> null and [order_id] <> ""),
    
    // 2. Load Orders & Filter Blanks
    orders_Table = Source{[Item="orders", Kind="Sheet"]}[Data],
    #"Promoted Orders" = Table.PromoteHeaders(orders_Table, [PromoteAllScalars=true]),
    #"Filtered Orders" = Table.SelectRows(#"Promoted Orders", each [order_id] <> null and [order_id] <> ""),
    
    // 3. Join Header to Items
    #"Merged Orders" = Table.NestedJoin(#"Filtered Items", {"order_id"}, #"Filtered Orders", {"order_id"}, "OrderHeader", JoinKind.Inner),
    #"Expanded Orders" = Table.ExpandTableColumn(#"Merged Orders", "OrderHeader", 
        {"customer_id", "order_status", "order_date", "required_date", "shipped_date", "store_id", "staff_id"}, 
        {"Customer_ID", "Order_Status_Code", "Order_Date", "Required_Date", "Shipped_Date", "Store_ID", "Staff_ID"}
    ),
    
    // 4. Transform Status & Line Metrics
    #"Added Status" = Table.AddColumn(#"Expanded Orders", "Order_Status", each 
        if [Order_Status_Code] = 1 then "Pending" 
        else if [Order_Status_Code] = 2 then "Processing" 
        else if [Order_Status_Code] = 3 then "Rejected" 
        else if [Order_Status_Code] = 4 then "Completed" 
        else "Unknown", type text
    ),
    #"Added Gross" = Table.AddColumn(#"Added Status", "Gross_Amount", each [quantity] * [list_price], type number),
    #"Added Discount Amt" = Table.AddColumn(#"Added Gross", "Discount_Amount", each [Gross_Amount] * [discount], type number),
    #"Added Net" = Table.AddColumn(#"Added Discount Amt", "Net_Amount", each [Gross_Amount] - [Discount_Amount], type number),
    #"Added Days to Ship" = Table.AddColumn(#"Added Net", "Days_To_Ship", each 
        if [Shipped_Date] = null or [Shipped_Date] = "NULL" then null 
        else Duration.Days(Date.From([Shipped_Date]) - Date.From([Order_Date])), Int64.Type
    ),
    #"Added Key" = Table.AddColumn(#"Added Days to Ship", "Order_Item_Composite_Key", each Text.From([order_id]) & "-" & Text.From([item_id]), type text),
    
    // 5. Rename & Type
    #"Renamed Columns" = Table.RenameColumns(#"Added Key", {
        {"order_id", "Order_ID"},
        {"item_id", "Item_ID"},
        {"product_id", "Product_ID"},
        {"quantity", "Quantity"},
        {"list_price", "Unit_Price"},
        {"discount", "Discount_Rate"}
    }),
    #"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns", {
        {"Order_Item_Composite_Key", type text},
        {"Order_ID", Int64.Type},
        {"Item_ID", Int64.Type},
        {"Product_ID", Int64.Type},
        {"Quantity", Int64.Type},
        {"Unit_Price", type number},
        {"Discount_Rate", type number},
        {"Customer_ID", Int64.Type},
        {"Order_Status_Code", Int64.Type},
        {"Order_Date", type date},
        {"Required_Date", type date},
        {"Shipped_Date", type date},
        {"Store_ID", Int64.Type},
        {"Staff_ID", Int64.Type},
        {"Order_Status", type text},
        {"Gross_Amount", type number},
        {"Discount_Amount", type number},
        {"Net_Amount", type number},
        {"Days_To_Ship", Int64.Type}
    })
in
    #"Changed Types"
```

---

## 6. Inventory Fact Table (`Fact_Inventory`)

```powerquery
let
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    stocks_Table = Source{[Item="stocks", Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(stocks_Table, [PromoteAllScalars=true]),
    #"Filtered Blank Rows" = Table.SelectRows(#"Promoted Headers", each [store_id] <> null and [store_id] <> ""),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Blank Rows", {
        {"store_id", "Store_ID"},
        {"product_id", "Product_ID"},
        {"quantity", "Quantity_In_Stock"}
    }),
    #"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns", {
        {"Store_ID", Int64.Type},
        {"Product_ID", Int64.Type},
        {"Quantity_In_Stock", Int64.Type}
    })
in
    #"Changed Types"
```
