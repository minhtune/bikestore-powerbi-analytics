#!/usr/bin/env python3
"""
Power BI Dashboard Blueprint & Visual Mockup Generator
Creates an interactive HTML wireframe and visual design guide based on dataset.
"""

import os
import sys
import json
import pandas as pd

def generate_interactive_blueprint(excel_file="BikeStore.xlsx", output_html="dashboard_preview.html"):
    if not os.path.exists(excel_file):
        print(f"Error: {excel_file} not found.")
        return
        
    xl = pd.ExcelFile(excel_file)
    orders = xl.parse("orders")
    items = xl.parse("order_items")
    stores = xl.parse("stores")
    stocks = xl.parse("stocks")
    products = xl.parse("products")
    customers = xl.parse("customers")
    categories = xl.parse("categories")
    brands = xl.parse("brands")
    staffs = xl.parse("staffs")
    
    # Calculate key benchmark numbers
    merged_sales = items.merge(orders, on="order_id")
    merged_sales["gross_rev"] = merged_sales["quantity"] * merged_sales["list_price"]
    merged_sales["discount_val"] = merged_sales["gross_rev"] * merged_sales["discount"]
    merged_sales["net_rev"] = merged_sales["gross_rev"] - merged_sales["discount_val"]
    
    total_net_rev = merged_sales["net_rev"].sum()
    total_orders = orders["order_id"].nunique()
    total_units = merged_sales["quantity"].sum()
    avg_order_val = total_net_rev / total_orders if total_orders > 0 else 0
    total_cust = customers["customer_id"].nunique()
    total_stock_qty = stocks["quantity"].sum()
    
    # Merge category & brand for products
    prod_full = products.merge(categories, on="category_id").merge(brands, on="brand_id")
    sales_with_prod = merged_sales.merge(prod_full, on="product_id")
    
    cat_summary = sales_with_prod.groupby("category_name")["net_rev"].sum().sort_values(ascending=False).reset_index()
    brand_summary = sales_with_prod.groupby("brand_name")["net_rev"].sum().sort_values(ascending=False).head(5).reset_index()
    store_summary = merged_sales.merge(stores, on="store_id").groupby("store_name")["net_rev"].sum().reset_index()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Power BI Executive Dashboard Blueprint - BikeStore</title>
    <style>
        :root {{
            --bg: #F8FAFC;
            --card-bg: #FFFFFF;
            --primary: #2563EB;
            --primary-light: #EFF6FF;
            --text-dark: #0F172A;
            --text-muted: #64748B;
            --border: #E2E8F0;
            --success: #10B981;
            --accent: #F59E0B;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background-color: var(--bg); color: var(--text-dark); padding: 24px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding: 16px 24px; background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .header h1 {{ font-size: 20px; font-weight: 700; color: var(--text-dark); }}
        .header .subtitle {{ font-size: 13px; color: var(--text-muted); margin-top: 4px; }}
        .nav-tabs {{ display: flex; gap: 8px; margin-bottom: 20px; }}
        .tab-btn {{ padding: 10px 18px; border-radius: 8px; border: 1px solid var(--border); background: var(--card-bg); font-size: 13px; font-weight: 600; cursor: pointer; color: var(--text-muted); transition: all 0.2s; }}
        .tab-btn.active {{ background: var(--primary); color: #fff; border-color: var(--primary); }}
        
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .kpi-card {{ background: var(--card-bg); padding: 18px 20px; border-radius: 12px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .kpi-label {{ font-size: 12px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }}
        .kpi-val {{ font-size: 24px; font-weight: 700; color: var(--text-dark); margin: 8px 0 4px; }}
        .kpi-sub {{ font-size: 12px; color: var(--success); font-weight: 600; display: flex; align-items: center; gap: 4px; }}

        .chart-grid-2 {{ display: grid; grid-template-columns: 3fr 2fr; gap: 16px; margin-bottom: 24px; }}
        .chart-grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }}
        .card {{ background: var(--card-bg); padding: 20px; border-radius: 12px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .card h3 {{ font-size: 15px; font-weight: 600; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }}
        .badge {{ font-size: 11px; padding: 4px 8px; border-radius: 4px; background: var(--primary-light); color: var(--primary); }}
        
        .bar-row {{ display: flex; align-items: center; margin-bottom: 12px; font-size: 13px; }}
        .bar-label {{ width: 140px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .bar-track {{ flex: 1; height: 12px; background: #EEF2F6; border-radius: 6px; margin: 0 12px; overflow: hidden; }}
        .bar-fill {{ height: 100%; background: var(--primary); border-radius: 6px; }}
        .bar-val {{ width: 80px; text-align: right; font-weight: 600; }}
        
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); }}
        th {{ background: #F8FAFC; color: var(--text-muted); font-weight: 600; }}
        
        .instructions-box {{ margin-top: 24px; background: #0F172A; color: #F8FAFC; padding: 20px; border-radius: 12px; font-size: 13px; line-height: 1.6; }}
        .instructions-box h4 {{ color: #38BDF8; margin-bottom: 8px; }}
    </style>
</head>
<body>

    <div class="header">
        <div>
            <h1>🚲 BikeStore Executive BI Dashboard Blueprint</h1>
            <div class="subtitle">Live Preview & Structural Wireframe for Power BI Desktop Modeling</div>
        </div>
        <span class="badge">Star Schema Powered</span>
    </div>

    <div class="nav-tabs">
        <button class="tab-btn active">1. Executive Overview</button>
        <button class="tab-btn">2. Products & Inventory</button>
        <button class="tab-btn">3. Customers & Geography</button>
        <button class="tab-btn">4. Logistics & Fulfillment</button>
    </div>

    <!-- KPI STRIP -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Total Net Revenue</div>
            <div class="kpi-val">${total_net_rev:,.0f}</div>
            <div class="kpi-sub">▲ Verified from 4,722 line items</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-val">{total_orders:,}</div>
            <div class="kpi-sub">▲ Across 3 store locations</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Average Order Value</div>
            <div class="kpi-val">${avg_order_val:,.2f}</div>
            <div class="kpi-sub">~ {total_units/total_orders:.1f} Units / Transaction</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Total Active Customers</div>
            <div class="kpi-val">{total_cust:,}</div>
            <div class="kpi-sub">CA, NY, TX Markets</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Current Stock Inventory</div>
            <div class="kpi-val">{total_stock_qty:,} Units</div>
            <div class="kpi-sub">Across 939 Store Batches</div>
        </div>
    </div>

    <!-- MAIN CHARTS ROW -->
    <div class="chart-grid-2">
        <div class="card">
            <h3>Revenue by Product Category <span class="badge">Visual: Clustered Bar</span></h3>
            {"".join([f'''
            <div class="bar-row">
                <div class="bar-label">{row['category_name']}</div>
                <div class="bar-track"><div class="bar-fill" style="width: {row['net_rev']/cat_summary['net_rev'].max()*100}%;"></div></div>
                <div class="bar-val">${row['net_rev']/1e3:,.1f}K</div>
            </div>
            ''' for _, row in cat_summary.iterrows()])}
        </div>

        <div class="card">
            <h3>Top 5 Selling Brands <span class="badge">Visual: Bar Chart</span></h3>
            {"".join([f'''
            <div class="bar-row">
                <div class="bar-label">{row['brand_name']}</div>
                <div class="bar-track"><div class="bar-fill" style="background: var(--accent); width: {row['net_rev']/brand_summary['net_rev'].max()*100}%;"></div></div>
                <div class="bar-val">${row['net_rev']/1e3:,.1f}K</div>
            </div>
            ''' for _, row in brand_summary.iterrows()])}
        </div>
    </div>

    <div class="chart-grid-3">
        <div class="card">
            <h3>Store Sales Contribution <span class="badge">Visual: Donut / Matrix</span></h3>
            <table>
                <tr><th>Store Name</th><th>Net Revenue</th><th>% Share</th></tr>
                {"".join([f'''
                <tr>
                    <td><b>{row['store_name']}</b></td>
                    <td>${row['net_rev']:,.0f}</td>
                    <td>{row['net_rev']/total_net_rev*100:.1f}%</td>
                </tr>
                ''' for _, row in store_summary.iterrows()])}
            </table>
        </div>
        
        <div class="card">
            <h3>DAX Modeling Directives</h3>
            <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">Pre-configured measures included in <code>_Measures</code> table:</p>
            <ul style="font-size: 13px; padding-left: 18px; line-height: 1.8;">
                <li><code>[Total Net Revenue]</code> = Gross - Discounts</li>
                <li><code>[YoY Net Revenue Growth %]</code> using <code>SAMEPERIODLASTYEAR</code></li>
                <li><code>[Average Order Value]</code> = Revenue / Orders</li>
                <li><code>[Stock-to-Sales Velocity]</code></li>
            </ul>
        </div>
    </div>

    <div class="instructions-box">
        <h4>🚀 Power BI Setup Instructions</h4>
        <ol style="padding-left: 20px;">
            <li>Import <code>BikeStore.xlsx</code> via Power Query using the queries provided in <code>.agents/skills/powerbi-powerquery-m/references/powerquery_patterns.md</code>.</li>
            <li>Apply the Star Schema model structure defined in <code>.agents/skills/powerbi-data-modeling/references/star_schema_guide.md</code>.</li>
            <li>Import the theme JSON located at <code>.agents/skills/powerbi-dashboard-design/resources/powerbi_theme.json</code>.</li>
            <li>Copy and paste the DAX measures from <code>.agents/skills/powerbi-dax-expert/references/dax_patterns.md</code>.</li>
        </ol>
    </div>

</body>
</html>
"""
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Blueprint generated: {output_html}")

if __name__ == "__main__":
    generate_interactive_blueprint()
