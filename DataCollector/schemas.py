from pydantic import BaseModel
from datetime import date
from typing import List

class DailyPrice(BaseModel):
    price_date: date
    avg_price: float
    max_price: float
    min_price: float

    class Config:
        orm_mode = True

class CoinByRange(BaseModel):
    coin_id: str
    startDate:str
    endDate:str

