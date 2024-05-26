import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import CartItem, PurchasedFlight
from ..services.booking_service import get_current_user_id
from ..services.kafka_events_utils import send_event
from ..services.payment_service import simulate_payment

from faststream.annotations import FastStream
from faststream.kafka import KafkaBroker

broker = KafkaBroker("localhost:9092")
app = FastStream(broker)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_to_cart/")
async def add_to_cart(flight_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_item = CartItem(user_id=user_id, flight_id=flight_id)
    db.add(cart_item)
    db.commit()

    event = json.dumps({
        "type": "CartAdded",
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "flight_id": flight_id
    })
    await send_event("booking-events", event)

    return {"message": "Flight added to cart"}


@router.delete("/remove_from_cart/")
async def remove_from_cart(cart_item_id: int, user_id: int = Depends(get_current_user_id),
                           db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == cart_item_id, CartItem.user_id == user_id).one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Flight not found")
    db.delete(item)
    db.commit()

    event = json.dumps({
        "type": "CartRemoved",
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "cart_item_id": cart_item_id
    })
    await send_event("booking-events", event)

    return {"message": "Flight removed from cart"}


@router.post("/purchase/")
async def purchase(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="No items in cart to purchase")

    # send event for event sourcing
    flights_ids = [cart_item.flight_id for cart_item in cart_items]
    event = json.dumps({
        "type": "PurchaseRequest",
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "flights_ids": flights_ids,
    })
    await send_event("purchase-request-event", event)

    await simulate_payment(user_id, flights_ids)
    return "Purchase received, going to be processed"


# consume event from kafka
@broker.subscriber("payment-response-event")
async def handle_payment_response(event):
    payment_response = json.loads(event)
    if payment_response["type"] == "PaymentSucceeded":
        await finalize_purchase(payment_response)


async def finalize_purchase(payment_response, db: Session = Depends(get_db)):
    user_id = payment_response["user_id"]
    flights_ids = payment_response["flights_ids"]
    for flight_id in flights_ids:
        purchased_flights = PurchasedFlight(user_id=user_id, flight_id=flight_id)
        db.add(purchased_flights)
        db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.flight_id == flight_id).delete()
    db.commit()
