# services/pairs_metrics_engine.py
import pandas as pd
import numpy as np
import statsmodels.api as sm
import json
import os


def compute_pairs_metrics(ticker_1: str, ticker_2: str, file_1: str, file_2: str, window: int = 30):
    """
    Compute correlation, cointegration, hedge ratio, rolling spread,
    rolling z-score, and save JSON output for frontend.
    """

    # --- Load fetched data ---
    df1 = pd.read_csv(file_1)
    df2 = pd.read_csv(file_2)

    df = pd.merge(
        df1[["timestamp", "close"]],
        df2[["timestamp", "close"]],
        on="timestamp",
        suffixes=(f"_{ticker_1}", f"_{ticker_2}")
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- Log prices & returns ---
    df["log_1"] = np.log(df[f"close_{ticker_1}"])
    df["log_2"] = np.log(df[f"close_{ticker_2}"])
    ret1, ret2 = df["log_1"].diff(), df["log_2"].diff()

    # --- Correlation ---
    corr = np.corrcoef(ret1.dropna(), ret2.dropna())[0, 1]

    # --- Hedge ratio via OLS ---
    model = sm.OLS(df["log_1"], sm.add_constant(df["log_2"])).fit()
    hedge_ratio = model.params[1]

    # --- Cointegration (ADF) ---
    adf_p = sm.tsa.stattools.adfuller(model.resid)[1]
    cointegration = 1 - adf_p

    # --- Spread & Rolling Stats ---
    df["spread"] = df["log_1"] - hedge_ratio * df["log_2"]
    df["spread_mean"] = df["spread"].rolling(window).mean()
    df["spread_std"] = df["spread"].rolling(window).std()
    df["z_score"] = (df["spread"] - df["spread_mean"]) / df["spread_std"]

    # --- Latest Z-score & Signal ---
    z = df["z_score"].iloc[-1]
    signal = (
        "SELL Stock 1, BUY Stock 2" if z > 2
        else "BUY Stock 1, SELL Stock 2" if z < -2
        else "HOLD"
    )

    # --- Prepare Output ---
    summary = {
        "ticker_1": ticker_1,
        "ticker_2": ticker_2,
        "correlation": round(corr, 3),
        "cointegration": round(cointegration, 3),
        "hedge_ratio": round(hedge_ratio, 3),
        "latest_z_score": round(z, 3),
        "signal": signal,
    }

    rolling_data = df[["timestamp", "spread", "spread_mean", "spread_std", "z_score"]].dropna()

    output = {
        "summary": summary,
        "rolling": [
            {
                "timestamp": str(row.timestamp),
                "spread": round(row.spread, 6),
                "spread_mean": round(row.spread_mean, 6),
                "spread_std": round(row.spread_std, 6),
                "z_score": round(row.z_score, 6)
            }
            for _, row in rolling_data.iterrows()
        ]
    }

    # --- Save JSON ---
    os.makedirs("data", exist_ok=True)
    path = f"data/pairs_{ticker_1}_{ticker_2}_metrics.json"
    with open(path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Saved metrics JSON: {path}")
    return summary
