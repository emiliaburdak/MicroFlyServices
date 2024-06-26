from typing import Optional
from datetime import date, time
from pydantic import BaseModel
from datetime import datetime


class FlightSchema(BaseModel):
    id: int
    departure: str
    destination: str
    date: date
    time_departure: Optional[time] = None
    time_arrival: Optional[time] = None
    flight_time: Optional[str] = None
    id_arrival_next_day: Optional[int] = None
    is_dreamliner: bool
    checked_baggage: Optional[bool] = None
    hand_luggage: Optional[bool] = None
    food: Optional[bool] = None
    price: float
    update_data: datetime

    class Config:
        orm_mode = True
