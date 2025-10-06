from fastapi import FastAPI
from models import PairRequest
from celery.result import AsyncResult
from services.tasks import fetch_data_task, compute_pairs_metrics_task
from celery import chord
import os, json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, server is running!"}

# @app.post("/pairs-data")
# def fetch_data(req: PairRequest):
#     ticker_1 = req.ticker_1
#     task = fetch_data_task.delay(ticker_1)
#     return {"task_id": task.id, "status": "queued"}

@app.post("/pairs-data")
def fetch_data(req: PairRequest):
    
    job = chord(
        [
                fetch_data_task.s(req.ticker_1, str(req.start_date), str(req.end_date)),
                fetch_data_task.s(req.ticker_2, str(req.start_date), str(req.end_date))
        ]
    )(compute_pairs_metrics_task.s())
    
    return {"group_id": job.id, "status": "queued"}

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "task_status": task.status,
        "task_result": task.result,
    }

@app.get("/pairs-metrics/{ticker_1}/{ticker_2}")
def get_pairs_metrics(ticker_1: str, ticker_2: str):
    file_path = f"data/pairs_{ticker_1}_{ticker_2}_metrics.json"
    if not os.path.exists(file_path):
        return {"error": "Metrics file not found. Run /pairs-data first."}
    with open(file_path) as f:
        return json.load(f)