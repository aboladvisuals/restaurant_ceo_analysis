import pandas as pd

input_file = "data/location_dataset_clean.xlsx"
output_file = "outputs/payment_categories.xlsx"

df = pd.read_excel(input_file, sheet_name="payments")

df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.strftime("%Y_%m")

# Normalise descriptions
desc = df["Description"].fillna("").astype(str).str.lower().str.strip()

def classify(x):
    if any(k in x for k in [
        "chicken", "beef", "goat", "catfish", "turkey",
        "fish", "titus", "eggs", "foodstuff", "vegg",
        "yam", "rice", "pepper", "tomato", "onion"
    ]):
        return "Food"

    if any(k in x for k in [
        "drink", "beer", "beverage", "water", "soft drink"
    ]):
        return "Beverages"

    if any(k in x for k in [
        "diesel", "fuel", "petrol", "gas", "power", "electric"
    ]):
        return "Energy & Fuel"

    if any(k in x for k in [
        "maintenance", "repair", "plumbing", "carpentry",
        "renovation", "equipment"
    ]):
        return "Maintenance"

    if any(k in x for k in [
        "event", "haulage", "transport", "delivery",
        "logistics"
    ]):
        return "Operations"

    if any(k in x for k in [
        "salary", "welfare", "staff", "worker"
    ]):
        return "Staff"

    return "Other"

df["Payment Category"] = desc.apply(classify)

summary = (
    df.groupby("Payment Category")["Amount"]
    .agg(["sum", "count"])
    .reset_index()
    .sort_values("sum", ascending=False)
)

summary.columns = [
    "Payment Category",
    "Total Amount",
    "Transaction Count"
]

print("\nPAYMENT CATEGORY ANALYSIS")
print(summary.to_string(index=False))

summary.to_excel(output_file, index=False)

print("\nSaved to:", output_file)