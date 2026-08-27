# Power BI Time Intelligence DAX Patterns

> **Prerequisite**: Ensure your `Dim_Date` table is marked as an official Date Table with contiguous daily dates.

## 1. Prior Period / Same Period Last Year (SPLY)

```dax
Net Revenue SPLY = 
CALCULATE(
    [Total Net Revenue],
    SAMEPERIODLASTYEAR(Dim_Date[Date])
)
```

## 2. Year-over-Year (YoY) Growth Variance & %

```dax
YoY Net Revenue Delta = 
VAR CurrentRev = [Total Net Revenue]
VAR PriorRev = [Net Revenue SPLY]
RETURN
    IF(
        NOT ISBLANK(CurrentRev) && NOT ISBLANK(PriorRev),
        CurrentRev - PriorRev,
        BLANK()
    )
```

```dax
YoY Net Revenue Growth % = 
VAR CurrentRev = [Total Net Revenue]
VAR PriorRev = [Net Revenue SPLY]
VAR Variance = CurrentRev - PriorRev
RETURN
    DIVIDE(Variance, PriorRev, BLANK())
```
*Format: `+0.0%;-0.0%;0.0%`*

## 3. Month-over-Month (MoM) Growth

```dax
Net Revenue Previous Month = 
CALCULATE(
    [Total Net Revenue],
    DATEADD(Dim_Date[Date], -1, MONTH)
)
```

```dax
MoM Net Revenue Growth % = 
VAR CurrentRev = [Total Net Revenue]
VAR PriorRev = [Net Revenue Previous Month]
RETURN
    DIVIDE(CurrentRev - PriorRev, PriorRev, BLANK())
```

## 4. Cumulative Year-to-Date (YTD), Quarter-to-Date (QTD), Month-to-Date (MTD)

```dax
Net Revenue YTD = 
CALCULATE(
    [Total Net Revenue],
    DATESYTD(Dim_Date[Date])
)
```

```dax
Net Revenue QTD = 
CALCULATE(
    [Total Net Revenue],
    DATESQTD(Dim_Date[Date])
)
```

```dax
Net Revenue MTD = 
CALCULATE(
    [Total Net Revenue],
    DATESMTD(Dim_Date[Date])
)
```

## 5. Rolling / Moving Averages (30-Day & 90-Day Moving Average)

```dax
Net Revenue 30D Moving Avg = 
VAR LastVisibleDate = MAX(Dim_Date[Date])
VAR DateWindow = 
    DATESBETWEEN(
        Dim_Date[Date],
        LastVisibleDate - 29,
        LastVisibleDate
    )
RETURN
    CALCULATE(
        DIVIDE([Total Net Revenue], 30, BLANK()),
        DateWindow
    )
```

## 6. Role-Playing Date Measures (Shipped Date Analysis)

When `Fact_Sales[Shipped_Date] -> Dim_Date[Date]` is configured as an **Inactive Relationship**:

```dax
Net Revenue Shipped = 
CALCULATE(
    [Total Net Revenue],
    USERELATIONSHIP(Fact_Sales[Shipped_Date], Dim_Date[Date])
)
```
