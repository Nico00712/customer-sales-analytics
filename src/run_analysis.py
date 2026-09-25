from pathlib import Path
import sys
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "olist.duckdb"

analyis_type = sys.argv[1] if len(sys.argv) > 1 else "basic"

sql_files ={
    "basic": BASE_DIR / "sql" / "basic_analysis.sql",
    "advanced": BASE_DIR / "sql" / "advanced_analysis.sql"
}

if analyis_type not in sql_files:
    print("Unkown analysis type.")
    print("Use: basic or advanced")
    sys.exit(1)

SQL_PATH = sql_files[analyis_type]

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


