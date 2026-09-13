import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

INPUT = DATA_DIR / "location_dataset_clean.xlsx"
OUTPUT = OUTPUT_DIR / "dashboard_data.xlsx"

# ============================================================
# LOAD DATA
# ============================================================

sales = pd.read_excel(INPUT, sheet_name="sales_invoice")
receipts = pd.read_excel(INPUT, sheet_name="receipts")
payments = pd.read_excel(INPUT, sheet_name="payments")
staff = pd.read_excel(INPUT, sheet_name="customers_but_staffs")
bank = pd.read_excel(INPUT, sheet_name="Bank&cash_accounts")

# Dates
sales["Issue date"] = pd.to_datetime(sales["Issue date"], errors="coerce")
receipts["Date"] = pd.to_datetime(receipts["Date"], errors="coerce")
payments["Date"] = pd.to_datetime(payments["Date"], errors="coerce")

sales["Month"] = sales["Issue date"].dt.to_period("M").astype(str)
receipts["Month"] = receipts["Date"].dt.to_period("M").astype(str)
payments["Month"] = payments["Date"].dt.to_period("M").astype(str)

# ============================================================
# 1. REVENUE BY UNIT
# ============================================================

def classify_revenue(description):
    d = str(description).strip().lower()

    if "restaurant" in d:
        return "Restaurant"
    elif "lounge" in d or "club" in d or d == "lou":
        return "Club/Lounge"
    elif d.startswith("bar"):
        return "Bar"
    elif "bakery" in d or "baking" in d:
        return "Bakery"
    elif "greela" in d or d == "gre":
        return "Greela"
    elif "delivery" in d:
        return "Delivery"
    else:
        return "Other"


sales["Revenue Unit"] = sales["Description"].apply(classify_revenue)

monthly_revenue = (
    sales.groupby(["Month", "Revenue Unit"], as_index=False)["Invoice Amount"]
    .sum()
    .rename(columns={"Invoice Amount": "Revenue"})
)

# ============================================================
# 2. MONTHLY REVENUE / RECEIPTS / PAYMENTS
# ============================================================

revenue_monthly = (
    sales.groupby("Month", as_index=False)["Invoice Amount"]
    .sum()
    .rename(columns={"Invoice Amount": "Revenue"})
)

receipts_monthly = (
    receipts.groupby("Month", as_index=False)["Amount"]
    .sum()
    .rename(columns={"Amount": "Receipts"})
)

payments_monthly = (
    payments.groupby("Month", as_index=False)["Amount"]
    .sum()
    .rename(columns={"Amount": "Payments"})
)

monthly_cash = revenue_monthly.merge(
    receipts_monthly, on="Month", how="outer"
).merge(
    payments_monthly, on="Month", how="outer"
).fillna(0)

# ============================================================
# 3. PAYMENT COST CATEGORIES
# ============================================================

def classify_cost(description):
    d = str(description).strip().lower()

    food = [
        "chicken", "beef", "goat", "catfish", "fish", "turkey",
        "egg", "eggs", "veggie", "vegetable", "foodstuff",
        "food items", "pepper", "tomato", "kitchen", "yam",
        "rice", "beans", "meat", "onion", "smoked fish"
    ]

    beverage = [
        "drink", "beer", "water", "ice cream", "beverage",
        "ou k drinks", "drinks from"
    ]

    energy = [
        "diesel", "fuel", "gas", "petrol", "power",
        "electricity", "generator"
    ]

    staff_words = [
        "staff", "salary", "welfare", "employee", "worker"
    ]

    maintenance = [
        "maintenance", "repair", "plumbing", "carpenter",
        "electrical", "renovation"
    ]

    marketing = [
        "event", "marketing", "advert", "promotion"
    ]

    property = [
        "rent", "rental", "property"
    ]

    admin = [
        "bank charge", "professional", "admin", "legal"
    ]

    utilities = [
        "internet", "waste", "water bill", "utility"
    ]

    if any(x in d for x in food):
        return "Food & Kitchen"
    elif any(x in d for x in beverage):
        return "Beverages"
    elif any(x in d for x in energy):
        return "Energy & Fuel"
    elif any(x in d for x in staff_words):
        return "Staff"
    elif any(x in d for x in maintenance):
        return "Maintenance"
    elif any(x in d for x in marketing):
        return "Marketing & Events"
    elif any(x in d for x in property):
        return "Property"
    elif any(x in d for x in admin):
        return "Admin & Professional"
    elif any(x in d for x in utilities):
        return "Utilities & Services"
    else:
        return "Other"


payments["Cost Category"] = payments["Description"].apply(classify_cost)

cost_summary = (
    payments.groupby("Cost Category", as_index=False)["Amount"]
    .sum()
    .rename(columns={"Amount": "Payment Spend"})
)

cost_summary["Share of Payments"] = (
    cost_summary["Payment Spend"] / cost_summary["Payment Spend"].sum()
)

monthly_cost = (
    payments.groupby(["Month", "Cost Category"], as_index=False)["Amount"]
    .sum()
    .rename(columns={"Amount": "Payment Spend"})
)

# ============================================================
# 4. CONTROL KPIs
# ============================================================

total_sales = sales["Invoice Amount"].sum()
total_receipts = receipts["Amount"].sum()
total_payments = payments["Amount"].sum()

missing_receipt_refs = receipts["Reference"].isna().sum()
missing_receipt_desc = receipts["Description"].isna().sum()
missing_paid_by = receipts["Paid by"].isna().sum()

missing_payee = payments["Payee"].isna().sum()
missing_payee_value = payments.loc[
    payments["Payee"].isna(), "Amount"
].sum()

positive_receivables = staff.loc[
    staff["Accounts receivable"] > 0,
    "Accounts receivable"
].sum()

overpaid_receivables = abs(
    staff.loc[
        staff["Accounts receivable"] < 0,
        "Accounts receivable"
    ].sum()
)

bank_actual_balance = bank["Actual balance"].fillna(0).sum()

control_kpis = pd.DataFrame([
    ["Total Recorded Sales", total_sales],
    ["Total Receipts", total_receipts],
    ["Total Payments", total_payments],
    ["Missing Receipt References", missing_receipt_refs],
    ["Missing Receipt Descriptions", missing_receipt_desc],
    ["Missing Paid By", missing_paid_by],
    ["Payments Without Payee", missing_payee],
    ["Value Without Payee", missing_payee_value],
    ["Positive Receivables", positive_receivables],
    ["Overpaid Balances", overpaid_receivables],
    ["Reported Bank/Cash Balance", bank_actual_balance],
], columns=["KPI", "Value"])

# ============================================================
# 5. DATA QUALITY FLAGS
# ============================================================

quality = pd.DataFrame([
    ["Expense recording", "CRITICAL",
     "Expense recording collapses from April 2026",
     "Post-April profitability requires reconciliation"],

    ["Payment Payees", "HIGH",
     f"{missing_payee:,} payments have no Payee",
     "Payment traceability is weak"],

    ["Bank reconciliation", "HIGH",
     "No bank reconciliation records",
     "Cash/bank balances require independent verification"],

    ["Receipt references", "HIGH",
     f"{missing_receipt_refs:,} receipts have no reference",
     "Receipts are difficult to trace"],

    ["Receipt descriptions", "HIGH",
     f"{missing_receipt_desc:,} receipts have no description",
     "Purpose of incoming funds is unclear"],

    ["Payment classification", "HIGH",
     "Large payment value remains classified as Other",
     "True cost structure is partially obscured"],
], columns=[
    "Area", "Risk", "Evidence", "Implication"
])

# ============================================================
# 6. EXPORT
# ============================================================

with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:

    monthly_revenue.to_excel(
        writer,
        sheet_name="Revenue by Unit",
        index=False
    )

    monthly_cash.to_excel(
        writer,
        sheet_name="Monthly Cash Flow",
        index=False
    )

    cost_summary.to_excel(
        writer,
        sheet_name="Cost Summary",
        index=False
    )

    monthly_cost.to_excel(
        writer,
        sheet_name="Monthly Costs",
        index=False
    )

    control_kpis.to_excel(
        writer,
        sheet_name="Control KPIs",
        index=False
    )

    quality.to_excel(
        writer,
        sheet_name="Data Quality",
        index=False
    )

print("\nDASHBOARD DATA LAYER COMPLETE")
print("=" * 70)
print(f"Sales:      ₦{total_sales:,.2f}")
print(f"Receipts:   ₦{total_receipts:,.2f}")
print(f"Payments:   ₦{total_payments:,.2f}")
print(f"Payee-less: {missing_payee:,} transactions")
print(f"Bank/Cash:  ₦{bank_actual_balance:,.2f}")

print("\nOutput:")
print(OUTPUT)