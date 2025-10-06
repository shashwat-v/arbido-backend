from fyers_apiv3 import fyersModel
# from fyers_client import fyers
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv
import pandas as pd
import os
import json
import sys

load_dotenv()
client_id = os.getenv("CLIENT_ID")

with open("access_token.json", "r") as f:
    access_token = json.load(f)["access_token"]

fyers = fyersModel.FyersModel(
    client_id=client_id,
    is_async=False,
    token=access_token,
    log_path="logs"
)

if len(sys.argv) != 4:
    raise ValueError("Usage: python data_fetcher.py <TICKER> <START_DATE> <END_DATE>")

ticker = sys.argv[1]
start_date = sys.argv[2]
end_date = sys.argv[3]
# ticker = "NSE:NIFTY50-INDEX"
# ticker = sys.argv[1] if len(sys.argv) > 1 else "NSE:NIFTY50-INDEX"
print(ticker)
timeframe = "30"
print(start_date)
print(end_date)
# start_date = "2024-10-20"
# end_date = "2024-12-20"

data = {
    "symbol": ticker,
    "resolution": timeframe,
    "date_format":"1",
    "range_from": start_date,
    "range_to": end_date,
    "cont_flag":"1"
}

response = fyers.history(data=data)

columns = ["timestamp", "open", "high", "low", "close", "volume"]
df = pd.DataFrame(response["candles"], columns=columns)

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

os.makedirs("data", exist_ok=True)

filename = f"{ticker.replace(':', '_')}_{timeframe}min_{start_date}_to_{end_date}.csv"
filepath = os.path.join("data", filename)

df.to_csv(filepath, index=False)

print(f"✅ Data saved successfully to: {filepath}")
print(df.head())