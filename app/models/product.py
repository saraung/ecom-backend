from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)

    price = Column(Numeric(10, 2), nullable=False)  # safe for money
    stock_quantity = Column(Integer, nullable=False, default=0)

    image_url = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product",
        cascade="all, delete",
    )