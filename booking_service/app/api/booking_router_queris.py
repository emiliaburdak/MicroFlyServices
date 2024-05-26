from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CartItem, PurchasedFlight
from ..schema import FlightSchema
from ..services.booking_service import get_current_user_id

router = APIRouter()


@router.get("/view_cart/", response_model=list[FlightSchema])
def view_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_flights = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    return cart_flights


@router.get("/view_purchase/")
def view_purchases(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    purchase_flight = db.query(PurchasedFlight).filter(PurchasedFlight.user_id == user_id).all()
    return purchase_flight
