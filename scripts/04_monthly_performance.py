import pandas as pd

input_file = "data/monthly_pnl_clean.xlsx"
output_file = "outputs/monthly_performance.csv"

df = pd.read_excel(input_file)

months = df["Month"].unique()

rows = []

for month in months:
    m = df[df["Month"] == month]

    revenue = m.loc[
        m["Category"] == "Total — Income", "Amount"
    ].sum()

    expenses = m.loc[
        m["Category"] == "Total — Less: Expenses", "Amount"
    ].sum()

    profit = m.loc[
        m["Category"] == "Net profit (loss)", "Amount"
    ].sum()

    margin = (profit / revenue * 100) if revenue else 0

    rows.append({
        "Month": month,
        "Revenue": revenue,
        "Expenses": expenses,
        "Net Profit": profit,
        "Profit Margin %": round(margin, 2)
    })

summary = pd.DataFrame(rows)

summary.to_csv(output_file, index=False)

print("\nMONTHLY CEO PERFORMANCE")
print(summary.to_string(index=False))

print("\nSaved to:", output_file)