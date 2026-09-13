import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "LOCATION_MONTHLY_PNL.xlsx"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

xls = pd.ExcelFile(INPUT_FILE)

results = []

for sheet in xls.sheet_names:

    raw = pd.read_excel(
        INPUT_FILE,
        sheet_name=sheet,
        header=None
    )

    # Column 0 = P&L labels
    # Column 1 = values
    labels = raw.iloc[:, 0].astype(str).str.strip()

    def get_value(label):
        matches = raw[
            labels.str.lower() == label.lower()
        ]

        if matches.empty:
            return 0

        value = pd.to_numeric(
            matches.iloc[0, 1],
            errors="coerce"
        )

        return 0 if pd.isna(value) else value

    revenue = get_value("Total — Income")

    expenses = get_value("Total — Less: Expenses")

    net_profit = get_value("Net profit (loss)")

    profit_margin = (
        net_profit / revenue * 100
        if revenue != 0 else 0
    )

    results.append({
        "Month": sheet.replace("pnl_", ""),
        "Revenue": revenue,
        "Expenses": expenses,
        "Net Profit": net_profit,
        "Profit Margin %": profit_margin
    })


# --------------------------------
# CREATE DATAFRAME
# --------------------------------

profitability = pd.DataFrame(results)

profitability = profitability.sort_values(
    "Month"
).reset_index(drop=True)


# --------------------------------
# ADD GROWTH / COST METRICS
# --------------------------------

profitability["Revenue Growth %"] = (
    profitability["Revenue"]
    .pct_change()
    * 100
)

profitability["Expense Ratio %"] = (
    profitability["Expenses"]
    / profitability["Revenue"]
    * 100
)


# --------------------------------
# DATA QUALITY FLAG
# --------------------------------

profitability["Data Quality"] = profitability["Month"].apply(
    lambda x:
        "REVIEW - Expense recording collapse"
        if x >= "2026-04"
        else "Usable"
)


# --------------------------------
# PROFITABILITY RANKING
# --------------------------------

ranking = profitability.sort_values(
    "Net Profit",
    ascending=False
).reset_index(drop=True)


# --------------------------------
# EXPORT
# --------------------------------

output_file = OUTPUT_DIR / "profitability_analysis.xlsx"

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    profitability.to_excel(
        writer,
        sheet_name="Monthly Profitability",
        index=False
    )

    ranking.to_excel(
        writer,
        sheet_name="Profitability Ranking",
        index=False
    )


# --------------------------------
# DISPLAY
# --------------------------------

print("\nPROFITABILITY ANALYSIS COMPLETE")
print("-" * 60)

print("\nMONTHLY PROFITABILITY:\n")

print(
    profitability.to_string(index=False)
)

print("\n\nTOP 10 PROFITABLE MONTHS:\n")

print(
    ranking.head(10).to_string(index=False)
)

print("\n\nLOWEST 10 MONTHS:\n")

print(
    ranking.tail(10).to_string(index=False)
)

print("\nSaved to:")
print(output_file)