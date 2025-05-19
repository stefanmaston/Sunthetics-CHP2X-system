# Sunthetics CHP2X Simulation

An interactive Streamlit application for simulating and analyzing CHP2X (Combined Heat, Power, and X) projects, specifically focused on methanol production with revenue sharing financial model. The Suntehtics CHP2X system produce stored solar energy at beneficial LCOE level, and zero intemittency creating renewable energy with baseload capability similar to traditional energy sources. 

![Bild 2025-05-19 kl  16 43](https://github.com/user-attachments/assets/4a60a2f4-d160-4556-97a1-a3378cc5f840)

![Bild 2025-05-19 kl  16 42](https://github.com/user-attachments/assets/1576ced8-16df-441e-9ca6-7b1002fdac26)

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

The application will be available at https://sunthetics-chp2x-system-uu6vehbpb7exha5wi2hg96.streamlit.app and at http://localhost:8501

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
