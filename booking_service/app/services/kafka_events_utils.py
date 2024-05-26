import os

from faststream.kafka.fastapi import KafkaRouter

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
kafka_router = KafkaRouter(KAFKA_BOOTSTRAP_SERVERS)


@kafka_router.subscriber("booking-events")
async def handle_msg(msg: str):
    print('Received message: {}'.format(msg))


async def send_event(topic, msg):
    print(f'Going to send message for topic: {topic}; message: {msg}')
    await kafka_router.broker.publish(message=msg, topic=topic)
