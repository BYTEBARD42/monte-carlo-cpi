# 🎓 CPI Monte Carlo Simulator — B.Tech ECE

A Monte Carlo–based CPI prediction tool designed for B.Tech ECE students. This application estimates your final CPI by simulating thousands of grade outcomes based on your historical performance and expected grade ranges for future semesters.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features
- Monte Carlo Simulation Engine
- 95% Confidence Interval
- CPI Evolution Tracking
- Visualizations (histograms, CDF, box plots)
- Letter Grade Mapping
- Streamlit UI

## 🚀 Quick Start
### Installation
```bash
git clone https://github.com/YOUR_USERNAME/cpi-monte-carlo.git
cd cpi-monte-carlo
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```

## 🌐 Deployment
Deploy easily on Streamlit Cloud.

## 📊 How It Works
Simulates semester-wise grade performance using normal distribution and computes CPI trajectories.

## 📚 Grade Mapping
AA=10, AB=9, BB=8, BC=7, CC=6, CD=5, DD=4, FF=0

## 🧮 CPI Formula
CPI = Total Grade Points / Total Credits

## 📁 Structure
```
cpi-monte-carlo/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
```

## 📄 License
MIT License
