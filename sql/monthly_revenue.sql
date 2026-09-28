
-- Gibt den Umsatz pro Monat aus
SELECT DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    ROUND(Sum(oi.price), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;