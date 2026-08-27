# Power BI Star Schema Transformation & Architecture Guide

## Step-by-Step Transformation Workflow

### Step 1: Denormalize Snowflake Dimensions
When source tables feature multi-tier relational normalized tables (3NF):
- `categories` -> `brands` -> `products`
**Transform into a single Star Dimension**:
- `Dim_Product`:
  - `Product_ID` (PK)
  - `Product_Name`
  - `Model_Year`
  - `Brand_ID` & `Brand_Name`
  - `Category_ID` & `Category_Name`
  - `List_Price`

### Step 2: Establish Conformed Dimensions
Ensure dimension keys are distinct and consistent across all fact tables:
- `Dim_Customer`: `Customer_ID`, `Full_Name`, `Email`, `Phone`, `City`, `State`, `Zip_Code`
- `Dim_Store`: `Store_ID`, `Store_Name`, `City`, `State`, `Zip_Code`
- `Dim_Staff`: `Staff_ID`, `Full_Name`, `Active_Status`, `Store_ID`, `Manager_Name`
- `Dim_Date`: Standard calendar table with Year, Quarter, Month, Month Name, Day, Day of Week, Fiscal Period, Is_Weekend.

### Step 3: Grain Alignment for Fact Tables
- **Sales Transactions Fact (`Fact_Sales`)**:
  - Grain: One row per order line item.
  - Join: `orders` + `order_items`
  - Keys: `Order_ID`, `Item_ID`, `Customer_ID`, `Store_ID`, `Staff_ID`, `Product_ID`, `Order_Date`, `Required_Date`, `Shipped_Date`
  - Measures / Degenerate fields: `Quantity`, `List_Price`, `Discount_Rate`, `Gross_Revenue`, `Discount_Amount`, `Net_Revenue`, `Order_Status`
- **Inventory Snapshot Fact (`Fact_Inventory`)**:
  - Grain: Product per Store quantity balance.
  - Keys: `Store_ID`, `Product_ID`
  - Metrics: `Quantity_In_Stock`

### Step 4: Power BI Relationship Matrix
| From (Fact) | To (Dimension) | Cardinality | Cross Filter | State |
| :--- | :--- | :--- | :--- | :--- |
| `Fact_Sales[Customer_ID]` | `Dim_Customer[Customer_ID]` | Many to One (*:1) | Single | Active |
| `Fact_Sales[Product_ID]` | `Dim_Product[Product_ID]` | Many to One (*:1) | Single | Active |
| `Fact_Sales[Store_ID]` | `Dim_Store[Store_ID]` | Many to One (*:1) | Single | Active |
| `Fact_Sales[Staff_ID]` | `Dim_Staff[Staff_ID]` | Many to One (*:1) | Single | Active |
| `Fact_Sales[Order_Date]` | `Dim_Date[Date]` | Many to One (*:1) | Single | Active |
| `Fact_Sales[Shipped_Date]` | `Dim_Date[Date]` | Many to One (*:1) | Single | Inactive |
| `Fact_Sales[Required_Date]` | `Dim_Date[Date]` | Many to One (*:1) | Single | Inactive |
| `Fact_Inventory[Store_ID]` | `Dim_Store[Store_ID]` | Many to One (*:1) | Single | Active |
| `Fact_Inventory[Product_ID]` | `Dim_Product[Product_ID]` | Many to One (*:1) | Single | Active |
