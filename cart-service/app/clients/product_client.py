import httpx
from fastapi import HTTPException
from app.core.config import settings


class ProductClient:
    @staticmethod
    async def get_product(product_id: int) -> dict:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}"
            )
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Product not found")
        if response.status_code != 200:
            raise HTTPException(status_code=503, detail="Product service unavailable")
        return response.json()
