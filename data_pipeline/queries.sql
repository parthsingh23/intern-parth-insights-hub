-- Total net value and total quantity.
SELECT SUM("Net Value (INR)") as total_net_value, SUM("Qty") as total_quantity FROM sales;

-- Net value by region, with percentage share.
SELECT Region, SUM("Net Value (INR)") as regional_net_value, ROUND(SUM("Net Value (INR)") * 100 / (SELECT SUM("Net Value (INR)") FROM sales), 2) as percentage_share
FROM sales
GROUP BY Region
ORDER BY regional_net_value DESC;

-- Top 5 SKUs by net value.
SELECT "SKU Code", "SKU Name", SUM("Net Value (INR)") as total_net_value
FROM sales
GROUP BY "SKU Code", "SKU Name"
ORDER BY total_net_value DESC
LIMIT 5;

-- Monthly net value trend (month, net value).
SELECT strftime('%Y-%m', "Invoice Date") as sales_month, ROUND(SUM("Net Value (INR)"), 2) as monthly_net_value
FROM sales
GROUP BY sales_month
ORDER BY sales_month;

-- Return value as a percentage of gross sales, by region.
SELECT Region, ROUND(SUM("Net Value (INR)") FILTER (WHERE is_return = 0), 2) AS gross_sales, ROUND(ABS(SUM("Net Value (INR)") FILTER (WHERE is_return = 1)), 2) AS return_value, ROUND(ABS(SUM("Net Value (INR)") FILTER (WHERE is_return = 1)) * 100.0 / SUM("Net Value (INR)") FILTER (WHERE is_return = 0), 2) AS return_percentage
FROM sales
GROUP BY Region
ORDER BY return_percentage DESC;

-- The 3 distributors with the highest return value.
SELECT "Dist Code", "Distributor Name", ROUND(SUM(ABS("Net Value (INR)")), 2) AS total_return_value
FROM sales
WHERE is_return = 1
GROUP BY "Dist Code", "Distributor Name"
ORDER BY total_return_value DESC
LIMIT 3;
