from services.pairs_metrics_engine import compute_pairs_metrics
from services.celery_worker import celery_app
import subprocess

@celery_app.task(name="fetch_data_task")
def fetch_data_task(symbol: str, start_date: str, end_date: str):
    """Fetch historical data for a single ticker."""
    try:
        print(f"🚀 Fetching data for {symbol} from {start_date} to {end_date}")
        subprocess.run(
            ["python", "services/data_fetcher.py", symbol, start_date, end_date],
            check=True
        )
        print(f"✅ CSV generated successfully for {symbol}")
        return {"symbol": symbol, "status": "success"}
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching data for {symbol}: {e}")
        return {"symbol": symbol, "status": "failed", "error": str(e)}

@celery_app.task(name="compute_pairs_metrics_task")
def compute_pairs_metrics_task(results):
    """Run after both tickers are fetched"""
    ticker_1 = results[0]["symbol"]
    ticker_2 = results[1]["symbol"]
    return compute_pairs_metrics(ticker_1, ticker_2)