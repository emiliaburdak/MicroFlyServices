from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Float
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
    price = Column(Float, index=True)