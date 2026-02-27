from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate
from app.repositories.order_repo import OrderRepository, OrderItemRepository

class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, user_id: int) -> Order:
        db_order = OrderRepository.create_order(db, order_data, user_id)
        for item in order_data.items:
            OrderItemRepository.create_order_item(db, item, db_order.id)
        return db_order

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order:
        return OrderRepository.get_order_by_id(db, order_id)

    @staticmethod
    def delete_order(db: Session, order_id: int) -> bool:
        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            return False
        OrderRepository.delete_order(db, order)
        return True