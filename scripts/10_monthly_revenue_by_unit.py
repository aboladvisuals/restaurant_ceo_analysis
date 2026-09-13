import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "location_dataset_clean.xlsx"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load sales invoices
df = pd.read_excel(INPUT_FILE, sheet_name="sales_invoice")

df["Description_clean"] = (
    df["Description"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Revenue classification
def classify_revenue(description):
    d = description.lower().strip()

    if "restaurant" in d:
        return "Restaurant"

    if d.startswith("bar") or " bar " in f" {d} ":
        return "Bar"

    if "lounge/club" in d or d == "lou":
        return "Club/Lounge"

    if "greela" in d or d == "gre":
        return "Greela"

    if "bakery" in d or "baking" in d:
        return "Bakery"

    if "delivery" in d:
        return "Delivery"

    return "Other"


df["Business Unit"] = df["Description_clean"].apply(classify_revenue)

df["Issue date"] = pd.to_datetime(df["Issue date"], errors="coerce")
df["Month"] = df["Issue date"].dt.to_period("M").astype(str)

# Monthly revenue by business unit
monthly = (
    df.groupby(["Month", "Business Unit"], as_index=False)
      .agg(
          Revenue=("Invoice Amount", "sum"),
          Transactions=("Invoice Amount", "count")
      )
)

# Pivot for easier analysis
revenue_pivot = (
    monthly
    .pivot(index="Month", columns="Business Unit", values="Revenue")
    .fillna(0)
    .reset_index()
)

# Ensure expected columns exist
units = [
    "Restaurant",
    "Club/Lounge",
    "Bar",
    "Bakery",
    "Greela",
    "Delivery",
    "Other"
]

for unit in units:
    if unit not in revenue_pivot.columns:
        revenue_pivot[unit] = 0

revenue_pivot["Total Revenue"] = revenue_pivot[units].sum(axis=1)

# Month-on-month total growth
revenue_pivot["MoM Growth %"] = (
    revenue_pivot["Total Revenue"]
    .pct_change()
    .mul(100)
)

# Highest revenue unit each month
revenue_pivot["Top Business Unit"] = (
    revenue_pivot[units].idxmax(axis=1)
)

# Export
output_file = OUTPUT_DIR / "monthly_revenue_by_unit.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    revenue_pivot.to_excel(
        writer,
        sheet_name="Monthly Revenue",
        index=False
    )

    monthly.to_excel(
        writer,
        sheet_name="Detailed Data",
        index=False
    )

print("\nMONTHLY REVENUE ANALYSIS COMPLETE")
print("-" * 55)

print("\nMonthly Revenue by Business Unit:")
print(
    revenue_pivot[
        ["Month"] + units + ["Total Revenue", "MoM Growth %", "Top Business Unit"]
    ].to_string(index=False)
)

print(f"\nSaved to:")
print(output_file)