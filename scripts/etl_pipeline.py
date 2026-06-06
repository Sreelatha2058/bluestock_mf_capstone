"""
etl_pipeline.py
Bluestock Fintech Capstone — Master ETL Pipeline
Runs full pipeline: ingest → clean → load to SQLite
"""
import pandas as pd
import os
from pathlib import Path
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR       = BASE_DIR / 'data' / 'raw_data'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed_data'
DB_PATH       = BASE_DIR / 'data' / 'db' / 'bluestock_mf.db'

PROCESSED_DIR.mkdir(exist_ok=True)

def extract():
    print("📥 EXTRACT: Loading raw CSVs...")
    datasets = {}
    for f in sorted(RAW_DIR.glob('*.csv')):
        datasets[f.stem] = pd.read_csv(f)
        print(f"  ✅ {f.name}: {datasets[f.stem].shape}")
    return datasets

def transform(datasets):
    print("\n🔄 TRANSFORM: Cleaning data...")

    # NAV history
    nav = datasets['02_nav_history'].copy()
    nav['date'] = pd.to_datetime(nav['date'])
    nav = nav.sort_values(['amfi_code','date'])
    nav = nav[nav['nav'] > 0].drop_duplicates()
    nav['daily_return_pct'] = nav.groupby('amfi_code')['nav'].pct_change() * 100
    nav.to_csv(PROCESSED_DIR / 'clean_nav.csv', index=False)
    print(f"  ✅ clean_nav.csv: {nav.shape}")

    # Transactions
    txn = datasets['08_investor_transactions'].copy()
    txn['transaction_date'] = pd.to_datetime(txn['transaction_date'])
    txn['transaction_type'] = txn['transaction_type'].str.strip().str.title()
    txn = txn[txn['amount_inr'] > 0].drop_duplicates()
    txn.to_csv(PROCESSED_DIR / 'clean_transactions.csv', index=False)
    print(f"  ✅ clean_transactions.csv: {txn.shape}")

    # Other files
    others = {
        '01_fund_master':          ('clean_fund_master.csv',        'launch_date'),
        '03_aum_by_fund_house':    ('clean_aum.csv',                'date'),
        '04_monthly_sip_inflows':  ('clean_sip_inflows.csv',        'month'),
        '05_category_inflows':     ('clean_category_inflows.csv',   'month'),
        '06_industry_folio_count': ('clean_folio_count.csv',        'month'),
        '07_scheme_performance':   ('clean_performance.csv',        None),
        '09_portfolio_holdings':   ('clean_portfolio_holdings.csv', 'portfolio_date'),
        '10_benchmark_indices':    ('clean_benchmark_indices.csv',  'date'),
    }
    for key, (out_file, date_col) in others.items():
        df = datasets[key].copy().drop_duplicates()
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col])
        df.to_csv(PROCESSED_DIR / out_file, index=False)
        print(f"  ✅ {out_file}: {df.shape}")

def load():
    print("\n📤 LOAD: Loading into SQLite...")
    engine = create_engine(f'sqlite:///{DB_PATH}')
    table_map = {
        'clean_fund_master.csv':        'dim_fund',
        'clean_nav.csv':                'fact_nav',
        'clean_transactions.csv':       'fact_transactions',
        'clean_performance.csv':        'fact_performance',
        'clean_aum.csv':                'fact_aum',
        'clean_sip_inflows.csv':        'fact_sip_industry',
        'clean_portfolio_holdings.csv': 'fact_portfolio',
        'clean_benchmark_indices.csv':  'fact_benchmark',
    }
    for csv_file, table in table_map.items():
        df = pd.read_csv(PROCESSED_DIR / csv_file)
        df.to_sql(table, engine, if_exists='replace', index=False)
        print(f"  ✅ {table}: {len(df)} rows")

if __name__ == '__main__':
    print("🚀 Starting ETL Pipeline...\n")
    datasets = extract()
    transform(datasets)
    load()
    print("\n✅ ETL Pipeline complete!")