from fastapi import FastAPI
from app.api.routes import router
from app.core.database import Base, engine
from app.events.kafka import kafka_producer

app = FastAPI(
    title="Product Service",
    docs_url="/products/docs",
    openapi_url="/products/openapi.json",
)


@app.get("/products/health")
async def health():
    return {"status": "product-service-ok"}


app.include_router(router, prefix="/products")


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await kafka_producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.stop()
