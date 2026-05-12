import json
from aiokafka import AIOKafkaProducer


class KafkaProducerClient:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer: AIOKafkaProducer | None = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            key_serializer=lambda key: key.encode("utf-8") if key else None,
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def publish(self, topic: str, event: dict, key: str | None = None):
        if not self.producer:
            raise RuntimeError("Kafka producer is not started")
        await self.producer.send_and_wait(topic, value=event, key=key)
