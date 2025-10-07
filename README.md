# ⚡ Arbido — Pairs Trading Dashboard (Backend)

### 🧠 High-Performance Python Engine for Statistical Arbitrage

The **Arbido Backend** powers the Pairs Trading Dashboard with **real-time data ingestion**, **statistical computations**, and **asynchronous background processing** — designed for speed, scalability, and precision.

---

## 🚀 Overview

Arbido's backend is a **modular Python-based system** that handles:

- 📈 Fetching price data from APIs (e.g., Fyers)
- ⚙️ Processing pairs for cointegration, correlation, and spread analysis
- ⏱ Running background Celery tasks for heavy computations
- 🧮 Serving metrics & insights to the frontend dashboard
- 🪶 Dockerized microservice architecture for smooth deployment

Built using **FastAPI**, **Celery**, **Redis**, and **Python**, Arbido Backend ensures **low latency**, **fault tolerance**, and **scalability**.

---

## 🧩 Tech Stack

| Component           | Technology                              |
| ------------------- | --------------------------------------- |
| 🧠 Core Language    | Python 3.11+                            |
| ⚙️ Web Framework    | FastAPI                                 |
| 🧮 Task Queue       | Celery                                  |
| 🗄️ Message Broker   | Redis                                   |
| 📊 Data Handling    | Pandas, NumPy                           |
| 🔍 API Client       | Fyers API                               |
| 🐳 Containerization | Docker + Docker Compose                 |
| 🧾 Logging          | Python `logging` module                 |
| ⚡ Environment      | `.env` file for secrets and credentials |

---

## 🗂️ Project Structure

```
arbido-backend/
│
├── data/                      # Local CSVs / market data
│   ├── NSE_RELIANCE-EQ_30min.csv
│   ├── NSE_TCS-EQ_30min.csv
│   └── pairs_NSE:RELIANCE-EQ_NSE:TCS-EQ.csv
│
├── logs/                      # Application and Celery logs
│   ├── celery.log
│   ├── fyersApi.log
│   └── fyersRequests.log
│
├── services/                  # Core backend service modules
│   ├── celery_worker.py
│   ├── fyers_auth.py
│   ├── fyers_client.py
│   ├── data_fetcher.py
│   ├── pairs_metrics_engine.py
│   └── tasks.py
│
├── main.py                    # Application entry point
├── models.py                  # Pydantic or ORM models
├── requirements.txt           # Dependencies list
├── docker-compose.yml         # Multi-service orchestration
├── Dockerfile                 # Backend image definition
├── .env                       # Environment variables
└── .gitignore                 # Ignored files and folders
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/shashwat-v/arbido-backend.git
cd arbido-backend
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create a `.env` File

Example:

```bash
FYERS_CLIENT_ID=your_client_id
FYERS_SECRET_KEY=your_secret_key
FYERS_ACCESS_TOKEN=your_access_token
REDIS_URL=redis://localhost:6379/0
```

---

## 🧵 Running the Backend

### 🧩 Option 1 — Run with Python (Development Mode)

#### Start FastAPI Server:

```bash
python main.py
```

#### Start Celery Worker:

```bash
celery -A services.celery_worker.celery_app worker --loglevel=info
```

---

### 🐳 Option 2 — Run with Docker (Recommended)

Start all services (API + Celery + Redis) with one command:

```bash
docker-compose up --build
```

✅ This will automatically start:

- FastAPI backend
- Redis broker
- Celery worker

---

## 📡 API Endpoints (Example)

| Endpoint         | Method | Description                                              |
| ---------------- | ------ | -------------------------------------------------------- |
| `/pairs-data`    | `POST` | Fetches price data for a given symbol or pair            |
| `/pairs-metrics` | `GET`  | Returns statistical metrics (z-score, beta, correlation) |
| `/health`        | `GET`  | Health check endpoint                                    |

Example request:

```bash
POST /pairs-data
{
  "ticker_1": "NSE:RELIANCE-EQ",
  "ticker_2": "NSE:TCS-EQ"
}
```

---

## 🧠 Core Services

### 🔹 `data_fetcher.py`

Fetches OHLCV data from Fyers API or CSVs for selected instruments.

### 🔹 `pairs_metrics_engine.py`

Computes key metrics like:

- Correlation
- Cointegration
- Mean reversion
- Z-score
- Beta ratio

### 🔹 `celery_worker.py`

Runs Celery worker and handles background processing for heavy tasks.

### 🔹 `fyers_auth.py` & `fyers_client.py`

Manages Fyers API authentication, tokens, and data requests.

---

## 🧰 Logging

All logs are stored under the `/logs` directory:

```
logs/
├── celery.log
├── fyersApi.log
└── fyersRequests.log
```

You can modify logging levels inside `main.py` or `celery_worker.py`.

---

## 🧾 Environment Variables Reference

| Variable             | Description                               |
| -------------------- | ----------------------------------------- |
| `FYERS_CLIENT_ID`    | Your Fyers API Client ID                  |
| `FYERS_SECRET_KEY`   | Your Fyers Secret Key                     |
| `FYERS_ACCESS_TOKEN` | Access Token for authentication           |
| `REDIS_URL`          | Redis connection string                   |
| `API_PORT`           | (Optional) Custom port for FastAPI server |

---

## 🧮 Example Workflow

1. User triggers data fetch from the frontend.
2. FastAPI receives the request and enqueues a Celery task.
3. Celery worker fetches data via `fyers_client.py`.
4. Data is processed by `pairs_metrics_engine.py`.
5. Results are logged and returned as metrics JSON to the frontend.

---

## 🧱 Docker Deployment Notes

- Default container names: `arbido_api`, `arbido_celery`, `arbido_redis`
- Logs are mapped to host volume `/logs`
- Environment variables are loaded from `.env`
- To rebuild images after code changes:
  ```bash
  docker-compose up --build
  ```

---

## 🧾 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Shashwat Vishwakarma**  
Aspiring Quant Trader | Developer | Finance Enthusiast  
📧 [shashwatv.dev@gmail.com](mailto:shashwatv.dev@gmail.com)  
🌐 [LinkedIn](https://linkedin.com/in/shashwat-v)

---

## 💡 Notes

- For development, Celery warnings like `"You're running the worker with superuser privileges"` are harmless in Docker containers — just avoid root in production.
- Use small candle intervals (5–15m) for faster backtesting.
