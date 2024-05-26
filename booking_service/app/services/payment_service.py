import random

from ..database import get_db
from ..models import PurchasedFlight
from ..services.kafka_events_utils import kafka_router


# consume event from kafka
@kafka_router.subscriber("payment-request")
async def handle_payment_request(msg):
    print('Received message to handle payment: {}'.format(msg))

    new_payment_status = simulate_payment_status()
    await update_payment_status_in_db(msg.user_id, msg.purchase_ids, new_payment_status, db=get_db())


async def simulate_payment_status() -> bool:
    return random.choices([True, False], weights=[0.8, 0.2])[0]


async def update_payment_status_in_db(user_id, purchase_ids, new_payment_status, db):
    for purchase_id in purchase_ids:
        purchased_flight = db.query(PurchasedFlight).filter(
            PurchasedFlight.user_id == user_id,
            PurchasedFlight.id == purchase_id
        ).first()

        purchased_flight.payment_status = new_payment_status
        db.add(purchased_flight)

    db.commit()
