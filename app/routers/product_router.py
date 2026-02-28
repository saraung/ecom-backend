from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.product_service import ProductService
from app.core.dependencies import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return ProductService.create_product(db, product_data)

@router.put("/{product_id}")
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    return ProductService.update_product(db, product_id, product_data)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService.delete_product(db, product_id)