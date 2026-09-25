
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