import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "location_dataset_clean.xlsx"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# --------------------------------
# LOAD PAYMENTS
# --------------------------------
df = pd.read_excel(
    INPUT_FILE,
    sheet_name="payments"
)

df["Description"] = (
    df["Description"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
).fillna(0)

# --------------------------------
# COST CLASSIFICATION
# --------------------------------
def classify_cost(description):

    d = description.lower().strip()

    # BEVERAGES
    beverage_words = [
        "drink",
        "beer",
        "beverage",
        "wine",
        "spirit",
        "soft drink",
        "water",
        "ice cream"
    ]

    if any(word in d for word in beverage_words):
        return "Beverages"

    # FOOD / RAW MATERIALS
    food_words = [
        "food",
        "foodstuff",
        "chicken",
        "beef",
        "goat",
        "catfish",
        "fish",
        "turkey",
        "egg",
        "veggie",
        "vegetable",
        "tomato",
        "pepper",
        "yam",
        "rice",
        "beans",
        "meat",
        "onion",
        "smoked",
        "kitchen item"
    ]

    if any(word in d for word in food_words):
        return "Food & Kitchen"

    # ENERGY / FUEL
    energy_words = [
        "diesel",
        "fuel",
        "petrol",
        "gas",
        "generator",
        "electric",
        "power"
    ]

    if any(word in d for word in energy_words):
        return "Energy & Fuel"

    # MAINTENANCE / REPAIRS
    maintenance_words = [
        "maintenance",
        "repair",
        "plumbing",
        "electrical",
        "renovation",
        "equipment",
        "spare",
        "generator repair"
    ]

    if any(word in d for word in maintenance_words):
        return "Maintenance"

    # STAFF / HR
    staff_words = [
        "staff",
        "salary",
        "welfare",
        "worker",
        "employee",
        "donation"
    ]

    if any(word in d for word in staff_words):
        return "Staff"

    # MARKETING / EVENTS
    marketing_words = [
        "advert",
        "marketing",
        "promotion",
        "event",
        "dj",
        "influencer"
    ]

    if any(word in d for word in marketing_words):
        return "Marketing & Events"

    # UTILITIES / SERVICES
    utility_words = [
        "dstv",
        "internet",
        "water bill",
        "waste",
        "utility",
        "subscription"
    ]

    if any(word in d for word in utility_words):
        return "Utilities & Services"

    # RENT / PROPERTY
    property_words = [
        "rent",
        "house",
        "room",
        "property",
        "warehouse"
    ]

    if any(word in d for word in property_words):
        return "Property"

    # ADMIN / PROFESSIONAL
    admin_words = [
        "accountant",
        "accounting",
        "legal",
        "survey",
        "bank charge",
        "fee",
        "tax"
    ]

    if any(word in d for word in admin_words):
        return "Admin & Professional"

    return "Other"


df["Cost Category"] = df["Description"].apply(
    classify_cost
)

# --------------------------------
# SUMMARY
# --------------------------------
summary = (
    df.groupby("Cost Category", as_index=False)
      .agg(
          Spend=("Amount", "sum"),
          Transactions=("Amount", "count")
      )
      .sort_values("Spend", ascending=False)
)

summary["Spend Share %"] = (
    summary["Spend"]
    / summary["Spend"].sum()
    * 100
)

# --------------------------------
# TOP INDIVIDUAL PAYMENT DESCRIPTIONS
# --------------------------------
top_descriptions = (
    df.groupby(
        ["Description", "Cost Category"],
        as_index=False
    )
    .agg(
        Spend=("Amount", "sum"),
        Transactions=("Amount", "count")
    )
    .sort_values("Spend", ascending=False)
)

# --------------------------------
# MONTHLY COST CATEGORY
# --------------------------------
df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Month"] = (
    df["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly = (
    df.groupby(
        ["Month", "Cost Category"],
        as_index=False
    )
    .agg(
        Spend=("Amount", "sum")
    )
)

monthly_pivot = (
    monthly
    .pivot(
        index="Month",
        columns="Cost Category",
        values="Spend"
    )
    .fillna(0)
    .reset_index()
)

# --------------------------------
# EXPORT
# --------------------------------
output_file = OUTPUT_DIR / "cost_analysis.xlsx"

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    summary.to_excel(
        writer,
        sheet_name="Cost Summary",
        index=False
    )

    top_descriptions.to_excel(
        writer,
        sheet_name="Top Payment Descriptions",
        index=False
    )

    monthly.to_excel(
        writer,
        sheet_name="Monthly Costs",
        index=False
    )

    monthly_pivot.to_excel(
        writer,
        sheet_name="Monthly Cost Pivot",
        index=False
    )

# --------------------------------
# DISPLAY
# --------------------------------
print("\nCOST ANALYSIS COMPLETE")
print("-" * 60)

print("\nCOST BY CATEGORY:\n")
print(summary.to_string(index=False))

print("\n\nTOP 30 PAYMENT DESCRIPTIONS:\n")
print(top_descriptions.head(30).to_string(index=False))

print("\n\nSaved to:")
print(output_file)