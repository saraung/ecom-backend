from pydantic import BaseModel, ConfigDict
from typing import List, Literal, Optional
from datetime import datetime

OrderStatus = Literal["pending", "processing", "shipped", "delivered", "cancelled"]


class OrderStatusUpdate(BaseModel):
    """Body for PATCH /orders/{id} — admin-only status update."""

    status: OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    price_at_purchase: float
    image_url: Optional[str] = None  # pulled from product relationship

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj, **kwargs):
        """Pull image_url from the related product when constructing from ORM."""
        instance = super().model_validate(obj, **kwargs)
        # If constructed from an ORM OrderItem, grab product.image_url
        if hasattr(obj, "product") and obj.product is not None:
            instance.image_url = obj.product.image_url
        return instance


class OrderBase(BaseModel):
    status: Optional[str] = "pending"


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderResponse(OrderBase):
    id: int
    user_id: int
    total_amount: float
    items: List[OrderItemResponse]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)