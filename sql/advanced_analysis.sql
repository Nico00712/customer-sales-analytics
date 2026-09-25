
-- Monatliches Umsatzwachstum
WITH monthly_revenue AS (
    SELECT 
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month, SUM(oi.price) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY month
)
SELECT month, ROUND(revenue, 2) AS revenue, ROUND(100.0 * (revenue / LAG(revenue) OVER (ORDER BY month) -1), 2) AS growth_pct
FROM monthly_revenue
ORDER BY month; 


-- Ranking der Produktkategorien nach Umsatz
WITH category_revenue AS (
    SELECT
        COALESCE(
            pct.product_category_name_english,
            'unknown'
        ) AS category,
        SUM(oi.price) AS revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN category_translation pct ON p.product_category_name = pct.product_category_name
    GROUP BY category
)
SELECT
    category, ROUND(revenue, 2) AS revenue,
    DENSE_RANK() OVER (
        ORDER BY revenue DESC
    ) AS revenue_rank
FROM category_revenue
ORDER BY revenue_rank;

-- Anteil der Kunden mit mehr als einer Bestellung
WITH customer_orders AS(
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
)
SELECT
    COUNT(*) AS total_customers,
    COUNT(*) FILTER(
        WHERE order_count > 1
    ) AS repeat_customers,
    ROUND(100.0 * COUNT(*) FILTER(WHERE order_count > 1) / COUNT(*), 2) AS repeat_customer_rate_pct
FROM customer_orders;


-- Cohort Analysis: Kunden nach Erstbestellmonat 
WITH customer_orders AS (
    SELECT c.customer_unique_id, DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
),
customer_cohorts AS (
    SELECT customer_unique_id, MIN(order_month) AS cohort_month
    FROM customer_orders
    GROUP BY customer_unique_id
)
SELECT
    co.customer_unique_id,
    cc.cohort_month,
    co.order_month
FROM customer_orders co
JOIN customer_cohorts cc ON co.customer_unique_id = cc.customer_unique_id
ORDER BY cc.cohort_month, co.customer_unique_id, co.order_month;

-- Cohort Retention nach Monaten
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
),
customer_cohorts AS (
    SELECT customer_unique_id, MIN(order_month) AS cohort_month
    FROM customer_orders
    GROUP BY customer_unique_id
),
cohort_activity AS (
    SELECT
        co.customer_unique_id,
        cc.cohort_month,
        co.order_month,
        DATE_DIFF('month', cc.cohort_month, co.order_month) AS month_number
    FROM customer_orders co
    JOIN customer_cohorts cc ON co.customer_unique_id = cc.customer_unique_id
)
SELECT cohort_month, month_number, COUNT(DISTINCT customer_unique_id) AS active_customers
FROM cohort_activity
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number;


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




