from pathlib import Path
import duckdb
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "olist.duckdb"
SQL_PATH = BASE_DIR / "sql" / "monthly_revenue.sql"
OUTPUT_DIR = BASE_DIR / "output" / "charts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(DB_PATH))

query = SQL_PATH.read_text(encoding="utf-8")

df = con.execute(query).fetchdf()

con.close()

df["month"] = df["month"].dt.strftime("%Y-%m")

df = df[df["month"] < "2018-09"] # Datensatz hat für September 2018 noch sehr wenige Bestellungen

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df["month"], df["revenue"], marker = "o")

ax.set_title("Monthly Revenue")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue")

ax.tick_params(axis = "x", rotation=45)

fig.tight_layout()

output_path = OUTPUT_DIR / "monthly_revenue.png"

fig.savefig(
    output_path,
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print(f"Chart saved to: {output_path}")

