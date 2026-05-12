from decimal import Decimal
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: str | None = None
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock: int
    is_active: bool

    class Config:
        from_attributes = True
