import random
from datetime import datetime
from typing import List

from faststream.annotations import FastStream
from faststream.kafka import KafkaBroker
from ..services.kafka_events_utils import send_event

broker = KafkaBroker("localhost:9092")
app = FastStream(broker)


async def simulate_payment(user_id: int, flights_ids: List[int]):
    # 80% success, 20% failure
    payment_success = random.choices([True, False], weights=[0.8, 0.2])[0]
    event_type = "PaymentSucceeded" if payment_success else "PaymentFailed"
    event = {
        "type": event_type,
        "user_id": user_id,
        "flight_id": flights_ids,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Send to kafka
    await send_event("payment-response-event", event)
