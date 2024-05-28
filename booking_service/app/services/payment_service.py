import random

from .cart_service import add_flight_to_cart
from ..database import get_db
from ..models import PurchasedFlight, CartItem
from ..services.kafka_events_utils import kafka_router


# consume event from kafka
@kafka_router.subscriber("payment-request")
async def handle_payment_request(msg):
    print('Received message to handle payment: {}'.format(msg))
    db = get_db()
    new_payment_status = simulate_payment_status()
    await update_payment_status_in_db(msg.user_id, msg.purchase_ids, new_payment_status, db)
    if new_payment_status == "PaymentFailed":
        await recreate_cart(db, msg)


async def recreate_cart(db, msg):
    for purchase_id in msg.purchase_ids:
        purchased_flight = db.query(PurchasedFlight).filter(
            PurchasedFlight.user_id == msg.user_id,
            PurchasedFlight.id == purchase_id
        ).first()
        flight_id = purchased_flight.flight_id
        await add_flight_to_cart(get_db(), flight_id, msg.user_id)


async def simulate_payment_status() -> str:
    payment_response = random.choices([True, False], weights=[0.8, 0.2])[0]
    new_payment_status = "PaymentSucceeded" if payment_response else "PaymentFailed"
    return new_payment_status


async def update_payment_status_in_db(user_id, purchase_ids, new_payment_status, db):
    for purchase_id in purchase_ids:
        purchased_flight = db.query(PurchasedFlight).filter(
            PurchasedFlight.user_id == user_id,
            PurchasedFlight.id == purchase_id
        ).first()

        purchased_flight.payment_status = new_payment_status

    db.commit()


async def save_purchases_with_pending_payment(user_id, flights_ids, db):
    purchase_ids = []
    for flight_id in flights_ids:
        purchased_flights = PurchasedFlight(user_id=user_id, flight_id=flight_id, payment_status='pending')
        db.add(purchased_flights)
        purchase_ids.append(flight_id)
        db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.flight_id == flight_id).delete()
    db.commit()
    return purchase_ids
