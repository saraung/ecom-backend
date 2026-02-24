from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    category = Column(String, nullable=False)
    orders = relationship("OrderItem", back_populates="product")