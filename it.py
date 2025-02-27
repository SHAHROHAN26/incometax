import streamlit as st
import pandas as pd

def calculate_tax_old_regime(income, deductions, year):
    taxable_income = max(0, income - deductions)
    
    if year == "2024-25":
        slabs = [(250000, 0), (500000, 0.05), (1000000, 0.2), (float('inf'), 0.3)]
    else:  # FY 2025-26 (Same slabs as previous year for old regime)
        slabs = [(250000, 0), (500000, 0.05), (1000000, 0.2), (float('inf'), 0.3)]

    tax = 0
    prev_limit = 0
    for limit, rate in slabs:
        if taxable_income > prev_limit:
            tax += (min(limit, taxable_income) - prev_limit) * rate
        prev_limit = limit

    return tax

def calculate_tax_new_regime(income, year):
    if year == "2024-25":
        slabs = [(300000, 0), (600000, 0.05), (900000, 0.1), (1200000, 0.15), (1500000, 0.2), (float('inf'), 0.3)]
        rebate_limit = 700000
        rebate_amount = 25000
        standard_deduction = 50000
    else:  # FY 2025-26 (Updated slabs)
        slabs = [(400000, 0), (800000, 0.05), (1200000, 0.1), (1600000, 0.15), (2000000, 0.2), (2400000, 0.25), (float('inf'), 0.3)]
        rebate_limit = 1200000
        rebate_amount = 60000
        standard_deduction = 75000

    taxable_income = max(0, income - standard_deduction)
    
    tax = 0
    prev_limit = 0
    for limit, rate in slabs:
        if taxable_income > prev_limit:
            tax += (min(limit, taxable_income) - prev_limit) * rate
        prev_limit = limit

    if taxable_income <= rebate_limit:
        tax = max(0, tax - rebate_amount)

    return tax

st.title("Advanced Tax Calculator (AY 2024-25 & 2025-26)")

# Select financial year
year = st.radio("Select Financial Year", ("2024-25", "2025-26"))

income = st.number_input("Enter Annual Income (₹)", min_value=0, step=10000)

gst_applicable = st.radio("Is GST applicable?", ("No", "Yes"))
gst_amount = st.number_input("Enter GST amount (₹)", min_value=0, step=1000) if gst_applicable == "Yes" else 0

total_income = income + gst_amount

tax_regime = st.radio("Select Tax Regime", ("Old", "New"))

if tax_regime == "Old":
    st.subheader("Enter Deductions:")
    deduction_80C = st.number_input("80C (PPF, EPF, LIC, etc.) (₹)", min_value=0, step=1000)
    deduction_80D = st.number_input("80D (Health Insurance Premium) (₹)", min_value=0, step=1000)
    home_loan_interest = st.number_input("Home Loan Interest (₹)", min_value=0, step=1000)
    hra = st.number_input("House Rent Allowance (HRA) (₹)", min_value=0, step=1000)

    total_deductions = deduction_80C + deduction_80D + home_loan_interest + hra
    tax_old = calculate_tax_old_regime(total_income, total_deductions, year)
    tax_new = calculate_tax_new_regime(total_income, year)  # Compare with new regime
else:
    tax_old = calculate_tax_old_regime(total_income, 0, year)  # Compare with old regime without deductions
    tax_new = calculate_tax_new_regime(total_income, year)

st.subheader("Tax Calculation Summary")
st.write(f"Total Income (Including GST): ₹{total_income}")
st.write(f"Tax under Old Regime: ₹{tax_old:.2f}")
st.write(f"Tax under New Regime: ₹{tax_new:.2f}")

if tax_old < tax_new:
    st.success(f"Old Regime is more beneficial! You save ₹{tax_new - tax_old:.2f}.")
elif tax_new < tax_old:
    st.success(f"New Regime is more beneficial! You save ₹{tax_old - tax_new:.2f}.")
else:
    st.info("Both regimes yield the same tax amount.")

# Comparison Table
comparison_data = {
    "Regime": ["Old", "New"],
    "Tax Amount (₹)": [tax_old, tax_new]
}
df_comparison = pd.DataFrame(comparison_data)

st.subheader("Comparison Table: Old vs. New Regime")
st.table(df_comparison)

