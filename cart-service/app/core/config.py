from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/cartdb"
    AUTH_SERVICE_URL: str = "http://auth-service:8000"
    PRODUCT_SERVICE_URL: str = "http://product-service:8002"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"


settings = Settings()
