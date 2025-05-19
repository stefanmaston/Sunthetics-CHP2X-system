# Sunthetics CHP2X Simulation

An interactive Streamlit application for simulating and analyzing CHP2X (Combined Heat, Power, and X) projects, specifically focused on methanol production.

## Features

- Interactive simulation of CHP2X projects
- Multiple currency support (SEK, EUR, USD)
- Configurable project parameters:
  - CAPEX per hectare
  - Number of hectares
  - Methanol production rate
  - Annual sun hours (DNI)
  - Project lifetime
  - Revenue sharing percentage
  - Price per liter of methanol
  - Annual price escalation
  - Build time
  - Discount rate

## Financial Analysis

- Net Present Value (NPV) calculation
- Revenue sharing calculations
- Monthly and annual financial summaries
- Long-term analysis
- Cash flow visualization

## Requirements

- Python 3.x
- Streamlit
- Pandas
- NumPy
- NumPy Financial
- Matplotlib

## Installation

1. Clone the repository
2. Install the required packages:
```bash
pip install streamlit pandas numpy numpy-financial matplotlib
```

## Usage

Run the application with:
```bash
streamlit run Sunthetics_CHP2X_Simulation.py
```

The application will be available at http://localhost:8501

## License

This project is licensed under the MIT License - see the LICENSE file for details. 