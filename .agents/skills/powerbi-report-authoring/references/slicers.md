# Slicers & Filtering Reference (`slicer`)

Slicers allow report consumers to interactively filter report sections.

## Slicer Visual Structure
- `visualType`: `"slicer"`
- Projections:
  - `Values`: `[{"queryRef": "Dim_Date.Year"}]` or `[{"queryRef": "Dim_Store.Store_Name"}]`
- Sizing:
  - Horizontal Pills: `width: 240px - 320px`, `height: 40px - 50px`
  - Dropdown / List: `width: 180px - 220px`, `height: 60px - 90px`

## Placement Best Practice
Place slicers in a unified header bar (`y: 10 - 20px`) or an expandable off-canvas filter pane using Power BI Bookmarks.
