from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str
    is_active: Optional[bool] = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    category: Optional[str]
    is_active: Optional[bool]

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True