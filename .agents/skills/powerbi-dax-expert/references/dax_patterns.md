# Power BI Enterprise DAX Pattern Library

## Folder: 01. Financial & Revenue KPIs

### 1. Total Gross Revenue
```dax
Total Gross Revenue = 
SUMX(
    Fact_Sales,
    Fact_Sales[Quantity] * Fact_Sales[Unit_Price]
)
```
*Format: `$#,##0`*

### 2. Total Discount Given
```dax
Total Discount Amount = 
SUMX(
    Fact_Sales,
    Fact_Sales[Quantity] * Fact_Sales[Unit_Price] * Fact_Sales[Discount_Rate]
)
```
*Format: `$#,##0`*

### 3. Total Net Revenue
```dax
Total Net Revenue = 
[Total Gross Revenue] - [Total Discount Amount]
```
*Format: `$#,##0`*

### 4. Overall Discount %
```dax
Average Discount % = 
DIVIDE([Total Discount Amount], [Total Gross Revenue], 0)
```
*Format: `0.0%`*

---

## Folder: 02. Volume & Orders

### 5. Total Orders
```dax
Total Orders = 
DISTINCTCOUNT(Fact_Sales[Order_ID])
```
*Format: `#,##0`*

### 6. Total Units Sold
```dax
Total Units Sold = 
SUM(Fact_Sales[Quantity])
```
*Format: `#,##0`*

### 7. Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE([Total Net Revenue], [Total Orders], BLANK())
```
*Format: `$#,##0.00`*

### 8. Units Per Order (Basket Size)
```dax
Units Per Order = 
DIVIDE([Total Units Sold], [Total Orders], BLANK())
```
*Format: `0.0`*

---

## Folder: 04. Customer Analytics & RFM

### 9. Total Active Customers
```dax
Total Customers = 
DISTINCTCOUNT(Fact_Sales[Customer_ID])
```
*Format: `#,##0`*

### 10. Revenue Per Customer
```dax
Revenue Per Customer = 
DIVIDE([Total Net Revenue], [Total Customers], BLANK())
```
*Format: `$#,##0.00`*

### 11. Customer Status (New vs Returning)
```dax
New Customers Count = 
VAR CustomersWithPriorOrders = 
    CALCULATETABLE(
        VALUES(Fact_Sales[Customer_ID]),
        FILTER(
            ALL(Dim_Date),
            Dim_Date[Date] < MIN(Dim_Date[Date])
        )
    )
VAR CurrentCustomers = VALUES(Fact_Sales[Customer_ID])
RETURN
    COUNTROWS(EXCEPT(CurrentCustomers, CustomersWithPriorOrders))
```

---

## Folder: 05. Operations & Inventory

### 12. Total Inventory Units on Hand
```dax
Total Stock Quantity = 
SUM(Fact_Inventory[Quantity_In_Stock])
```
*Format: `#,##0`*

### 13. Total Inventory Value ($)
```dax
Total Inventory Value = 
SUMX(
    Fact_Inventory,
    Fact_Inventory[Quantity_In_Stock] * RELATED(Dim_Product[List_Price])
)
```
*Format: `$#,##0`*

### 14. Out of Stock Products Count
```dax
Out of Stock Products = 
CALCULATE(
    DISTINCTCOUNT(Fact_Inventory[Product_ID]),
    Fact_Inventory[Quantity_In_Stock] = 0
)
```
*Format: `#,##0`*

---

## Folder: 06. Dynamic Formatting & Titles

### 15. Dynamic Header Title
```dax
Dynamic Page Title = 
VAR SelectedYear = SELECTEDVALUE(Dim_Date[Year], "All Years")
VAR SelectedCategory = SELECTEDVALUE(Dim_Product[Category_Name], "All Categories")
RETURN
    "Performance Summary: " & SelectedCategory & " (" & SelectedYear & ")"
```
