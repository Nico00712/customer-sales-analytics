from pathlib import Path
from matplotlib.ticker import FuncFormatter
import duckdb
import matplotlib.pyplot as plt

"""
Generates a horizontal bar chart showing the product categories with the highest revenue.

The resulting chart is saved to output/charts/top_categories.png.
"""

# Resolve paths relative to the project root so the script works regardless of the current working directory.
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "olist.duckdb"
SQL_PATH = BASE_DIR / "sql" / "top_categories.sql"
OUTPUT_DIR = BASE_DIR / "output" / "charts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(DB_PATH))

query = SQL_PATH.read_text(encoding="utf-8")

df = con.execute(query).fetchdf()

con.close()

#Sort ascending so the highest_revenue category appears at the top of the horizontal chart.
df = df.sort_values("revenue")

# Improve category labels for presentation.
df["category"] = df["category"].str.replace("_", " ").str.title()

fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(
    df["category"],
    df["revenue"]
)

ax.set_title("Top 10 Product Categories by Revenue")

# Format large revenue values in millions for a cleaner x-axis.
ax.xaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f"{x / 1_000_000:.1f}M")
)

ax.set_xlabel("Revenue")
ax.set_ylabel("Product Category")

fig.tight_layout()

output_path = OUTPUT_DIR / "top_categories.png"

fig.savefig(
    output_path,
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print(f"Chart saved to: {output_path}")

