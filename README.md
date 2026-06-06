# Bluestock MF Capstone — Mutual Fund Analytics Platform

**Company:** Bluestock Fintech Pvt. Ltd.  
**Domain:** Mutual Fund / Fintech  
**Duration:** 7 Working Days  

## Project Overview
End-to-end Mutual Fund Analytics Platform that ingests AMFI data, transforms it through an ETL pipeline, stores it in SQLite, and presents insights via an interactive Tableau dashboard.

## Setup Instructions
```bash
pip install -r requirements.txt
```

## How to Run ETL Pipeline
```bash
python scripts/etl_pipeline.py
```

## How to Fetch Live NAV
```bash
python scripts/live_nav_fetch.py
```

## How to Compute Metrics
```bash
python scripts/compute_metrics.py
```

## How to Get Fund Recommendations
```bash
python scripts/recommender.py
```

## How to Open Dashboard
Open `dashboard/bluestock_mf_dashboard.twbx` in Tableau Public

## Project Structure
- `data/raw_data/` — 10 original CSV datasets
- `data/processed_data/` — cleaned and merged CSVs
- `data/db/` — SQLite database (not committed, use schema.sql)
- `notebooks/` — Jupyter analysis notebooks
- `scripts/` — Python ETL and analytics scripts
- `sql/` — Database schema and queries
- `dashboard/` — Tableau dashboard file
- `reports/` — Final report, presentation and charts

## Key Findings
1. SIP inflows grew 169% from ₹11,517 Cr (Jan 2022) to ₹31,002 Cr (Dec 2025)
2. ICICI Pru Midcap Fund scored highest (100/100) in composite scorecard
3. Industry folios nearly doubled from 13.26 to 26.12 crore in 4 years
4. Banking and IT sectors dominate equity fund portfolios (40%+ weight)
5. 26-35 age group has highest SIP transaction count

## Technologies Used
Python, Pandas, NumPy, SQLite, SQLAlchemy, Matplotlib, Seaborn, Plotly, Tableau, Git