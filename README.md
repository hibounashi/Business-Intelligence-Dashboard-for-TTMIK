# TTMIK BI Dashboard

A simple **Business Intelligence (BI) dashboard** for **TTMIK (Talk To Me In Korean)** sales data.  
Built using **Python**, **Streamlit**, and **SQLite**, this dashboard allows you to visualize key sales metrics and insights.

---

## Features

- Display global sales indicators:
  - Total revenue
  - Total quantity sold
- Sales by region
- Top products by revenue
- Monthly revenue evolution
- Interactive visualization with Streamlit

---

## Installation & Setup

### 1. Clone the repository and navigate to it

```bash
git clone https://github.com/your-username/ttmik_bi_dashboard.git
cd ttmik_bi_dashboard
```
2. Create a Python virtual environment
```bash
python -m venv env
```
3. Activate the virtual environment
Windows

```bash
env\Scripts\activate
```
Linux / Mac
```bash
source env/bin/activate
```
4. Install dependencies
```bash
pip install -r requirements.txt
```
Make sure requirements.txt includes:
streamlit, pandas, sqlite3 (built-in with Python), matplotlib or plotly if used

Running the Dashboard
```bash
streamlit run app.py
```
Open the URL provided in the terminal (usually http://localhost:8501)

Interact with the dashboard to explore sales data and visualizations.

