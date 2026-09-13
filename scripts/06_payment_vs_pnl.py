import pandas as pd

file = "data/location_dataset_clean.xlsx"

payments = pd.read_excel(file, sheet_name="payments")
pnl = pd.read_excel("data/monthly_pnl_clean.xlsx")

payments["Date"] = pd.to_datetime(payments["Date"])
payments["Month"] = payments["Date"].dt.strftime("%Y_%m")

payment_monthly = (
    payments.groupby("Month")["Amount"]
    .sum()
    .reset_index()
    .rename(columns={"Amount": "Payments"})
)

pnl_summary = (
    pnl[pnl["Category"].isin([
        "Total — Income",
        "Total — Less: Expenses"
    ])]
    .pivot(index="Month", columns="Category", values="Amount")
    .reset_index()
)

pnl_summary = pnl_summary.rename(columns={
    "Total — Income": "Revenue",
    "Total — Less: Expenses": "PNL Expenses"
})

comparison = pnl_summary.merge(
    payment_monthly,
    on="Month",
    how="left"
)

comparison["Payments"] = comparison["Payments"].fillna(0)

print("\nPAYMENTS VS P&L EXPENSES")
print(comparison.to_string(index=False))

comparison.to_excel(
    "outputs/payments_vs_pnl.xlsx",
    index=False
)

print("\nSaved to: outputs/payments_vs_pnl.xlsx")