from fastapi import FastAPI
from models import PairRequest
from celery.result import AsyncResult
from services.tasks import fetch_data_task

app = FastAPI()

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

    task_1 = fetch_data_task.delay(req.ticker_1, str(req.start_date), str(req.end_date))
    task_2 = fetch_data_task.delay(req.ticker_2, str(req.start_date), str(req.end_date))

    return {
        "status": "queued",
        "tasks": [
            {"ticker": req.ticker_1, "task_id": task_1.id},
            {"ticker": req.ticker_2, "task_id": task_2.id},
        ]
    }

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "task_status": task.status,
        "task_result": task.result,
    }
