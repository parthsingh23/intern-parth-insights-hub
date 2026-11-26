
# Week 04: EXPLAIN ANALYZE and Index Performance

## Objective

Compare PostgreSQL query execution before and after creating indexes on the
sales table.

## Query

The following query calculates monthly sales value and transaction count
for September 2026.

```sql
EXPLAIN ANALYZE
SELECT
    DATE_TRUNC('month', invoice_date)::date AS sales_month,
    SUM(net_value) AS total_sales,
    COUNT(*) AS transaction_count
FROM sales
WHERE invoice_date >= DATE '2026-09-01'
  AND invoice_date < DATE '2026-10-01'
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY sales_month;
```

## Before Index Creation

The query was executed after temporarily downgrading migration 0002.

- Scan strategy: Sequential Scan
- Index used: None
- Rows returned by scan: 302
- Rows removed by filter: 5,116
- Shared buffers hit: 138
- Planning time: 3.049 ms
- Execution time: 0.769 ms

PostgreSQL scanned the sales table and filtered rows based on the invoice
date condition.

## After Index Creation

Migration `8567eda89aca` added the following indexes:

- `idx_sales_invoice_date` on `sales(invoice_date)`
- `idx_sales_distributor_id` on `sales(distributor_id)`
- `idx_sales_sku_id` on `sales(sku_id)`

The same query was executed after applying migration 0002.

- Scan strategy: Bitmap Index Scan followed by Bitmap Heap Scan
- Index used: `idx_sales_invoice_date`
- Rows returned by scan: 302
- Heap blocks accessed: 67
- Shared buffers hit: 69
- Shared buffers read: 1
- Planning time: 3.482 ms
- Execution time: 0.374 ms

PostgreSQL used the invoice-date index to identify matching rows before
accessing the corresponding table pages.


## Comparison

| Metric | Before | After |
|---|---:|---:|
| Scan strategy | Sequential Scan | Bitmap Index Scan + Bitmap Heap Scan |
| Index used | No | `idx_sales_invoice_date` |
| Matching rows | 302 | 302 |
| Rows removed by filter | 5,116 | Not applicable |
| Execution time | 0.769 ms | 0.374 ms |
| Planning time | 3.049 ms | 3.482 ms |

Observed execution-time reduction:

$$
\frac{0.769 - 0.374}{0.769} \times 100 \approx 51.4\%
$$

The observed execution time decreased from 0.769 ms to 0.374 ms,
approximately 2.06 times faster in these runs.

## Conclusion

The invoice-date index changed the query execution plan from a
sequential scan to an index-assisted bitmap scan.

Both executions returned the same 302 matching rows. The indexed
execution showed an approximately 51.4% reduction in execution time.

This improvement is specific to the recorded executions. Actual
performance depends on table size, data distribution, cache state,
and query selectivity.

The distributor and SKU indexes were also created as required by
the assignment. Their usage should be evaluated with queries
filtering on those columns.
