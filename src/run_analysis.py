from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "olist.duckdb"
SQL_PATH = BASE_DIR / "sql" / "basic_analysis.sql"

con = duckdb.connect(str(DB_PATH))

sql_text = SQL_PATH.read_text(encoding="utf-8")

queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

print("== BASIC ANALYSIS ===")

for index, query in enumerate(queries, start=1):
    print(f"\n --- Query {index} ---")

    result = con.execute(query).fetchdf()

    print(result.to_string(index=False))

con.close()

