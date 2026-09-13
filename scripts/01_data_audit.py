from pathlib import Path
import pandas as pd


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

LOCATION_FILE = DATA_DIR / "location_dataset.xlsx"
PNL_FILE = DATA_DIR / "LOCATION_MONTHLY_PNL.xlsx"


def load_workbook(path):
    """Load all sheets from an Excel workbook."""
    workbook = pd.ExcelFile(path)

    return {
        sheet: pd.read_excel(path, sheet_name=sheet)
        for sheet in workbook.sheet_names
    }


# Load workbooks
location = load_workbook(LOCATION_FILE)
monthly_pnl = load_workbook(PNL_FILE)


# Inspect location datasets
print("\nLOCATION DATASETS")
print("=" * 70)

for name, df in location.items():

    print(f"\n{name}")
    print("-" * 70)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")


# Inspect monthly P&L datasets
print("\n\nMONTHLY P&L DATASETS")
print("=" * 70)

for name, df in monthly_pnl.items():

    print(f"\n{name}")
    print("-" * 70)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")