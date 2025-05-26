
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(layout="wide")
st.title("SCWE Electrolyzer Simulator")

# Inputs
P_kW = st.sidebar.slider("Electrical Power (kW)", 1.0, 20.0, 6.8, 0.1)
n_cells = st.sidebar.slider("Number of Cells", 10, 80, 40, 1)
T_min = st.sidebar.slider("Minimum Temperature (°C)", 250, 700, 250, 10)
T_max = st.sidebar.slider("Maximum Temperature (°C)", T_min + 10, 800, 750, 10)
T_step = st.sidebar.slider("Temperature Step (°C)", 10, 100, 50, 10)

# Constants
HHV_H2_kJmol = 285.8
LHV_H2_kJmol = 241.8
LHV_H2_kWhkg = 33.3
V_stack = 50  # Stack voltage

# Simulering
temperatures = list(range(T_min, T_max + 1, T_step))
results = []

for T_C in temperatures:
    el_energy_per_mol = max(190 - (T_C - 700) * 0.1, 160)
    mol_H2_per_s = (P_kW * 1000) / el_energy_per_mol
    kg_H2_per_h = mol_H2_per_s * 2.016 * 3600 / 1000
    eleff = LHV_H2_kJmol / el_energy_per_mol * 100
    totaleff = LHV_H2_kJmol / HHV_H2_kJmol * 100
    thermal_energy = HHV_H2_kJmol - el_energy_per_mol
    thermal_kW = mol_H2_per_s * thermal_energy / 1000
    total_input_kW = P_kW + thermal_kW
    output_kW = kg_H2_per_h * LHV_H2_kWhkg
    total_efficiency = 100 * output_kW / total_input_kW

    results.append({
        "Temperature (°C)": T_C,
        "H2 Production (kg/h)": kg_H2_per_h,
        "Electrical Efficiency (%)": eleff,
        "Thermal Energy (kW)": thermal_kW,
        "Total Efficiency (%)": total_efficiency
    })

df = pd.DataFrame(results)

# Diagram
st.line_chart(df.set_index("Temperature (°C)")[["H2 Production (kg/h)", "Thermal Energy (kW)"]])
st.line_chart(df.set_index("Temperature (°C)")[["Electrical Efficiency (%)", "Total Efficiency (%)"]])

# Tabell
st.dataframe(df)


import json
from datetime import datetime

# Save/load config
st.sidebar.markdown("---")
save_name = st.sidebar.text_input("Config name", value="my_config")
if st.sidebar.button("💾 Save config"):
    config = {
        "P_kW": P_kW,
        "n_cells": n_cells,
        "T_min": T_min,
        "T_max": T_max,
        "T_step": T_step
    }
    with open(f"{save_name}.json", "w") as f:
        json.dump(config, f)
    st.success(f"Configuration saved as {save_name}.json")

if st.sidebar.button("📂 Load config"):
    try:
        with open(f"{save_name}.json", "r") as f:
            config = json.load(f)
            P_kW = config["P_kW"]
            n_cells = config["n_cells"]
            T_min = config["T_min"]
            T_max = config["T_max"]
            T_step = config["T_step"]
        st.success(f"Configuration {save_name}.json loaded")
    except FileNotFoundError:
        st.error("Config file not found.")
