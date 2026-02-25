from pydantic import BaseModel
from typing import List, Optional

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    total_price: float
    status: Optional[str] = "Pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    user_id: int
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True