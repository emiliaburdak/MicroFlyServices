import json
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CartItem, PurchasedFlight
from ..services.booking_service import get_current_user_id
from ..services.kafka_events_utils import send_to_kafka

router = APIRouter()


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
    await send_to_kafka("booking-events", event)

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
    await send_to_kafka("booking-events", event)

    return {"message": "Flight removed from cart"}


@router.post("/purchase/")
async def purchase(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="No items in cart to purchase")

    flights_ids = [cart_item.flight_id for cart_item in cart_items]
    purchase_ids = await save_purchases_with_pending_payment(user_id=user_id, flights_ids=flights_ids, db=db)

    # send event for event sourcing
    event = json.dumps({
        "type": "PurchaseRequest",
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "flights_ids": flights_ids,
    })
    await send_to_kafka(topic="purchase-event", msg=event)

    # send msg to process payment
    process_payment_request = json.dumps({
        "type": "ProcessPayment",
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "purchase_ids": purchase_ids
    })
    await send_to_kafka(topic='payment-request', msg=process_payment_request)

    return "Purchase received, payment is going to be processed soon"


async def save_purchases_with_pending_payment(user_id, flights_ids, db: Session = Depends(get_db)):
    purchase_ids = []
    for flight_id in flights_ids:
        purchased_flights = PurchasedFlight(user_id=user_id, flight_id=flight_id, payment_status='pending')
        db.add(purchased_flights)
        purchase_ids.append(flight_id)
        db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.flight_id == flight_id).delete()
    db.commit()
    return purchase_ids
