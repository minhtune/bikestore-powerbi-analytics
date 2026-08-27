# Power BI DAX Measure Catalog


## 📁 Folder: `01. Financial & Revenue KPIs`

### `Total Gross Revenue`
- **Description**: Total revenue before applying discounts.
- **Format String**: `$#,##0`
```dax
Total Gross Revenue = 
SUMX(Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[Unit_Price])
```

### `Total Discount Amount`
- **Description**: Total monetary discount granted across all sales.
- **Format String**: `$#,##0`
```dax
Total Discount Amount = 
SUMX(Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[Unit_Price] * Fact_Sales[Discount_Rate])
```

### `Total Net Revenue`
- **Description**: Net realized sales revenue after deducting discounts.
- **Format String**: `$#,##0`
```dax
Total Net Revenue = 
[Total Gross Revenue] - [Total Discount Amount]
```

### `Average Discount %`
- **Description**: Effective average discount percentage.
- **Format String**: `0.0%`
```dax
Average Discount % = 
DIVIDE([Total Discount Amount], [Total Gross Revenue], 0)
```


## 📁 Folder: `02. Volume & Orders`

### `Total Orders`
- **Description**: Unique count of orders placed.
- **Format String**: `#,##0`
```dax
Total Orders = 
DISTINCTCOUNT(Fact_Sales[Order_ID])
```

### `Total Units Sold`
- **Description**: Total physical items sold.
- **Format String**: `#,##0`
```dax
Total Units Sold = 
SUM(Fact_Sales[Quantity])
```

### `Average Order Value`
- **Description**: Average revenue generated per order.
- **Format String**: `$#,##0.00`
```dax
Average Order Value = 
DIVIDE([Total Net Revenue], [Total Orders], BLANK())
```

### `Units Per Order`
- **Description**: Average quantity of items in a single transaction.
- **Format String**: `0.0`
```dax
Units Per Order = 
DIVIDE([Total Units Sold], [Total Orders], BLANK())
```


## 📁 Folder: `03. Time Intelligence (YoY / MoM / YTD)`

### `Net Revenue SPLY`
- **Description**: Net revenue for the same period in the prior year.
- **Format String**: `$#,##0`
```dax
Net Revenue SPLY = 
CALCULATE([Total Net Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))
```

### `YoY Net Revenue Delta`
- **Description**: Absolute dollar variance compared to same period last year.
- **Format String**: `$#,##0`
```dax
YoY Net Revenue Delta = 
VAR CurrentRev = [Total Net Revenue]
VAR PriorRev = [Net Revenue SPLY]
RETURN IF(NOT ISBLANK(CurrentRev) && NOT ISBLANK(PriorRev), CurrentRev - PriorRev, BLANK())
```

### `YoY Net Revenue Growth %`
- **Description**: Percentage growth compared to prior year.
- **Format String**: `+0.0%;-0.0%;0.0%`
```dax
YoY Net Revenue Growth % = 
VAR CurrentRev = [Total Net Revenue]
VAR PriorRev = [Net Revenue SPLY]
RETURN DIVIDE(CurrentRev - PriorRev, PriorRev, BLANK())
```

### `Net Revenue YTD`
- **Description**: Cumulative net revenue Year-to-Date.
- **Format String**: `$#,##0`
```dax
Net Revenue YTD = 
CALCULATE([Total Net Revenue], DATESYTD(Dim_Date[Date]))
```


## 📁 Folder: `04. Customer Analytics`

### `Total Active Customers`
- **Description**: Count of unique purchasing customers.
- **Format String**: `#,##0`
```dax
Total Active Customers = 
DISTINCTCOUNT(Fact_Sales[Customer_ID])
```

### `Revenue Per Customer`
- **Description**: Average net revenue per active customer.
- **Format String**: `$#,##0.00`
```dax
Revenue Per Customer = 
DIVIDE([Total Net Revenue], [Total Active Customers], BLANK())
```


## 📁 Folder: `05. Inventory & Supply Chain`

### `Total Stock Quantity`
- **Description**: Total units currently held across store inventories.
- **Format String**: `#,##0`
```dax
Total Stock Quantity = 
SUM(Fact_Inventory[Quantity_In_Stock])
```

### `Total Stock Value`
- **Description**: Monetary value of current stock at list price.
- **Format String**: `$#,##0`
```dax
Total Stock Value = 
SUMX(Fact_Inventory, Fact_Inventory[Quantity_In_Stock] * RELATED(Dim_Product[List_Price]))
```


## 📁 Folder: `06. Dynamic UI & Formatting`

### `Dynamic Dashboard Title`
- **Description**: Dynamic header text for report canvases.
- **Format String**: `Text`
```dax
Dynamic Dashboard Title = 
VAR SelectedYear = SELECTEDVALUE(Dim_Date[Year], "All Years")
VAR SelectedBrand = SELECTEDVALUE(Dim_Product[Brand_Name], "All Brands")
RETURN "Executive Performance Overview - " & SelectedBrand & " (" & SelectedYear & ")"
```
