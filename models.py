from pydantic import BaseModel
from datetime import date

class PairRequest(BaseModel):
    ticker_1: str
    ticker_2: str
    start_date: date
    end_date: date
    capital: int
    z_score: int
    freq: int | None=None