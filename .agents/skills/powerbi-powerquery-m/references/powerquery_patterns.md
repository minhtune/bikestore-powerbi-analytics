# Power Query (M) Script Library & Design Patterns

## 1. Dynamic Calendar (Date Dimension) in M

This M query dynamically scans the date range from your Fact tables and generates an enterprise Date dimension without external dependencies.

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

## 2. Denormalized Product Dimension (`Dim_Product`)

Merge `products`, `brands`, and `categories` into a single Star Schema dimension in M:

```powerquery
let
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    
    // 1. Load Products Table
    products_Table = Source{[Item="products",Kind="Table"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(products_Table, [PromoteAllScalars=true]),
    
    // 2. Merge Brands
    brands_Table = Source{[Item="brands",Kind="Table"]}[Data],
    #"Promoted Brands" = Table.PromoteHeaders(brands_Table, [PromoteAllScalars=true]),
    #"Merged Brands" = Table.NestedJoin(#"Promoted Headers", {"brand_id"}, #"Promoted Brands", {"brand_id"}, "BrandTable", JoinKind.LeftOuter),
    #"Expanded Brand" = Table.ExpandTableColumn(#"Merged Brands", "BrandTable", {"brand_name"}, {"Brand_Name"}),
    
    // 3. Merge Categories
    categories_Table = Source{[Item="categories",Kind="Table"]}[Data],
    #"Promoted Categories" = Table.PromoteHeaders(categories_Table, [PromoteAllScalars=true]),
    #"Merged Categories" = Table.NestedJoin(#"Expanded Brand", {"category_id"}, #"Promoted Categories", {"category_id"}, "CategoryTable", JoinKind.LeftOuter),
    #"Expanded Category" = Table.ExpandTableColumn(#"Merged Categories", "CategoryTable", {"category_name"}, {"Category_Name"}),
    
    // 4. Clean and Standardize Names & Types
    #"Renamed Columns" = Table.RenameColumns(#"Expanded Category",{
        {"product_id", "Product_ID"},
        {"product_name", "Product_Name"},
        {"brand_id", "Brand_ID"},
        {"category_id", "Category_ID"},
        {"model_year", "Model_Year"},
        {"list_price", "List_Price"}
    }),
    #"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns",{
        {"Product_ID", Int64.Type},
        {"Product_Name", type text},
        {"Brand_ID", Int64.Type},
        {"Brand_Name", type text},
        {"Category_ID", Int64.Type},
        {"Category_Name", type text},
        {"Model_Year", Int64.Type},
        {"List_Price", Currency.Type}
    })
in
    #"Changed Types"
```

---

## 3. Sales Fact Table (`Fact_Sales`)

Combining `orders` and `order_items` into a clean transactional grain fact table:

```powerquery
let
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    
    // 1. Load Order Items
    order_items_Table = Source{[Item="order_items",Kind="Table"]}[Data],
    #"Promoted Items" = Table.PromoteHeaders(order_items_Table, [PromoteAllScalars=true]),
    
    // 2. Load Orders
    orders_Table = Source{[Item="orders",Kind="Table"]}[Data],
    #"Promoted Orders" = Table.PromoteHeaders(orders_Table, [PromoteAllScalars=true]),
    
    // 3. Join Header Info to Line Items
    #"Merged Orders" = Table.NestedJoin(#"Promoted Items", {"order_id"}, #"Promoted Orders", {"order_id"}, "OrderHeader", JoinKind.Inner),
    #"Expanded Orders" = Table.ExpandTableColumn(#"Merged Orders", "OrderHeader", 
        {"customer_id", "order_status", "order_date", "required_date", "shipped_date", "store_id", "staff_id"}, 
        {"Customer_ID", "Order_Status_Code", "Order_Date", "Required_Date", "Shipped_Date", "Store_ID", "Staff_ID"}
    ),
    
    // 4. Calculate Order Status Description
    #"Added Status Desc" = Table.AddColumn(#"Expanded Orders", "Order_Status", each 
        if [Order_Status_Code] = 1 then "Pending"
        else if [Order_Status_Code] = 2 then "Processing"
        else if [Order_Status_Code] = 3 then "Rejected"
        else if [Order_Status_Code] = 4 then "Completed"
        else "Unknown", type text
    ),
    
    // 5. Calculate Revenue Metrics per Line
    #"Added Gross Amount" = Table.AddColumn(#"Added Status Desc", "Gross_Amount", each [quantity] * [list_price], Currency.Type),
    #"Added Discount Amount" = Table.AddColumn(#"Added Gross Amount", "Discount_Amount", each [Gross_Amount] * [discount], Currency.Type),
    #"Added Net Amount" = Table.AddColumn(#"Added Discount Amount", "Net_Amount", each [Gross_Amount] - [Discount_Amount], Currency.Type),
    
    // 6. Rename & Enforce Strict Types
    #"Renamed Columns" = Table.RenameColumns(#"Added Net Amount",{
        {"order_id", "Order_ID"},
        {"item_id", "Line_Item_ID"},
        {"product_id", "Product_ID"},
        {"quantity", "Quantity"},
        {"list_price", "Unit_Price"},
        {"discount", "Discount_Rate"}
    }),
    #"Changed Types" = Table.TransformColumnTypes(#"Renamed Columns",{
        {"Order_ID", Int64.Type},
        {"Line_Item_ID", Int64.Type},
        {"Product_ID", Int64.Type},
        {"Customer_ID", Int64.Type},
        {"Store_ID", Int64.Type},
        {"Staff_ID", Int64.Type},
        {"Order_Status_Code", Int64.Type},
        {"Order_Status", type text},
        {"Order_Date", type date},
        {"Required_Date", type date},
        {"Shipped_Date", type date},
        {"Quantity", Int64.Type},
        {"Unit_Price", Currency.Type},
        {"Discount_Rate", Percentage.Type},
        {"Gross_Amount", Currency.Type},
        {"Discount_Amount", Currency.Type},
        {"Net_Amount", Currency.Type}
    })
in
    #"Changed Types"
```
