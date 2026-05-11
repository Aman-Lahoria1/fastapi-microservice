from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Auth Service - Phase 2",
    docs_url="/auth/docs",
    openapi_url="/auth/openapi.json",
)

app.include_router(router, prefix="/auth")


@app.get("/auth/")
async def root():
    return {
        "message": "Auth Service Running with PostgreSQL, Redis, Async SQLAlchemy and Alembic"
    }
