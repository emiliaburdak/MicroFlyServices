from faststream.kafka import KafkaBroker

broker = KafkaBroker("localhost:9092")


async def send_event(topic, event):
    await broker.publish(topic, event.encode('utf-8'))
