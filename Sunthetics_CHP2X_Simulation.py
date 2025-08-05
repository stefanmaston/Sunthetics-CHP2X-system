import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

# Currency conversion rates (as of latest)
CURRENCY_RATES = {
    'SEK': 1.0,
    'EUR': 0.087,  # 1 SEK = 0.087 EUR
    'USD': 0.095   # 1 SEK = 0.095 USD
}

# Streamlit app
st.title("Sunthetics CHP2X Interactive Simulation")

# Currency selection
selected_currency = st.selectbox("Select Currency", ['SEK', 'EUR', 'USD'])
currency_rate = CURRENCY_RATES[selected_currency]
currency_symbol = {'SEK': 'SEK', 'EUR': '€', 'USD': '$'}[selected_currency]

# Helper function for currency formatting. Values in the app are already
# provided in the selected currency so no further conversion is required here.
def format_currency(value: float) -> str:
    """Format a numeric value with the selected currency symbol."""
    return f"{value:,.2f} {currency_symbol}"

# Calculate minimum values based on currency
min_capex = int(10000 * currency_rate)
min_share_price = int(100 * currency_rate)
min_price_per_liter = 1.0 * currency_rate

# User inputs
st.subheader("Project Parameters")
capex_per_hectare = st.number_input(f"CAPEX per hectare ({currency_symbol})", min_value=min_capex, value=int(15000000 * currency_rate), step=min_capex)
number_of_hectares = st.number_input("Number of hectares", min_value=1, value=1, step=1)

st.subheader("Production Parameters")
liters_per_hour = st.number_input("Methanol Production Rate (L/h)", min_value=1.0, value=105.0, step=1.0)
sunhours = st.slider("Annual Sun Hours (DNI)", min_value=500, max_value=3500, value=1250, step=100)
annual_production_liters_per_hectare = 6 * liters_per_hour * sunhours  # Calculate annual production
st.write(f"### Annual Methanol Production per Hectare: {annual_production_liters_per_hectare:,.0f} L/year")
project_lifetime = st.slider("Project Lifetime (years)", min_value=1, max_value=100, value=50)

st.subheader("Share Parameters")
shares_per_hectare = 15000  # Fixed number of shares per hectare
number_of_shares = number_of_hectares * shares_per_hectare
share_price = st.number_input(f"Price per share ({currency_symbol})", min_value=min_share_price, value=int(1000 * currency_rate), step=min_share_price)
st.write(f"### Number of shares: {number_of_shares:,} (15,000 shares per hectare)")

st.subheader("Financial Parameters")
revenue_sharing_percentage = st.slider("Revenue Sharing Percentage (%)", 0, 100, 50) / 100
price_per_liter = st.number_input(f"Price per liter of methanol ({currency_symbol})", min_value=min_price_per_liter, value=5.5 * currency_rate, step=0.1 * currency_rate)
st.write("""
    **Annual Price Escalation**
    - Current EU energy price trends suggest moderate annual increases
    - Based on energy transition costs, carbon pricing, and infrastructure investments
    - Historical average: 2-3% per year
    - Projected range: 1-5% per year
""")
annual_price_escalation = st.slider("Annual Price Escalation (%)", 1.0, 5.0, 2.5) / 100
build_time_years = st.slider("Build Time (years)", 0, 10, 4)
st.write("""
    **Discount Rate**
    - Based on opportunity cost of capital (no loans)
    - Risk-free rate (Swedish government bonds): ~2-3%
    - Renewable energy project risk premium: ~2-4%
    - Total reasonable range: 4-7%
""")
discount_rate = st.slider("Discount Rate (%)", 4.0, 7.0, 5.0) / 100

# Calculate investments
total_capex = capex_per_hectare * number_of_hectares
total_share_investment = share_price * number_of_shares
investment_gap = total_capex - total_share_investment
monthly_capex_payment = total_capex / (project_lifetime * 12)  # Monthly CAPEX payment over project lifetime

# Calculate base revenue
annual_revenue_base = annual_production_liters_per_hectare * price_per_liter * number_of_hectares
monthly_revenue_base = annual_revenue_base / 12

# Calculate revenue sharing based on revenue percentage
monthly_revenue_share = monthly_revenue_base * revenue_sharing_percentage
monthly_revenue_share_per_share = monthly_revenue_share / number_of_shares
total_revenue_share = monthly_revenue_share * 12 * project_lifetime
total_revenue_share_per_share = total_revenue_share / number_of_shares

# Calculate equivalent annual return rate
annual_return_rate = (monthly_revenue_share * 12) / total_share_investment

# Calculate and display revenue share verification
annual_revenue_share_per_share = monthly_revenue_share_per_share * 12
total_revenue_share_ratio = total_revenue_share / total_share_investment

st.write(f"### Total Revenue Share ({project_lifetime} years): {format_currency(total_revenue_share)}")
st.write(f"### Monthly Revenue Share per Share: {format_currency(monthly_revenue_share_per_share)}")
st.write(f"### Annual Revenue Share per Share: {format_currency(annual_revenue_share_per_share)}")
st.write(f"### Total Revenue Share per Share ({project_lifetime} years): {format_currency(total_revenue_share_per_share)}")
st.write(f"### Total Revenue Share to Investment Ratio: {total_revenue_share_ratio:.2f}x")
st.write(f"### Equivalent Annual Return Rate: {annual_return_rate:.1%}")

# Calculate monthly revenues with price escalation
monthly_revenues = []
monthly_cash_flows = [-total_capex]  # Initial investment
monthly_discount_rate = (1 + discount_rate) ** (1/12) - 1

# Display base revenue calculations
st.write(f"### Base Annual Revenue: {format_currency(annual_revenue_base)}")
st.write(f"### Base Monthly Revenue: {format_currency(monthly_revenue_base)}")

for year in range(project_lifetime):
    # Calculate escalated price for this year
    year_price = price_per_liter * (1 + annual_price_escalation) ** year
    monthly_revenue = (annual_production_liters_per_hectare * year_price * number_of_hectares) / 12
    
    # For each month in the year
    for month in range(12):
        if year < build_time_years:
            monthly_revenues.append(0)
            monthly_cash_flows.append(-monthly_capex_payment)  # Only CAPEX during build time
        else:
            monthly_revenues.append(monthly_revenue)
            # Cash flow is revenue minus CAPEX (revenue sharing is part of the return)
            monthly_cash_flow = monthly_revenue - monthly_capex_payment
            monthly_cash_flows.append(monthly_cash_flow)

# Calculate NPV with escalated prices
npv = npf.npv(monthly_discount_rate, monthly_cash_flows)

# Calculate total revenue and costs
total_revenue = sum(monthly_revenues)
total_costs = total_capex  # Only CAPEX is a cost, revenue sharing is part of the return

# Calculate revenue to CAPEX ratios
revenue_to_capex_ratio = total_revenue / total_capex
annual_revenue_to_capex_ratio = annual_revenue_base / total_capex

st.write(f"### Revenue to CAPEX Ratio: {revenue_to_capex_ratio:.2f}x")
st.write(f"### Annual Revenue to CAPEX Ratio: {annual_revenue_to_capex_ratio:.2f}x")

# LCOE Calculation
kwh_per_liter = 5
annual_energy_production = annual_production_liters_per_hectare * number_of_hectares * kwh_per_liter
total_energy_production = annual_energy_production * project_lifetime
lcoe = total_costs / total_energy_production

# Output results
st.subheader("Investment Summary")
st.write(f"### Total CAPEX Required: {format_currency(total_capex)}")
st.write(f"### Monthly CAPEX Payment: {format_currency(monthly_capex_payment)}")
st.write(f"### Total Share Investment: {format_currency(total_share_investment)}")
st.write(f"### Investment Gap: {format_currency(investment_gap)}")

st.subheader("Monthly Financial Summary")
st.write(f"### Initial Monthly Revenue: {format_currency(monthly_revenues[build_time_years*12])}")
st.write(f"### Final Monthly Revenue: {format_currency(monthly_revenues[-1])}")
st.write(f"### Monthly Revenue Sharing: {format_currency(monthly_revenue_share)}")
st.write(f"### Monthly Net Revenue (Year 1): {format_currency(monthly_revenues[build_time_years*12] - monthly_capex_payment)}")
st.write(f"### Monthly Company Earnings (Year 1): {format_currency(monthly_revenues[build_time_years*12] - monthly_capex_payment - monthly_revenue_share)}")

st.subheader("Long-term Analysis")
st.write(f"### Net Present Value ({project_lifetime} years): {format_currency(npv)}")
st.write(f"### Levelized Cost of Energy (LCOE): {format_currency(lcoe)}/kWh")
st.write(f"### Total Energy Production ({project_lifetime} years): {total_energy_production:,.0f} kWh")
st.write(f"### Total Revenue ({project_lifetime} years): {format_currency(total_revenue)}")
st.write(f"### Total Costs ({project_lifetime} years): {format_currency(total_costs)}")
st.write(f"### Total Company Earnings ({project_lifetime} years): {format_currency(total_revenue - total_costs - total_revenue_share)}")

# Time series for visualization
months = project_lifetime * 12
build_time_months = build_time_years * 12
cumulative_cash_flow = np.cumsum(monthly_cash_flows[1:])  # Exclude initial investment

# DataFrame for plotting
data = {
    "Month": list(range(months)),
    "Monthly Revenue": monthly_revenues,
    "Cumulative Cash Flow": cumulative_cash_flow
}
df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(df["Month"], df["Cumulative Cash Flow"], label=f'Cumulative Cash Flow ({currency_symbol})', color='green')
plt.axvline(build_time_months, color='red', linestyle='--', label='Build Time')
plt.title("Sunthetics CHP2X Cash Flow Simulation")
plt.xlabel("Months")
plt.ylabel(f"Cumulative Cash Flow ({currency_symbol})")
plt.grid(True)
plt.legend()
st.pyplot(plt)
