
-- Verkürzte Version des 'Ranking der Produktkategorien nach Umsatz' in advanced_analysis.sql
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
    category,
    ROUND(revenue, 2) AS revenue
FROM category_revenue
ORDER BY revenue DESC
LIMIT 10;