from fastapi import FastAPI
from app.api.routes import router
from app.events.kafka import kafka_producer

app = FastAPI(
    title="Auth Service - Phase 3 Kafka",
    docs_url="/auth/docs",
    openapi_url="/auth/openapi.json",
)

app.include_router(router, prefix="/auth")


@app.on_event("startup")
async def startup_event():
    await kafka_producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.stop()


@app.get("/auth/")
async def root():
    return {"message": "Auth Service Running with PostgreSQL, Redis and Kafka Producer"}
