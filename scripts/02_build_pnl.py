import pandas as pd

input_file = "data/location_dataset_clean.xlsx"
output_file = "data/pnl_clean.xlsx"

raw = pd.read_excel(
    input_file,
    sheet_name="PNL_combined _months",
    header=None
)

# Extract the P&L line items
pnl = raw.iloc[6:31, [0, 1]].copy()
pnl.columns = ["Category", "Amount"]

# Remove blank rows
pnl = pnl.dropna(subset=["Category"])

# Convert amounts to numeric
pnl["Amount"] = pd.to_numeric(pnl["Amount"], errors="coerce")

# Save clean P&L
pnl.to_excel(output_file, index=False)

print("\nCLEAN P&L")
print(pnl.to_string(index=False))

print("\nSaved to:", output_file)