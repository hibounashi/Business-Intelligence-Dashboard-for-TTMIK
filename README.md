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
2. Create a Python virtual environment
bash
Copy code
python -m venv env
3. Activate the virtual environment
Windows

bash
Copy code
env\Scripts\activate
Linux / Mac

bash
Copy code
source env/bin/activate
4. Install dependencies
bash
Copy code
pip install -r requirements.txt
Make sure requirements.txt includes:
streamlit, pandas, sqlite3 (built-in with Python), matplotlib or plotly if used

Running the Dashboard
bash
Copy code
streamlit run app.py
Open the URL provided in the terminal (usually http://localhost:8501)

Interact with the dashboard to explore sales data and visualizations.

Project Structure
bash
Copy code
ttmik_bi_dashboard/
├── app.py             # Main Streamlit dashboard
├── data/
│   └── ttmik_sales.db # SQLite database
├── requirements.txt   # Python dependencies
└── README.md          # This file
Screenshots
Add screenshots of your dashboard here for better presentation, e.g.:


Contribution
Fork the repo

Create a new branch: git checkout -b feature-name

Commit your changes: git commit -m 'Add new feature'

Push to the branch: git push origin feature-name

Open a Pull Request
