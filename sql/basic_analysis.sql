
-- Gibt die Anzahl der Bestellungen nach Status aus
SELECT order_status, COUNT(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;

-- Gibt alle eindeutige Bestellungen aus
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM orders;

-- Gibt den Gesamtumsatz aus Produktpreisen aus
SELECT ROUND(SUM(price), 2) AS total_revenue
FROM order_items;

-- Gibt den Durschnittlichen Warenwert pro Bestellung aus
SELECT ROUND(SUM(price) / COUNT(DISTINCT order_id), 2)
    AS avg_order_value
FROM order_items;

-- Gibt die Bestellungen pro Monat aus
SELECT DATE_TRUNC('month', order_purchase_timestamp) AS month,
    COUNT(DISTINCT order_id) AS orders
FROM orders
GROUP BY month
ORDER BY month;

-- Gibt den Umsatz pro Monat aus
SELECT DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    ROUND(Sum(oi.price), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;

-- Gibt die TOP 10 Produktkategorien nach Umsatz aus
SELECT pct.product_category_name_english AS category, 
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi 
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN category_translation pct ON p.product_category_name = pct.product_category_name
GROUP BY category
ORDER BY revenue DESC
LIMIT 10;

-- Gibt die 20 Kunden mit den meisten Bestellungen aus
SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
ORDER BY order_count DESC 
LIMIT 20;

-- Durchschnittliche Lieferdauer in Tagen
SELECT ROUND(AVG(DATE_DIFF('day', order_purchase_timestamp, order_delivered_customer_date)), 2) AS avg_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;
