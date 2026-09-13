import pandas as pd
from pathlib import Path

# -----------------------------
# PATHS
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "location_dataset_clean.xlsx"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# LOAD SALES DATA
# -----------------------------
df = pd.read_excel(INPUT_FILE, sheet_name="sales_invoice")

# Make description safe for classification
df["Description_clean"] = (
    df["Description"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# -----------------------------
# REVENUE CLASSIFICATION
# -----------------------------
def classify_revenue(description):
    d = description.lower().strip()

    # Restaurant
    if "restaurant" in d:
        return "Restaurant"

    # Bar
    if d.startswith("bar") or " bar " in f" {d} ":
        return "Bar"

    # Club / Lounge
    if "lounge/club" in d or d == "lou":
        return "Club/Lounge"

    # Greela
    if "greela" in d or d == "gre":
        return "Greela"

    # Bakery
    if "bakery" in d or "baking" in d:
        return "Bakery"

    # Delivery
    if "delivery" in d:
        return "Delivery"

    # Known but not confidently attributable
    if "campus sales" in d:
        return "Other"

    if "january outstanding debt" in d:
        return "Other"

    # Everything else
    return "Other"


df["Business Unit"] = df["Description_clean"].apply(classify_revenue)

# -----------------------------
# SUMMARY
# -----------------------------
summary = (
    df.groupby("Business Unit", as_index=False)
      .agg(
          Revenue=("Invoice Amount", "sum"),
          Transactions=("Invoice Amount", "count")
      )
      .sort_values("Revenue", ascending=False)
)

summary["Revenue Share %"] = (
    summary["Revenue"] / summary["Revenue"].sum() * 100
)

# -----------------------------
# DESCRIPTION CHECK
# -----------------------------
description_check = (
    df.groupby(["Description_clean", "Business Unit"], as_index=False)
      .agg(
          Revenue=("Invoice Amount", "sum"),
          Transactions=("Invoice Amount", "count")
      )
      .sort_values("Revenue", ascending=False)
)

# -----------------------------
# MONTHLY BUSINESS UNIT REVENUE
# -----------------------------
df["Issue date"] = pd.to_datetime(df["Issue date"], errors="coerce")
df["Month"] = df["Issue date"].dt.to_period("M").astype(str)

monthly = (
    df.groupby(["Month", "Business Unit"], as_index=False)
      .agg(
          Revenue=("Invoice Amount", "sum"),
          Transactions=("Invoice Amount", "count")
      )
      .sort_values(["Month", "Revenue"], ascending=[True, False])
)

# -----------------------------
# EXPORT
# -----------------------------
output_file = OUTPUT_DIR / "revenue_analysis.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    summary.to_excel(writer, sheet_name="Revenue Summary", index=False)
    monthly.to_excel(writer, sheet_name="Monthly Revenue", index=False)
    description_check.to_excel(
        writer,
        sheet_name="Classification Check",
        index=False
    )

print("\nREVENUE ANALYSIS COMPLETE")
print("-" * 50)

print("\nRevenue by Business Unit:")
print(summary.to_string(index=False))

print(f"\nSaved to:")
print(output_file)