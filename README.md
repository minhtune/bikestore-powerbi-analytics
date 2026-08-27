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
> **Note**: If you cloned or moved this repository to a different folder, update the `FilePath` parameter via **Home > Transform Data > Edit Parameters** to point to your local `BikeStore.xlsx`.

### 3. Regenerate Report Visuals (Optional)
To programmatically regenerate all 4 dashboard pages with verified schema bindings:
- **On Windows (Zero Dependencies)**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\generate_report_visuals.ps1
  ```
- **Using Python**:
  ```bash
  python generate_report_visuals.py
  ```

### 4. Save as Single PBIX (Optional)
To export as a standalone file, select **File > Save As** > choose **Power BI files (*.pbix)**.

---

## 🛠️ Project Structure

```text
├── BikeStore_Analytics.pbip               # Root Power BI Project File
├── BikeStore_Analytics.Report/            # PBIR Report & Canvas Sections (report.json)
├── BikeStore_Analytics.SemanticModel/     # TMSL model.bim & TMDL Tabular Model
│   ├── model.bim                          # Tabular Object Model JSON schema
│   └── definition/                        # TMDL semantic model definition
├── BikeStore.xlsx                         # Source Raw Data
├── generate_report_visuals.ps1            # Native Windows visual generator script
├── generate_report_visuals.py             # Python visual generator script
├── TROUBLESHOOTING_AND_LESSONS_LEARNED.md # Complete post-mortem & troubleshooting guide
├── dashboard_preview.html                 # Interactive HTML Dashboard Wireframe
├── data_profile_report.md                 # Complete Data Profiling Report
├── dax_measures_catalog.md                # 17 DAX Measures Dictionary
└── .agents/                               # Power BI Analytics Plugin & Skills
    ├── plugins/powerbi-analytics/
    ├── rules/
    └── skills/
        ├── powerbi-powerquery-m/          # Power Query ETL & M patterns
        ├── powerbi-report-authoring/      # PBIP/PBIR visual generation & troubleshooting
        ├── powerbi-data-modeling/         # Star Schema & relationship rules
        ├── powerbi-dax-expert/            # Production DAX measures & optimization
        └── powerbi-dashboard-design/      # Executive visual layouts & themes
```

---

## 📖 Troubleshooting & Error Log
Detailed analysis of all errors encountered during development, root causes, and verified fixes are documented in:
👉 [**TROUBLESHOOTING_AND_LESSONS_LEARNED.md**](./TROUBLESHOOTING_AND_LESSONS_LEARNED.md)

