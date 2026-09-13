import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# MANAGEMENT ACTION PLAN
# ============================================================

actions = pd.DataFrame([
    {
        "Priority": 1,
        "Risk Level": "CRITICAL",
        "Issue": "Expense recording collapse from April 2026",
        "Evidence": "Monthly recorded expenses fell from ₦58.45m in March 2026 to ₦2.07m in April and below ₦1m in May-July",
        "Business Impact": "Reported profit from April 2026 onward is unreliable",
        "Recommended Action": "Perform a full reconciliation of all expenses from April 2026 onward and identify the accounting-process change",
        "Owner": "Finance / Management",
        "Timeline": "Immediate"
    },
    {
        "Priority": 2,
        "Risk Level": "HIGH",
        "Issue": "Payments lack Payee information",
        "Evidence": "19,146 payments lack Payee information, representing approximately ₦2.10bn",
        "Business Impact": "Weak payment traceability and difficulty verifying suppliers and payment accountability",
        "Recommended Action": "Make Payee/Supplier mandatory for every payment",
        "Owner": "Finance",
        "Timeline": "Immediate"
    },
    {
        "Priority": 3,
        "Risk Level": "HIGH",
        "Issue": "No bank reconciliation records",
        "Evidence": "Zero bank reconciliation records despite approximately ₦795.17m in bank/cash actual balances",
        "Business Impact": "Management cannot rely solely on the accounting system to confirm cash and bank accuracy",
        "Recommended Action": "Introduce monthly bank and cash reconciliation with management sign-off",
        "Owner": "Finance",
        "Timeline": "Immediate"
    },
    {
        "Priority": 4,
        "Risk Level": "HIGH",
        "Issue": "Receipt references missing",
        "Evidence": "33,605 receipts have no reference",
        "Business Impact": "Transactions are difficult to trace and audit",
        "Recommended Action": "Require a unique reference for every receipt",
        "Owner": "Finance / Operations",
        "Timeline": "Within 30 days"
    },
    {
        "Priority": 5,
        "Risk Level": "HIGH",
        "Issue": "Receipt descriptions missing",
        "Evidence": "24,159 receipts have no description",
        "Business Impact": "Limited visibility into the purpose of incoming funds",
        "Recommended Action": "Make receipt descriptions mandatory and standardise receipt categories",
        "Owner": "Finance",
        "Timeline": "Within 30 days"
    },
    {
        "Priority": 6,
        "Risk Level": "HIGH",
        "Issue": "Large unclassified payment spend",
        "Evidence": "Approximately ₦556.3m of payments is currently classified as Other",
        "Business Impact": "Management cannot accurately assess the underlying cost structure",
        "Recommended Action": "Review and reclassify major payment descriptions and introduce standard purchasing categories",
        "Owner": "Finance / Procurement",
        "Timeline": "Within 30 days"
    },
    {
        "Priority": 7,
        "Risk Level": "MEDIUM",
        "Issue": "Outstanding receivables",
        "Evidence": "Approximately ₦5.74m in positive outstanding balances",
        "Business Impact": "Cash may be tied up in unpaid balances",
        "Recommended Action": "Produce an aged receivables list and assign collection responsibility",
        "Owner": "Finance / Operations",
        "Timeline": "Within 30 days"
    },
    {
        "Priority": 8,
        "Risk Level": "MEDIUM",
        "Issue": "Overpaid invoices",
        "Evidence": "₦7.73m of negative invoice balances across 4,244 transactions",
        "Business Impact": "Potential credits, corrections or data-entry issues require clarification",
        "Recommended Action": "Review overpaid balances and document the reason for each material balance",
        "Owner": "Finance",
        "Timeline": "Within 30 days"
    },
    {
        "Priority": 9,
        "Risk Level": "MEDIUM",
        "Issue": "High revenue volatility",
        "Evidence": "Monthly revenue fluctuates significantly across business units",
        "Business Impact": "Planning, staffing and purchasing become difficult",
        "Recommended Action": "Introduce monthly business-unit performance reviews and investigate major revenue swings",
        "Owner": "Management / Operations",
        "Timeline": "Monthly"
    }
])

# ============================================================
# CEO SUMMARY
# ============================================================

summary = pd.DataFrame([
    {
        "Metric": "Largest revenue engine",
        "Result": "Restaurant",
        "Evidence": "42.4% of recorded sales"
    },
    {
        "Metric": "Revenue concentration",
        "Result": "Restaurant + Club/Lounge",
        "Evidence": "66.5% of recorded sales"
    },
    {
        "Metric": "Worst reliable profitability month",
        "Result": "February 2026",
        "Evidence": "₦16.10m reported loss"
    },
    {
        "Metric": "Largest identifiable payment category",
        "Result": "Food & Kitchen",
        "Evidence": "₦735.6m / 34.8% of payments"
    },
    {
        "Metric": "Second-largest identifiable payment category",
        "Result": "Beverages",
        "Evidence": "₦510.0m / 24.1% of payments"
    },
    {
        "Metric": "Major unclassified spend",
        "Result": "Other",
        "Evidence": "₦556.3m / 26.3% of payments"
    },
    {
        "Metric": "Critical accounting issue",
        "Result": "Expense recording collapse",
        "Evidence": "Begins April 2026"
    }
])

# ============================================================
# EXPORT
# ============================================================

output_file = OUTPUT_DIR / "management_action_plan.xlsx"

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    actions.to_excel(
        writer,
        sheet_name="Action Plan",
        index=False
    )

    summary.to_excel(
        writer,
        sheet_name="CEO Summary",
        index=False
    )

print("\nMANAGEMENT ACTION PLAN COMPLETE")
print("=" * 65)

print("\nCEO SUMMARY:\n")
print(summary.to_string(index=False))

print("\n\nPRIORITY ACTIONS:\n")
print(actions.to_string(index=False))

print("\n\nSaved to:")
print(output_file)