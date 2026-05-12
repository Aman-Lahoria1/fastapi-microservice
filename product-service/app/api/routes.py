from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.events.kafka import kafka_producer
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = await ProductRepository.create(db, Product(**payload.model_dump()))
    await kafka_producer.publish(
        topic="product.created",
        key=str(product.id),
        event={
            "event_type": "product.created",
            "product_id": product.id,
            "name": product.name,
            "price": str(product.price),
            "stock": product.stock,
        },
    )
    return product


@router.get("/", response_model=list[ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await ProductRepository.list(db)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await ProductRepository.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
