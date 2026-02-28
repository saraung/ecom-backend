from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate
from app.services.order_service import OrderService
from app.core.dependencies import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order(order_data: OrderCreate, user_id: int, db: Session = Depends(get_db)):
    return OrderService.create_order(db, order_data, user_id)

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    return OrderService.get_order_by_id(db, order_id)

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return OrderService.delete_order(db, order_id)