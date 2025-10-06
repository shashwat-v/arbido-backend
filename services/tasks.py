from services.pairs_metrics_engine import compute_pairs_metrics
from services.celery_worker import celery_app
import subprocess
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@celery_app.task(name="fetch_data_task")
def fetch_data_task(symbol: str, start_date: str, end_date: str):
    """Fetch historical data for a single ticker and return the saved CSV path."""
    try:
        print(f"🚀 Fetching data for {symbol} from {start_date} to {end_date}")

        safe_symbol = symbol.replace(":", "_").replace("/", "_")
        filename = f"data/{safe_symbol}_30min_{start_date}_to_{end_date}.csv"

        subprocess.run(
            ["python", "services/data_fetcher.py", symbol, start_date, end_date],
            check=True
        )

        # ✅ Return both symbol and exact CSV filename
        print(f"✅ CSV generated successfully for {symbol}: {filename}")
        return {"symbol": symbol, "status": "success", "file_path": filename}

    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching data for {symbol}: {e}")
        return {"symbol": symbol, "status": "failed", "error": str(e)}


@celery_app.task(name="compute_pairs_metrics_task")
def compute_pairs_metrics_task(results):
    """Run after both tickers are fetched."""
    print(f"📦 Received results: {results}")

    try:
        ticker_1 = results[0]["symbol"]
        ticker_2 = results[1]["symbol"]
        file_1 = results[0]["file_path"]
        file_2 = results[1]["file_path"]

        print(f"🔍 Using files:\n{file_1}\n{file_2}")

        # Directly compute metrics using provided file paths
        return compute_pairs_metrics(ticker_1, ticker_2, file_1, file_2)

    except Exception as e:
        import traceback
        print("🔥 Exception in compute_pairs_metrics_task:", e)
        print(traceback.format_exc())
        return {"error": str(e)}