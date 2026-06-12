"""
run_pipeline.py
Bluestock Fintech Capstone — Master execution script
Runs the full pipeline in sequence: ETL → Metrics → Recommendations
"""
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def run(script):
    print(f"\n{'='*50}")
    print(f"▶ Running: {script}")
    print('='*50)
    result = subprocess.run(
        [sys.executable, BASE_DIR / 'scripts' / script],
        capture_output=False
    )
    if result.returncode != 0:
        print(f"❌ Failed: {script}")
        sys.exit(1)
    print(f"✅ Done: {script}")

if __name__ == '__main__':
    print("🚀 Bluestock MF Capstone — Full Pipeline\n")
    run('etl_pipeline.py')
    run('live_nav_fetch.py')
    run('compute_metrics.py')
    run('recommender.py')
    print("\n✅ Full pipeline complete!")