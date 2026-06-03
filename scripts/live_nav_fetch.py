"""
live_nav_fetch.py
Bluestock Fintech Capstone — Day 1
Fetches live NAV for 6 schemes from mfapi.in and saves as CSV.
"""
import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw_data'
RAW_DIR.mkdir(parents=True, exist_ok=True)

SCHEMES = {
    'HDFC_Top100_Direct' : 125497,
    'SBI_Bluechip'       : 119551,
    'ICICI_Bluechip'     : 120503,
    'Nippon_LargeCap'    : 118632,
    'Axis_Bluechip'      : 119092,
    'Kotak_Bluechip'     : 120841,
}

def fetch_nav(scheme_name, code):
    url = f"https://api.mfapi.in/mf/{code}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        meta = data.get('meta', {})
        print(f"  Fund : {meta.get('scheme_name')}")
        print(f"  Type : {meta.get('scheme_type')}")

        df = pd.DataFrame(data.get('data', []))
        df['scheme_code'] = code
        df['scheme_name'] = scheme_name

        out_path = RAW_DIR / f'live_nav_{scheme_name}.csv'
        df.to_csv(out_path, index=False)
        print(f"  ✅ Saved {len(df)} rows → {out_path.name}")

    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error: {e}")

if __name__ == '__main__':
    for name, code in SCHEMES.items():
        print(f"\nFetching: {name} (code: {code})")
        fetch_nav(name, code)
    print("\n✅ Live NAV fetch complete.")