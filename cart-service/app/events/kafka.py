from app.core.config import settings
from common.kafka.producer import KafkaProducerClient

kafka_producer = KafkaProducerClient(settings.KAFKA_BOOTSTRAP_SERVERS)
