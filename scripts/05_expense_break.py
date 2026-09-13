import pandas as pd

df = pd.read_excel("data/monthly_pnl_clean.xlsx")

expense_categories = [
    "Admin",
    "Bank Charges",
    "Beverages",
    "Food Items",
    "Haulages",
    "Maintenance, Housekeeping & Renovations",
    "Others",
    "Power & Electricity",
    "Rental",
    "Sales & Marketing",
    "Staff welfare",
    "Tax Fees",
    "Utility"
]

expenses = df[df["Category"].isin(expense_categories)].copy()

summary = (
    expenses
    .pivot_table(
        index="Category",
        columns="Month",
        values="Amount",
        aggfunc="sum",
        fill_value=0
    )
)

print("\nEXPENSE CATEGORY — MONTHLY COMPARISON")
print(summary.to_string())

summary.to_excel("outputs/expense_break_analysis.xlsx")

print("\nSaved to: outputs/expense_break_analysis.xlsx")