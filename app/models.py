from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Float, Time, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Flight(Base):
    __tablename__ = "flight"

    id = Column(Integer, primary_key=True)
    departure = Column(String, index=True)
    destination = Column(String, index=True)
    date = Column(Date, index=True)
    time_departure = Column(Time, index=True)
    time_arrival = Column(Time, index=True)
    flight_time = Column(String, index=True)
    id_arrival_next_day = Column(Integer)
    is_dreamliner = Column(Boolean, default=False)
    checked_baggage = Column(Boolean)
    hand_luggage = Column(Boolean)
    food = Column(Boolean)
    price = Column(Float, index=True)
    update_data = Column(DateTime, default=datetime.utcnow)
