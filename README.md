# 🚲 BikeStore Power BI End-to-End Analytics

Enterprise-grade Power BI project ([`BikeStore_Analytics.pbip`](./BikeStore_Analytics.pbip)) built with **Kimball Star Schema**, 17 production DAX measures, automated Power Query (M) ETL pipelines, and executive multi-page dashboard architecture.

---

## 📊 Dataset & Architecture Overview

- **Source Dataset**: [`BikeStore.xlsx`](./BikeStore.xlsx) (9 relational tables, 9,071 records).
- **Core KPIs**: Total Net Revenue (~$7.7M), 1,615 Orders, Average Order Value ($4,756), 1,445 Active Customers, 939 Inventory Batches.
- **Data Model**: Star Schema (Fact_Sales, Fact_Inventory, Dim_Date, Dim_Product, Dim_Customer, Dim_Store, Dim_Staff).
- **DAX Measures**: 17 explicit measures organized in Display Folders (Revenue, Volume, Time Intelligence YoY/SPLY/YTD, Customer Analytics, Inventory).

---

## 🚀 Getting Started

### 1. Open the Project
Double click or open [`BikeStore_Analytics.pbip`](./BikeStore_Analytics.pbip) directly with **Power BI Desktop**.

### 2. Refresh Data
Click **Home > Refresh** to load data from [`BikeStore.xlsx`](./BikeStore.xlsx).

### 3. Save as Single PBIX (Optional)
To export as a standalone file, select **File > Save As** > choose **Power BI files (*.pbix)**.

---

## 🛠️ Project Structure

```text
├── BikeStore_Analytics.pbip               # Root Power BI Project File
├── BikeStore_Analytics.Report/            # PBIR Report & Canvas Sections
├── BikeStore_Analytics.SemanticModel/     # TMSL model.bim & TMDL Tabular Model
│   ├── model.bim                          # Tabular Object Model JSON schema
│   └── definition/                        # TMDL semantic model definition
├── BikeStore.xlsx                         # Source Raw Data
├── dashboard_preview.html                 # Interactive HTML Dashboard Wireframe
├── data_profile_report.md                 # Complete Data Profiling Report
├── dax_measures_catalog.md                # 17 DAX Measures Dictionary
└── .agents/                               # Power BI Analytics Plugin & Skills
    ├── plugins/powerbi-analytics/
    ├── rules/
    └── skills/
```
