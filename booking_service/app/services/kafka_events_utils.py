from faststream import FastStream
from faststream.kafka import KafkaBroker
from faststream.kafka.fastapi import KafkaRouter

# kafka_router = KafkaRouter("localhost:9092")
broker = KafkaBroker("kafka:9092")
app = FastStream(broker)


# def get_kafka_broker():
#     return broker


@broker.publisher("booking-events")
async def handle_msg(msg: str) -> str:
    return msg


async def send_event(topic, event):
    # broker = get_kafka_broker()
    # await broker.connect()
    await handle_msg(event)
    # try:
    #     print(f'going to send for {topic}: {event}')
    #     result = await broker.publish(message=event, topic=topic)
    #     print(result)
    # except Exception as e:
    #     print(f"Error publishing event: {e}")
    # finally:
    #     await broker.close()
