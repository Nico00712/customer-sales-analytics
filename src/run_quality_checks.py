from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "olist.duckdb"

con = duckdb.connect(str(DB_PATH))

checks = {
    "Order items -> Orders": """
    SELECT COUNT(*)
    FROM order_items oi
    LEFT JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_id IS NULL
    """,

    "Payments -> Orders":"""
    SELECT COUNT(*)
    FROM payments p
    LEFT JOIN orders o ON p.order_id = o.order_id
    WHERE o.order_id IS NULL
    """,

    "Reviews -> Orders": """
    SELECT COUNT(*)
    FROM reviews r
    LEFT JOIN orders o ON r.order_id = o.order_id
    WHERE o.order_id IS NULL
    """,

    "Orders -> Customers": """
    SELECT COUNT(*)
    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
    """,

    "Order items -> Products": """
    SELECT COUNT(*)
    FROM order_items oi
    LEFT JOIN products p ON oi.product_id = p.product_id
    WHERE p.product_id IS NULL
    """,

    "Order items -> Sellers": """
    SELECT COUNT(*)
    FROM order_items oi
    LEFT JOIN sellers s ON oi.seller_id = s.seller_id
    WHERE s.seller_id IS NULL
    """,

    "Negative product prices": """
    SELECT COUNT(*)
    FROM order_items
    WHERE price < 0
    """,

    "Negative freight values": """
    SELECT COUNT(*)
    FROM order_items
    WHERE freight_value < 0
    """,

    "Invalid review scores": """
    SELECT COUNT(*)
    FROM reviews
    WHERE review_score NOT BETWEEN 1 AND 5
    """,

    "Purchase after delivery": """
    SELECT COUNT(*)
    FROM orders
    WHERE order_purchase_timestamp > order_delivered_customer_date
    """
}

print("=== DATA QUALITY CHECKS === \n")

all_passed = True

for name, query in checks.items():
    result = con.execute(query).fetchone()[0]

    if result == 0:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}: {result:,} invalid rows")
        all_passed = False


if all_passed:
    print("\n All integrity checks passed.")
else:
    print("\n Some data quality checks failed")


con.close()
