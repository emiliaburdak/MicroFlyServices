import os

from faststream.kafka.fastapi import KafkaRouter

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
kafka_router = KafkaRouter(KAFKA_BOOTSTRAP_SERVERS)
