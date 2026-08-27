# Multi-Page Power BI Dashboard Layout Blueprint

## 📄 Page 1: Executive Sales Overview
- **Goal**: High-level executive pulse check on overall revenue, growth vs prior year, volume, and top categories.
- **Components**:
  1. **Header Banner**: Dynamic title showing selected Year/Quarter, Last Refreshed timestamp, Logo, and Bookmark navigation buttons (Overview | Products & Inventory | Customers & Stores | Order Fulfillment).
  2. **Top Filter Slicers**: Horizontal pill slicers (Year, Quarter, Store Location, Category).
  3. **KPI Scorecard Strip (5 Cards)**:
     - Card 1: `Total Net Revenue` + YoY Variance badge (`▲ +14.2%`).
     - Card 2: `Total Orders` + YoY Variance badge.
     - Card 3: `Average Order Value (AOV)`.
     - Card 4: `Total Units Sold`.
     - Card 5: `Average Discount %`.
  4. **Main Chart Left**: `Net Revenue by Month vs Net Revenue SPLY` (Line chart with shaded area for current year).
  5. **Main Chart Right**: `Net Revenue by Category & Brand` (Stacked/Clustered Horizontal Bar Chart).
  6. **Bottom Left**: `Store Performance Comparison` (Bar chart or Mini-matrix with CA, NY, TX comparisons).
  7. **Bottom Right**: `Top 5 Best Selling Models` (Horizontal bar chart with data labels).

---

## 📄 Page 2: Product & Inventory Intelligence
- **Goal**: Identify product sales velocity, inventory risks, out-of-stock items, and stock-to-sales ratios.
- **Components**:
  1. **KPI Cards**: `Total Inventory Units`, `Total Inventory Value ($)`, `Out of Stock Products Count`, `Inventory Turnover Ratio`.
  2. **Chart 1**: `Current Stock vs Units Sold by Product Category` (Combo Clustered Column & Line Chart).
  3. **Chart 2**: `Stock Distribution Across Stores` (100% Stacked Bar Chart by Store: Baldwin Bikes, Santa Cruz Bikes, Rowlett Bikes).
  4. **Detailed Matrix**: `Product Inventory Health Table`:
     - Columns: `Category`, `Brand`, `Product Name`, `Model Year`, `List Price`, `Units Sold`, `Current Stock`, `Stock Status (In Stock / Low Stock / Out of Stock)` with conditional color icons.

---

## 📄 Page 3: Customer & Store Performance
- **Goal**: Understand customer geographic concentration, repeat purchase behavior, and sales staff leaderboard.
- **Components**:
  1. **KPI Cards**: `Total Customers`, `Revenue Per Customer`, `New Customers Count`, `Repeat Customer Rate %`.
  2. **Chart 1**: `Revenue by Customer State & City` (Filled Map / Shape Map or Treemap).
  3. **Chart 2**: `Staff Sales Leaderboard` (Horizontal Bar Chart showing Net Revenue per Staff member grouped by Store).
  4. **Chart 3**: `Customer Order Frequency Distribution` (Histogram / Column chart: 1 order, 2 orders, 3+ orders).

---

## 📄 Page 4: Order Fulfillment & Operations
- **Goal**: Monitor fulfillment speed, order status pipeline, and shipping lead times.
- **Components**:
  1. **KPI Cards**: `Completed Orders`, `Pending/Processing Orders`, `Average Shipping Lead Time (Days)`, `On-Time Delivery %`.
  2. **Chart 1**: `Order Status Breakdown` (Donut Chart or Horizontal Funnel: Completed vs Pending vs Processing vs Rejected).
  3. **Chart 2**: `Average Days to Ship by Store & Month` (Line Chart).
  4. **Detailed Table**: `Orders Delayed / Pending Shipments` with customer contact email, phone, and store location for proactive customer service.
