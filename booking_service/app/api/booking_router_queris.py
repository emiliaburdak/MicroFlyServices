from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import CartItem
from ..schema import FlightSchema
from ..services.booking_service import get_current_user_id

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/view_cart/", response_model=list[FlightSchema])
def view_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_flights = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    return cart_flights
