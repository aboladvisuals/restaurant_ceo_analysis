import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# 5 QUESTIONS EVERY CEO WANTS ANSWERED
# ============================================================

ceo_answers = pd.DataFrame([
    {
        "Question": "1. Where is the money coming from?",
        "Finding": "Restaurant is the core revenue engine",
        "Evidence": "Restaurant generated 42.4% of recorded sales. Restaurant + Club/Lounge generated 66.5%.",
        "Why It Matters": "These are the most important revenue engines and should receive the strongest performance monitoring.",
        "Management Action": "Track Restaurant and Club/Lounge revenue monthly, including volume, average transaction value and major revenue swings."
    },
    {
        "Question": "2. Where is the money going?",
        "Finding": "Food & Kitchen and Beverages dominate identifiable payment spend",
        "Evidence": "Food & Kitchen: ₦735.6m (34.8%). Beverages: ₦510.0m (24.1%). Combined: approximately 58.9% of payments.",
        "Why It Matters": "Purchasing, stock control, supplier pricing and wastage in these areas can materially affect profitability.",
        "Management Action": "Introduce tighter purchasing, stock and supplier controls for food and beverages."
    },
    {
        "Question": "3. Are we actually profitable?",
        "Finding": "Profitability cannot be reliably assessed after April 2026",
        "Evidence": "February 2026 recorded a ₦16.1m loss. Expenses then fell from ₦58.45m in March to ₦2.07m in April and below ₦1m in May-July.",
        "Why It Matters": "The extremely high reported margins from April onward are not reliable evidence of genuine profitability.",
        "Management Action": "Reconcile April 2026 onward before management relies on reported profit figures."
    },
    {
        "Question": "4. Where is management exposed?",
        "Finding": "Transaction traceability and reconciliation controls are weak",
        "Evidence": "19,146 payments lack Payees, representing approximately ₦2.10bn. There are zero bank reconciliation records. 33,605 receipts lack references.",
        "Why It Matters": "Management has limited ability to independently trace, verify and reconcile a large volume of financial transactions.",
        "Management Action": "Make Payee, receipt reference and transaction description mandatory and perform monthly bank reconciliation."
    },
    {
        "Question": "5. What should management do first?",
        "Finding": "Fix financial recording and control before optimising reported profit",
        "Evidence": "Expense recording collapsed from April 2026 and approximately ₦556.3m of payment spend remains classified as Other.",
        "Why It Matters": "Poor recording can hide the true cost structure and make profitability analysis misleading.",
        "Management Action": "1) Reconcile Apr-2026 onward. 2) Restore complete expense recording. 3) Reclassify major Other payments. 4) Implement monthly control review."
    }
])

# ============================================================
# PRIORITY ROADMAP
# ============================================================

roadmap = pd.DataFrame([
    {
        "Phase": "1",
        "Priority": "CRITICAL",
        "Action": "Reconcile April 2026 onward",
        "Objective": "Establish the true financial position",
        "Timing": "Immediate"
    },
    {
        "Phase": "2",
        "Priority": "HIGH",
        "Action": "Restore complete expense recording",
        "Objective": "Make monthly profitability reliable",
        "Timing": "Immediate"
    },
    {
        "Phase": "3",
        "Priority": "HIGH",
        "Action": "Mandatory Payee + receipt references",
        "Objective": "Improve transaction traceability",
        "Timing": "Within 30 days"
    },
    {
        "Phase": "4",
        "Priority": "HIGH",
        "Action": "Monthly bank reconciliation",
        "Objective": "Validate reported cash and bank balances",
        "Timing": "Monthly"
    },
    {
        "Phase": "5",
        "Priority": "HIGH",
        "Action": "Reclassify major Other payments",
        "Objective": "Understand the true cost structure",
        "Timing": "Within 30 days"
    },
    {
        "Phase": "6",
        "Priority": "MEDIUM",
        "Action": "Strengthen food and beverage cost controls",
        "Objective": "Protect the largest identifiable spending areas",
        "Timing": "Ongoing"
    }
])

# ============================================================
# KEY NUMBERS
# ============================================================

key_numbers = pd.DataFrame([
    {"Metric": "Recorded sales", "Value": "₦2.888bn"},
    {"Metric": "Total payments", "Value": "₦2.123bn"},
    {"Metric": "Restaurant share of sales", "Value": "42.4%"},
    {"Metric": "Restaurant + Club/Lounge share", "Value": "66.5%"},
    {"Metric": "Food & Kitchen payments", "Value": "₦735.6m"},
    {"Metric": "Beverage payments", "Value": "₦510.0m"},
    {"Metric": "Food + Beverage share of payments", "Value": "58.9%"},
    {"Metric": "Unclassified/Other payments", "Value": "₦556.3m"},
    {"Metric": "Payments without Payee", "Value": "₦2.10bn"},
    {"Metric": "Receipts without reference", "Value": "33,605"},
    {"Metric": "Reported bank/cash actual balance", "Value": "₦795.17m"},
    {"Metric": "Reported February 2026 loss", "Value": "₦16.10m"},
])

# ============================================================
# EXPORT
# ============================================================

output_file = OUTPUT_DIR / "ceo_executive_summary.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    ceo_answers.to_excel(
        writer,
        sheet_name="5 CEO Answers",
        index=False
    )

    roadmap.to_excel(
        writer,
        sheet_name="Priority Roadmap",
        index=False
    )

    key_numbers.to_excel(
        writer,
        sheet_name="Key Numbers",
        index=False
    )

print("\nCEO EXECUTIVE SUMMARY COMPLETE")
print("=" * 70)

print("\n5 CEO ANSWERS:\n")
print(ceo_answers.to_string(index=False))

print("\n\nPRIORITY ROADMAP:\n")
print(roadmap.to_string(index=False))

print("\n\nSaved to:")
print(output_file)