from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/productdb"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"


settings = Settings()
