import os

from faststream.kafka.fastapi import KafkaRouter

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
kafka_router = KafkaRouter(KAFKA_BOOTSTRAP_SERVERS)


async def send_to_kafka(topic, msg):
    print(f'Going to send message for topic: {topic}; message: {msg}')
    await kafka_router.broker.publish(message=msg, topic=topic)
