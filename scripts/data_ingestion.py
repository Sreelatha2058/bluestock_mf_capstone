"""
data_ingestion.py
Bluestock Fintech Capstone — Day 1
Loads all 10 CSV datasets and prints shape, dtypes, head for each.
"""
import pandas as pd
import os
from pathlib import Path

# Always use Path — never hardcode
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw_data'

def load_all_datasets():
    datasets = {}
    files = sorted(RAW_DIR.glob('*.csv'))

    for filepath in files:
        df = pd.read_csv(filepath)
        name = filepath.stem
        datasets[name] = df

        print(f"\n{'='*50}")
        print(f"FILE: {filepath.name}")
        print(f"Shape: {df.shape}")
        print(f"\nColumn types:\n{df.dtypes}")
        print(f"\nFirst 3 rows:\n{df.head(3)}")

        # Anomaly check
        nulls = df.isnull().sum().sum()
        dupes = df.duplicated().sum()
        if nulls > 0 or dupes > 0:
            print(f"⚠️  Nulls: {nulls}, Duplicates: {dupes}")

    return datasets

if __name__ == '__main__':
    datasets = load_all_datasets()
    print("\n✅ All datasets loaded successfully.")