from pathlib import Path
import duckdb
import matplotlib.pyplot as plt

"""
Generates a cohort-retention heatmap based on each customer's first purchase month.

The resulting chart is saved to output/charts/cohort_retention.png.
"""

# Resolve paths relative to the project root so the script works regardless of the current working directory.
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "olist.duckdb"
SQL_PATH = BASE_DIR / "sql" / "cohort_retention.sql"
OUTPUT_DIR = BASE_DIR / "output" / "charts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(DB_PATH))

query = SQL_PATH.read_text(encoding="utf-8")

df = con.execute(query).fetch_df()

con.close()

# Datumsanzeige etwas vereinfachen
df["cohort_month"] = (
    df["cohort_month"]
    .dt.strftime("%Y-%m")
)

# Pivot the cohort data so rows represent customer cohorts and colums represent months since the first purchase.
retention_matrix = df.pivot(
    index="cohort_month",
    columns="month_number",
    values="retention_rate_pct"
)

print(retention_matrix)

# Exclude incomplete cohorts to keep retention periods comparable.
retention_plot = retention_matrix.loc[
    "2017-01":"2018-08",
    1:12
]

fig, ax = plt.subplots(figsize=(12,8))

# Most retention values are below 1%, so the color scale is capped at 1% to make differences between cohorts easier to see.
image = ax.imshow(
    retention_plot,
    aspect="auto",
    vmin=0,
    vmax=1
)

ax.set_title("Customer Cohort Retention")
ax.set_xlabel("Months Since First Purchase")
ax.set_ylabel("Cohort Month")

ax.set_xticks(range(len(retention_plot.columns)))
ax.set_xticklabels(retention_plot.columns)

ax.set_yticks(range(len(retention_plot.index)))
ax.set_yticklabels(retention_plot.index)

fig.colorbar(
    image,
    ax=ax,
    label = "Retention Rate (%)"
)

fig.tight_layout

output_path = OUTPUT_DIR / "cohort_retention.png"

fig.savefig(
    output_path,
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print(f"\nChart saved to: {output_path}")
