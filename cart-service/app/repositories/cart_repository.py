from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cart import CartItem


class CartRepository:
    @staticmethod
    async def add_item(db: AsyncSession, user_id: int, product: dict, quantity: int) -> CartItem:
        result = await db.execute(
            select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product["id"])
        )
        item = result.scalar_one_or_none()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(
                user_id=user_id,
                product_id=product["id"],
                product_name=product["name"],
                unit_price=product["price"],
                quantity=quantity,
            )
            db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def list_items(db: AsyncSession, user_id: int) -> list[CartItem]:
        result = await db.execute(select(CartItem).where(CartItem.user_id == user_id).order_by(CartItem.id.desc()))
        return list(result.scalars().all())
