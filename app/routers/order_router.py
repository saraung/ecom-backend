from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.core.database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate, user_id: int, db: Session = Depends(get_db)
):
    return OrderService.create_order(db, order_data, user_id)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@router.get("/user/{user_id}", response_model=list[OrderResponse])
def get_user_orders(
    user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return OrderService.get_orders_by_user(db, user_id, skip=skip, limit=limit)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    success = OrderService.delete_order(db, order_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )