import asyncio
from fastapi import FastAPI
from app.api.routes import router
from app.core.database import Base, engine
from app.events.user_registered_consumer import consume_user_registered

app = FastAPI(
    title="User Service - Phase 3 Kafka",
    docs_url="/users/docs",
    openapi_url="/users/openapi.json",
)

app.include_router(router, prefix="/users")
consumer_task: asyncio.Task | None = None


@app.on_event("startup")
async def startup_event():
    global consumer_task
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    consumer_task = asyncio.create_task(consume_user_registered())


@app.on_event("shutdown")
async def shutdown_event():
    if consumer_task:
        consumer_task.cancel()


@app.get("/users/")
async def root():
    return {"message": "User Service Running with Kafka Consumer"}
