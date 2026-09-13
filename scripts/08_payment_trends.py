import pandas as pd

file = "data/location_dataset_clean.xlsx"

df = pd.read_excel(file, sheet_name="payments")

df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.strftime("%Y_%m")

df["Description"] = (
    df["Description"]
    .fillna("BLANK")
    .astype(str)
    .str.strip()
)

monthly = (
    df.groupby(["Month", "Description"])["Amount"]
    .sum()
    .reset_index()
)

# Top 10 payment descriptions for every month
monthly["Rank"] = (
    monthly.groupby("Month")["Amount"]
    .rank(method="first", ascending=False)
)

top10 = monthly[monthly["Rank"] <= 10].copy()

top10 = top10.sort_values(
    ["Month", "Amount"],
    ascending=[True, False]
)

print("\nTOP 10 PAYMENT DESCRIPTIONS BY MONTH")
print(top10.to_string(index=False))

top10.to_excel(
    "outputs/top_payment_descriptions_monthly.xlsx",
    index=False
)

print("\nSaved to: outputs/top_payment_descriptions_monthly.xlsx")