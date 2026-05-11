from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="User Service - Phase 2",
    docs_url="/users/docs",
    openapi_url="/users/openapi.json",
)

app.include_router(router, prefix="/users")


@app.get("/users/")
async def root():
    return {"message": "User Service Running"}