from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from booking_service.app.database import SessionLocal
from booking_service.app.models import CartItem, PurchasedFlight
from booking_service.app.schema import FlightSchema
from booking_service.app.services.booking_service import get_current_user_id

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_to_cart/")
def add_to_cart(flight_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_item = CartItem(user_id=user_id, flight_id=flight_id)
    db.add(cart_item)
    db.commit()
    return {"message": "Flight added to cart"}


@router.delete("/remove_from_cart/")
def remove_from_cart(cart_item_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == cart_item_id, CartItem.user_id == user_id).one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Flight not found")
    db.delete(item)
    db.commit()
    return {"message": "Flight removed from cart"}


@router.get("/view_cart/", response_model=list[FlightSchema])
def view_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_flights = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    return cart_flights


@router.post("/purchase/")
def purchase(flight_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.flight_id == flight_id).first()
    if not cart_items:
        raise HTTPException(status_code=404, detail="No items in cart to purchase")
    purchased_flight = PurchasedFlight(user_id=user_id, flight_id=flight_id)
    db.add(purchased_flight)
    db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.flight_id == flight_id).delete()
    db.commit()
    return {"message": "You have purchased flight!"}
