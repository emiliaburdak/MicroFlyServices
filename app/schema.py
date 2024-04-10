from typing import Union

from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserOutput(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class FlightSchema(BaseModel):
    id: int
    departure: str
    destination: str
    date: datetime
    price: float

    class Config:
        orm_mode = True
