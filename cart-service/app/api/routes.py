from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.clients.auth_client import AuthClient
from app.clients.product_client import ProductClient
from app.core.database import get_db
from app.events.kafka import kafka_producer
from app.repositories.cart_repository import CartRepository
from app.schemas.cart import AddCartItemRequest, CartItemResponse

router = APIRouter()


@router.post("/items", response_model=CartItemResponse, status_code=201)
async def add_item(
    payload: AddCartItemRequest,
    authorization: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
):
    auth_user = await AuthClient.validate(authorization)
    product = await ProductClient.get_product(payload.product_id)
    if product["stock"] < payload.quantity:
        raise HTTPException(status_code=400, detail="Not enough product stock")
    item = await CartRepository.add_item(
        db, auth_user["user_id"], product, payload.quantity
    )
    await kafka_producer.publish(
        topic="cart.item_added",
        key=str(auth_user["user_id"]),
        event={
            "event_type": "cart.item_added",
            "user_id": auth_user["user_id"],
            "product_id": item.product_id,
            "quantity": item.quantity,
        },
    )
    return item


@router.get("/items", response_model=list[CartItemResponse])
async def list_items(
    authorization: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
):
    auth_user = await AuthClient.validate(authorization)
    return await CartRepository.list_items(db, auth_user["user_id"])
