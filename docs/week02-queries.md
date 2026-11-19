# Week 2 SQL Analysis

## Overview

The cleaned secondary-sales dataset was loaded into a SQLite database named `sales.db`, with the table name `sales`.

- Clean records analysed: 5,418
- Number of analytical queries: 6
- SQL source file: `data_pipeline/queries.sql`

---

## Q1. What are the total net value and total quantity?

### SQL query

```sql
SELECT
    SUM("Net Value (INR)") AS total_net_value,
    SUM("Qty") AS total_quantity
FROM sales;
```

### Result

| Metric | Result |
|---|---:|
| Total net value | ₹60,984,552.24 |
| Total quantity | 568,254 |

### Interpretation

The cleaned dataset contains total net sales of **₹60,984,552.24** across **568,254 units**.

---

## Q2. What is the net value by region, and what percentage of total net value does each region contribute?

### SQL query

```sql
SELECT
    Region,
    SUM("Net Value (INR)") AS regional_net_value,
    ROUND(
        SUM("Net Value (INR)") * 100.0
        / (SELECT SUM("Net Value (INR)") FROM sales),
        2
    ) AS percentage_share
FROM sales
GROUP BY Region
ORDER BY regional_net_value DESC;
```

### Result

| Region | Net value | Percentage share |
|---|---:|---:|
| West | ₹18,726,486.86 | 30.71% |
| South | ₹15,657,120.63 | 25.67% |
| North | ₹14,621,494.11 | 23.98% |
| East | ₹11,979,450.64 | 19.64% |

### Interpretation

West contributes the largest share of net sales at **30.71%**, while East contributes the smallest share at **19.64%**. The four regional shares add up to 100%.

---

## Q3. Which are the top five SKUs by net value?

### SQL query

```sql
SELECT
    "SKU Code",
    "SKU Name",
    SUM("Net Value (INR)") AS total_net_value
FROM sales
GROUP BY "SKU Code", "SKU Name"
ORDER BY total_net_value DESC
LIMIT 5;
```

### Result

| Rank | SKU Code | SKU Name | Net value |
|---:|---|---|---:|
| 1 | EM-1007 | Kesh King Ayurvedic Oil 200 ml | ₹3,956,206.23 |
| 2 | EM-1018 | Dermicool Prickly Heat Powder 300 g | ₹3,527,485.97 |
| 3 | EM-1009 | BoroPlus Antiseptic Cream 40 ml | ₹3,280,513.22 |
| 4 | EM-1023 | He Deodorant 150 ml | ₹3,109,241.46 |
| 5 | EM-1016 | Zandu Chyawanprash 900 g | ₹3,014,871.09 |

### Interpretation

**Kesh King Ayurvedic Oil 200 ml (EM-1007)** has the highest net value among the SKUs, contributing **₹3,956,206.23**.

---

## Q4. What is the monthly net value trend?

### SQL query

```sql
SELECT
    strftime('%Y-%m', "Invoice Date") AS sales_month,
    ROUND(SUM("Net Value (INR)"), 2) AS monthly_net_value
FROM sales
GROUP BY sales_month
ORDER BY sales_month;
```

### Result

| Month | Net value |
|---|---:|
| 2025-01 | ₹201,596.24 |
| 2025-02 | ₹244,226.51 |
| 2025-03 | ₹164,718.06 |
| 2025-04 | ₹2,960,353.81 |
| 2025-05 | ₹2,687,757.66 |
| 2025-06 | ₹3,355,547.48 |
| 2025-07 | ₹2,615,774.05 |
| 2025-08 | ₹3,029,622.83 |
| 2025-09 | ₹3,404,576.15 |
| 2025-10 | ₹3,146,067.27 |
| 2025-11 | ₹3,283,674.08 |
| 2025-12 | ₹3,206,741.11 |
| 2026-01 | ₹3,411,578.61 |
| 2026-02 | ₹4,006,659.58 |
| 2026-03 | ₹4,031,948.02 |
| 2026-04 | ₹3,796,327.70 |
| 2026-05 | ₹3,291,906.13 |
| 2026-06 | ₹4,012,441.99 |
| 2026-07 | ₹2,939,967.38 |
| 2026-08 | ₹3,131,483.42 |
| 2026-09 | ₹3,439,393.46 |
| 2026-10 | ₹274,512.39 |
| 2026-11 | ₹164,490.51 |
| 2026-12 | ₹183,187.80 |

### Interpretation

The highest monthly net value is in **March 2026**, at **₹4,031,948.02**. The lowest is in **November 2026**, at **₹164,490.51**.

### Data-period observation

The workbook README describes the source data as covering **April 2025 to September 2026**. However, the parsed invoice dates and monthly query results also include **January to March 2025** and **October to December 2026**.

These records have been retained because the listed cleaning rules do not instruct the analyst to remove records outside the stated period. This discrepancy should be reviewed or clarified with the assignment owner rather than silently filtering the records.

---

## Q5. What is the return value as a percentage of gross sales, by region?

### SQL query

```sql
SELECT
    Region,
    ROUND(
        SUM("Net Value (INR)") FILTER (WHERE is_return = 0),
        2
    ) AS gross_sales,
    ROUND(
        ABS(SUM("Net Value (INR)") FILTER (WHERE is_return = 1)),
        2
    ) AS return_value,
    ROUND(
        ABS(SUM("Net Value (INR)") FILTER (WHERE is_return = 1))
        * 100.0
        / SUM("Net Value (INR)") FILTER (WHERE is_return = 0),
        2
    ) AS return_percentage
FROM sales
GROUP BY Region
ORDER BY return_percentage DESC;
```

### Result

| Region | Gross sales | Return value | Return percentage |
|---|---:|---:|---:|
| North | ₹14,690,670.76 | ₹69,176.65 | 0.47% |
| South | ₹15,710,450.67 | ₹53,330.04 | 0.34% |
| East | ₹12,009,505.74 | ₹30,055.10 | 0.25% |
| West | ₹18,762,427.93 | ₹35,941.07 | 0.19% |

### Interpretation

North has the highest return percentage at **0.47%**, while West has the lowest at **0.19%**. West has the highest gross sales, but its return percentage is the lowest among the four regions.

The metric is calculated as:

`absolute return value / gross sales * 100`

Returns are treated as positive values for this ratio because credit-note amounts are stored as negative values in the cleaned dataset.

---

## Q6. Which three distributors have the highest return value?

### SQL query

```sql
SELECT
    "Dist Code",
    "Distributor Name",
    ROUND(
        SUM(ABS("Net Value (INR)")),
        2
    ) AS total_return_value
FROM sales
WHERE is_return = 1
GROUP BY
    "Dist Code",
    "Distributor Name"
ORDER BY total_return_value DESC
LIMIT 3;
```

### Result

| Rank | Distributor code | Distributor name | Return value |
|---:|---|---|---:|
| 1 | D006 | Amritsar Distributors | ₹27,752.27 |
| 2 | D009 | Chennai Traders | ₹16,601.31 |
| 3 | D003 | Lucknow Enterprises | ₹13,941.70 |

### Interpretation

**Amritsar Distributors (D006)** has the highest return value at **₹27,752.27**, followed by Chennai Traders (D009) and Lucknow Enterprises (D003).

The combined return value of these three distributors is **₹58,295.28**.

---

## Summary of findings

1. Total net sales are **₹60,984,552.24**, with a total quantity of **568,254**.
2. West is the largest contributor to net sales, accounting for **30.71%**.
3. Kesh King Ayurvedic Oil 200 ml (EM-1007) is the top SKU by net value at **₹3,956,206.23**.
4. March 2026 has the highest monthly net value at **₹4,031,948.02**.
5. North has the highest return percentage at **0.47%**.
6. Amritsar Distributors (D006) has the highest return value among distributors at **₹27,752.27**.
7. The observed invoice-date range extends beyond the period stated in the workbook README. The out-of-period records were retained because no supplied cleaning rule directed their removal.
