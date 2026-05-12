from fastapi import FastAPI
from app.api.routes import router
from app.core.database import Base, engine
from app.events.kafka import kafka_producer

app = FastAPI(
    title="Cart Service", docs_url="/cart/docs", openapi_url="/cart/openapi.json"
)


@app.get("/cart/health")
async def health():
    return {"status": "cart-service-ok"}


app.include_router(router, prefix="/cart")


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await kafka_producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.stop()
