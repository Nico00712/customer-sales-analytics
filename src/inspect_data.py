from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")

csv_files = list(DATA_DIR.glob("*.csv"))

for file in csv_files:
    print(f"\n=== {file.name} ===")

    df = pd.read_csv(file)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False).head(10)) # Searches for missing values within a file and sums them up.

    print("\nData types:")
    print(df.dtypes)
