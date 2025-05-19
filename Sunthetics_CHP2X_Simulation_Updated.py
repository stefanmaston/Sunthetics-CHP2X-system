
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Streamlit app
st.title("Sunthetics CHP2X Interactive Simulation")

# User inputs
investment_amount = st.number_input("Investment Amount (SEK)", min_value=10000, value=100000, step=10000)
annual_return_rate = st.slider("Annual Return Rate (%)", 5, 25, 15) / 100
price_per_liter = st.number_input("Price per liter of methanol (€)", min_value=0.10, value=0.55, step=0.01)
build_time_years = st.slider("Build Time (years)", 0, 10, 4)

# CHP2X Parameters
capex_per_hectare = 15000000  # 15 MSEK per hektar
annual_production_liters_per_hectare = 735000
monthly_revenue_per_hectare = (annual_production_liters_per_hectare * price_per_liter) / 12

# Simulation calculations
monthly_return_needed = investment_amount * annual_return_rate / 12
percentage_needed = (monthly_return_needed / monthly_revenue_per_hectare) * 100

# Hektarberäkning för att täcka utbetalning
hectares_required = monthly_return_needed / monthly_revenue_per_hectare

# Output results
st.write(f"### Monthly Payout: {monthly_return_needed:.2f} SEK")
st.write(f"### Required Production Share: {percentage_needed:.2f} %")
st.write(f"### Required Hectares to Cover Payout: {hectares_required:.2f} hectares")

# Time series for visualization
months = 50 * 12
build_time_months = build_time_years * 12
cash_flows = [0] * build_time_months + [monthly_return_needed] * (months - build_time_months)
cumulative_cash_flow = np.cumsum(cash_flows)

# DataFrame for plotting
data = {
    "Month": list(range(months)),
    "Monthly Payout (SEK)": cash_flows,
    "Cumulative Cash Flow (SEK)": cumulative_cash_flow
}
df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(df["Month"], df["Cumulative Cash Flow (SEK)"], label='Cumulative Cash Flow (SEK)', color='green')
plt.axvline(build_time_months, color='red', linestyle='--', label='Build Time')
plt.title("Sunthetics CHP2X Cash Flow Simulation")
plt.xlabel("Months")
plt.ylabel("Cumulative Cash Flow (SEK)")
plt.grid(True)
plt.legend()
st.pyplot(plt)
