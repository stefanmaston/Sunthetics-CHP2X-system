# Sunthetics CHP2X Simulation

An interactive Streamlit application for simulating and analyzing CHP2X (Combined Heat, Power, and X) projects, specifically focused on methanol production with revenue sharing financial model. The Sunthetics CHP2X system produce stored solar energy at beneficial LCOE level, and zero intemittency creating renewable energy with baseload capability similar to traditional energy sources. 

![Bild 2025-08-20 kl  16 31](https://github.com/user-attachments/assets/d0eaa50b-f00f-40a6-8800-5a2e4def4811)


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

![Bild 2025-08-20 kl  16 18](https://github.com/user-attachments/assets/39c3a58f-d6f7-4d2f-a381-0bbb07abe08a)

## Financial Analysis

- Net Present Value (NPV) calculation
- Revenue sharing calculations
- Monthly and annual financial summaries
- Long-term analysis
- Cash flow visualization

![Bild 2025-05-19 kl  16 53](https://github.com/user-attachments/assets/0bbba158-1eae-400f-ab1b-9151725bf678)


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
