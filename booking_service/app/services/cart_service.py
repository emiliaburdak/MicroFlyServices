import json
from datetime import datetime

from ..models import CartItem
from ..services.kafka_events_utils import send_to_kafka


async def add_flight_to_cart(db, flight_id, user_id):
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
