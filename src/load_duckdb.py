from pathlib import Path
import duckdb

"""
Loads the raw Olist CSV files into a DuckDB database.

The script creates a table per source file and prints the number of imported rows for each table.
"""

DATA_DIR = Path("data/raw")
DB_PATH = Path("data/olist.duckdb")

con = duckdb.connect(DB_PATH)

tables = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

for table_name, filename in tables.items(): 
    path = DATA_DIR / filename

    # Rebuild each table from the raw CSV so the database can be recreated reproducibly from the orginal source data.
    con.execute(
        f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT *
        FROM read_csv_auto('{path.as_posix()}')
        """
    )

    count = con.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()[0]

    print(f"{table_name}: {count:,} rows")

con.close