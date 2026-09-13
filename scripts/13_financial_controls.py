import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "location_dataset_clean.xlsx"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

sales = pd.read_excel(
    INPUT_FILE,
    sheet_name="sales_invoice"
)

receipts = pd.read_excel(
    INPUT_FILE,
    sheet_name="receipts"
)

payments = pd.read_excel(
    INPUT_FILE,
    sheet_name="payments"
)

customers = pd.read_excel(
    INPUT_FILE,
    sheet_name="customers_but_staffs"
)

bank = pd.read_excel(
    INPUT_FILE,
    sheet_name="Bank&cash_accounts"
)

# ============================================================
# BASIC CLEANING
# ============================================================

sales["Invoice Amount"] = pd.to_numeric(
    sales["Invoice Amount"],
    errors="coerce"
).fillna(0)

sales["Balance due"] = pd.to_numeric(
    sales["Balance due"],
    errors="coerce"
).fillna(0)

receipts["Amount"] = pd.to_numeric(
    receipts["Amount"],
    errors="coerce"
).fillna(0)

payments["Amount"] = pd.to_numeric(
    payments["Amount"],
    errors="coerce"
).fillna(0)

customers["Accounts receivable"] = pd.to_numeric(
    customers["Accounts receivable"],
    errors="coerce"
).fillna(0)

# ============================================================
# 1. RECEIVABLES
# ============================================================

total_receivables = customers[
    customers["Accounts receivable"] > 0
]["Accounts receivable"].sum()

overpaid_customers = customers[
    customers["Accounts receivable"] < 0
]

unpaid_customers = customers[
    customers["Accounts receivable"] > 0
]

# ============================================================
# 2. SALES INVOICE STATUS
# ============================================================

status_summary = (
    sales.groupby("Status", as_index=False)
    .agg(
        Transactions=("Invoice Amount", "count"),
        Invoice_Value=("Invoice Amount", "sum"),
        Balance_Due=("Balance due", "sum")
    )
)

overpaid_invoices = sales[
    sales["Balance due"] < 0
]

overdue_invoices = sales[
    sales["Status"].astype(str).str.lower() == "overdue"
]

# ============================================================
# 3. RECEIPT DATA QUALITY
# ============================================================

receipt_reference_missing = receipts["Reference"].isna().sum()
receipt_description_missing = receipts["Description"].isna().sum()
receipt_paidby_missing = receipts["Paid by"].isna().sum()

receipt_total = len(receipts)

# ============================================================
# 4. PAYMENT DATA QUALITY
# ============================================================

payment_payee_missing = payments["Payee"].isna().sum()
payment_description_missing = payments["Description"].isna().sum()

payment_total = len(payments)

payments_without_payee_value = payments.loc[
    payments["Payee"].isna(),
    "Amount"
].sum()

total_payment_value = payments["Amount"].sum()

# ============================================================
# 5. BANK RECONCILIATION
# ============================================================

bank_reconciliation_note = (
    "No bank reconciliation records were found in the dataset."
)

# Actual balances
bank_actual_balance = pd.to_numeric(
    bank["Actual balance"],
    errors="coerce"
).fillna(0).sum()

# ============================================================
# 6. SALES / RECEIPTS RECONCILIATION
# ============================================================

total_sales = sales["Invoice Amount"].sum()
total_receipts = receipts["Amount"].sum()

receipt_vs_sales_difference = (
    total_receipts - total_sales
)

# ============================================================
# 7. CONTROL FINDINGS TABLE
# ============================================================

findings = pd.DataFrame([
    {
        "Control Area": "Receivables",
        "Finding": "Positive outstanding customer/staff balances exist",
        "Value": total_receivables,
        "Risk": "Medium",
        "Management Action":
            "Review outstanding balances and establish collection ownership"
    },
    {
        "Control Area": "Overpaid invoices",
        "Finding": "Invoices have negative balances",
        "Value": overpaid_invoices["Balance due"].abs().sum(),
        "Risk": "Medium",
        "Management Action":
            "Investigate overpayments and confirm whether they represent credits, corrections or data-entry issues"
    },
    {
        "Control Area": "Receipt references",
        "Finding": "Receipt references are missing",
        "Value": receipt_reference_missing,
        "Risk": "High",
        "Management Action":
            "Require unique references for every receipt"
    },
    {
        "Control Area": "Receipt descriptions",
        "Finding": "Receipt descriptions are missing",
        "Value": receipt_description_missing,
        "Risk": "High",
        "Management Action":
            "Require meaningful descriptions for receipts"
    },
    {
        "Control Area": "Receipt collector",
        "Finding": "Paid-by information is missing",
        "Value": receipt_paidby_missing,
        "Risk": "Medium",
        "Management Action":
            "Require staff/collector identification where applicable"
    },
    {
        "Control Area": "Payment payees",
        "Finding": "Payment payees are largely missing",
        "Value": payments_without_payee_value,
        "Risk": "High",
        "Management Action":
            "Require supplier/payee name for every payment"
    },
    {
        "Control Area": "Payment descriptions",
        "Finding": "Some payments have no description",
        "Value": payment_description_missing,
        "Risk": "Medium",
        "Management Action":
            "Require payment purpose/category"
    },
    {
        "Control Area": "Bank reconciliation",
        "Finding": "No bank reconciliation records",
        "Value": bank_actual_balance,
        "Risk": "High",
        "Management Action":
            "Introduce monthly bank and cash reconciliation"
    },
    {
        "Control Area": "Expense recording",
        "Finding": "Recorded expenses collapse from April 2026",
        "Value": 0,
        "Risk": "Critical",
        "Management Action":
            "Investigate accounting process change and reconcile April 2026 onward"
    }
])

# ============================================================
# 8. CONTROL METRICS
# ============================================================

metrics = pd.DataFrame([
    {
        "Metric": "Total sales invoices",
        "Value": total_sales
    },
    {
        "Metric": "Total receipts",
        "Value": total_receipts
    },
    {
        "Metric": "Receipts minus sales invoices",
        "Value": receipt_vs_sales_difference
    },
    {
        "Metric": "Outstanding receivables",
        "Value": total_receivables
    },
    {
        "Metric": "Overpaid invoice balance",
        "Value": overpaid_invoices["Balance due"].abs().sum()
    },
    {
        "Metric": "Receipts missing references",
        "Value": receipt_reference_missing
    },
    {
        "Metric": "Receipts missing descriptions",
        "Value": receipt_description_missing
    },
    {
        "Metric": "Receipts missing Paid by",
        "Value": receipt_paidby_missing
    },
    {
        "Metric": "Payments missing Payee",
        "Value": payment_payee_missing
    },
    {
        "Metric": "Value of payments missing Payee",
        "Value": payments_without_payee_value
    },
    {
        "Metric": "Bank/Cash actual balance",
        "Value": bank_actual_balance
    }
])

# ============================================================
# EXPORT
# ============================================================

output_file = OUTPUT_DIR / "financial_controls_analysis.xlsx"

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    findings.to_excel(
        writer,
        sheet_name="Control Findings",
        index=False
    )

    metrics.to_excel(
        writer,
        sheet_name="Control Metrics",
        index=False
    )

    status_summary.to_excel(
        writer,
        sheet_name="Invoice Status",
        index=False
    )

# ============================================================
# DISPLAY
# ============================================================

print("\nFINANCIAL CONTROL ANALYSIS COMPLETE")
print("=" * 65)

print("\nCONTROL FINDINGS:\n")
print(findings.to_string(index=False))

print("\n\nKEY CONTROL METRICS:\n")
print(metrics.to_string(index=False))

print("\n\nInvoice Status:")
print(status_summary.to_string(index=False))

print("\n\nSaved to:")
print(output_file)