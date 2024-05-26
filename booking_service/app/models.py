from .database import Base
from sqlalchemy import Column, Integer, String


class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    flight_id = Column(Integer)


class PurchasedFlight(Base):
    __tablename__ = 'purchased_flights'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    flight_id = Column(Integer)
