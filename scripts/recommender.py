"""
recommender.py
Bluestock Fintech Capstone
Fund recommendation engine based on investor risk appetite
"""
import pandas as pd
from pathlib import Path

BASE_DIR      = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed_data'

def recommend(risk_level: str) -> pd.DataFrame:
    """
    Returns top 3 fund recommendations based on risk level.
    Args:
        risk_level: 'low', 'moderate', or 'high'
    Returns:
        DataFrame with top 3 recommended funds
    """
    scorecard = pd.read_csv(PROCESSED_DIR / 'fund_scorecard.csv')
    fund      = pd.read_csv(PROCESSED_DIR / 'clean_fund_master.csv')
    merged    = scorecard.merge(fund[['amfi_code','risk_category']], on='amfi_code')

    mapping = {
        'low':      'Low',
        'moderate': 'Moderate',
        'high':     'Very High'
    }
    grade    = mapping.get(risk_level.lower(), 'Moderate')
    filtered = merged[merged['risk_category'] == grade]
    result   = filtered[['scheme_name','cagr_3yr',
                          'sharpe_ratio_computed','score_100']]\
               .sort_values('score_100', ascending=False).head(3)
    return result

if __name__ == '__main__':
    print("=== BLUESTOCK FUND RECOMMENDER ===\n")
    for level in ['low', 'moderate', 'high']:
        print(f"Top 3 funds for {level.upper()} risk investor:")
        print(recommend(level).to_string(index=False))
        print()