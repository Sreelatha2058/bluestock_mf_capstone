"""
compute_metrics.py
Bluestock Fintech Capstone
Computes CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown, VaR
"""
import pandas as pd
import numpy as np
import scipy.stats as stats
from pathlib import Path

BASE_DIR      = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed_data'
RF_DAILY      = 0.065 / 252

def compute_all_metrics():
    nav  = pd.read_csv(PROCESSED_DIR / 'clean_nav.csv', parse_dates=['date'])
    fund = pd.read_csv(PROCESSED_DIR / 'clean_fund_master.csv')
    bench= pd.read_csv(PROCESSED_DIR / 'clean_benchmark_indices.csv', parse_dates=['date'])

    nav = nav.sort_values(['amfi_code','date'])
    nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()

    nifty100 = bench[bench['index_name']=='NIFTY100'].sort_values('date')
    nifty100['bench_return'] = nifty100['close_value'].pct_change()

    results = []
    for code in nav['amfi_code'].unique():
        df = nav[nav['amfi_code']==code].sort_values('date')
        ret = df['daily_return'].dropna()
        if len(ret) < 30:
            continue

        # CAGR
        n = len(df)
        cagr = (df['nav'].iloc[-1]/df['nav'].iloc[0])**(252/n) - 1

        # Sharpe
        sharpe = ((ret.mean()-RF_DAILY)/ret.std()) * np.sqrt(252)

        # Sortino
        downside = ret[ret < 0].std()
        sortino = ((ret.mean()-RF_DAILY)/downside) * np.sqrt(252) if downside > 0 else None

        # Max Drawdown
        roll_max = df['nav'].cummax()
        max_dd = ((df['nav']-roll_max)/roll_max).min()

        # VaR
        var_95 = ret.quantile(0.05)

        # Alpha & Beta
        merged = df[['date','daily_return']].merge(
            nifty100[['date','bench_return']], on='date')
        if len(merged) > 30:
            slope, intercept, _, _, _ = stats.linregress(
                merged['bench_return'], merged['daily_return'])
            beta  = round(slope, 4)
            alpha = round(intercept * 252 * 100, 4)
        else:
            beta = alpha = None

        name = fund[fund['amfi_code']==code]['scheme_name'].values
        results.append({
            'amfi_code':    code,
            'scheme_name':  name[0] if len(name) > 0 else str(code),
            'cagr_pct':     round(cagr*100, 4),
            'sharpe':       round(sharpe, 4),
            'sortino':      round(sortino, 4) if sortino else None,
            'max_dd_pct':   round(max_dd*100, 4),
            'var_95_pct':   round(var_95*100, 4),
            'beta':         beta,
            'alpha':        alpha,
        })

    out = pd.DataFrame(results)
    out.to_csv(PROCESSED_DIR / 'computed_metrics.csv', index=False)
    print("✅ Metrics saved to computed_metrics.csv")
    print(out.to_string(index=False))

if __name__ == '__main__':
    compute_all_metrics()