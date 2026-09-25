
-- Cohort Retention Rate
WITH customer_orders AS (
    SELECT c.customer_unique_id, DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
),
customer_cohorts AS (
    SELECT customer_unique_id, MIN(order_month) AS cohort_month
    FROM customer_orders
    GROUP BY customer_unique_id
),
cohort_activity AS (
    SELECT co.customer_unique_id, cc.cohort_month, co.order_month, DATE_DIFF('month', cc.cohort_month, co.order_month) AS month_number
    FROM customer_orders co 
    JOIN customer_cohorts cc ON co.customer_unique_id = cc.customer_unique_id
),
cohort_counts AS (
    SELECT cohort_month, month_number, COUNT(DISTINCT customer_unique_id) AS active_customers
    FROM cohort_activity
    GROUP BY cohort_month, month_number
),
cohort_sizes AS (
    SELECT cohort_month, active_customers AS cohort_size
    FROM cohort_counts
    WHERE month_number = 0
)
SELECT cc.cohort_month, cc.month_number, cc.active_customers, cs.cohort_size, ROUND(100.0 * cc.active_customers / cs.cohort_size, 2) AS retention_rate_pct
FROM cohort_counts cc
JOIN cohort_sizes cs ON cc.cohort_month = cs.cohort_month
ORDER BY cc.cohort_month, cc.month_number;