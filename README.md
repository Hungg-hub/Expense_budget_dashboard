
# 💳 Personal Expense & Budget Analytics Dashboard

An interactive personal finance analytics web application built with Python, Streamlit, Pandas, and Plotly. The tool automatically ingests bank and payment card transaction CSV files, classifies merchants into spending categories, and delivers real-time month-over-month budgetary insights.

🔗 🔗 **Live Demo:** [Open Dashboard](https://expensebudgetdashboard-znwz84pz4rovnde8xvotan.streamlit.app/)

---

## 🌟 Key Features

- **Automated Merchant Classification:** Maps unstructured merchant strings (e.g., transit passes, supermarkets, cafes) into standardized budget categories using pattern-matching rules.
- **Dynamic Time-Series & Category Breakdown:** Side-by-side interactive Plotly charts rendering spending shares (donut chart) and daily consumption rhythms (bar chart).
- **Multi-Month Financial Aggregation:** Compare total expenditure, transaction counts, and average spend across distinct monthly billing cycles.
- **Interactive Multi-Category Filtering:** Real-time filtering and sorting of transaction records without client-side latency.

---

## 🛠️ Tech Stack

- **Application & UI:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
- **Data Visualization:** [Plotly Express](https://plotly.com/python/)
- **Deployment:** Streamlit Community Cloud

---

## 🚀 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Hungg-hub/Expense-budget-dashboard.git](https://github.com/Hungg-hub/Expense-budget-dashboard.git)
   cd Expense-budget-dashboard
