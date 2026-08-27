# Power BI DAX Optimization & Formula Engine Best Practices

## 1. Eliminate Context Transitions Inside Iterators
Avoid calling measures inside `FILTER()` over large tables:
- ❌ **Slow**:
  ```dax
  High Spenders = 
  COUNTROWS(
      FILTER(
          Dim_Customer,
          [Total Net Revenue] > 5000 -- Forces context transition for EVERY customer row
      )
  )
  ```
- ✅ **Optimized**:
  ```dax
  High Spenders = 
  VAR CustomerSummary = 
      ADDCOLUMNS(
          VALUES(Dim_Customer[Customer_ID]),
          "@CustRevenue", [Total Net Revenue]
      )
  RETURN
      COUNTROWS(
          FILTER(CustomerSummary, [@CustRevenue] > 5000)
      )
  ```

## 2. Pushing Predicates to the Storage Engine
Use column filters directly in `CALCULATE` or with `KEEPFILTERS` instead of wrapping the entire table in `FILTER()`:
- ❌ **Slow (Formula Engine heavy)**:
  ```dax
  CA Revenue = 
  CALCULATE(
      [Total Net Revenue],
      FILTER(Dim_Store, Dim_Store[State] = "CA")
  )
  ```
- ✅ **Optimized (Storage Engine direct)**:
  ```dax
  CA Revenue = 
  CALCULATE(
      [Total Net Revenue],
      KEEPFILTERS(Dim_Store[State] = "CA")
  )
  ```

## 3. Pre-aggregate in ETL vs Complex DAX
- If an attribute does not change dynamically with slicers (e.g. `Gross_Amount = quantity * list_price`), compute it in Power Query (M) or source SQL rather than computing row-by-row in DAX iterators.
