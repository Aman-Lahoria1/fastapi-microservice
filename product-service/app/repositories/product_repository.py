from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product


class ProductRepository:
    @staticmethod
    async def create(db: AsyncSession, product: Product) -> Product:
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def list(db: AsyncSession) -> list[Product]:
        result = await db.execute(select(Product).where(Product.is_active == True).order_by(Product.id.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get(db: AsyncSession, product_id: int) -> Product | None:
        result = await db.execute(select(Product).where(Product.id == product_id, Product.is_active == True))
        return result.scalar_one_or_none()
