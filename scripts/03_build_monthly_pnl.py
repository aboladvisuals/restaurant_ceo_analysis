import pandas as pd

input_file = "data/LOCATION_MONTHLY_PNL.xlsx"
output_file = "data/monthly_pnl_clean.xlsx"

records = []

for sheet in pd.ExcelFile(input_file).sheet_names:
    raw = pd.read_excel(input_file, sheet_name=sheet, header=None)

    # Find the date/value column
    date_value = raw.iloc[5, 1]

    # Extract relevant rows
    for _, row in raw.iloc[6:33].iterrows():
        category = row.iloc[0]
        amount = row.iloc[1]

        if pd.notna(category):
            records.append({
                "Month": sheet.replace("pnl_", ""),
                "Category": category,
                "Amount": pd.to_numeric(amount, errors="coerce")
            })

monthly = pd.DataFrame(records)

monthly.to_excel(output_file, index=False)

print("\nMONTHLY P&L CREATED")
print(monthly.head(20).to_string(index=False))

print("\nMonths:", monthly["Month"].unique())
print("\nSaved to:", output_file)