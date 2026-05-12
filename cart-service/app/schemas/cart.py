from decimal import Decimal
from pydantic import BaseModel, Field


class AddCartItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=50)


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int

    class Config:
        from_attributes = True
