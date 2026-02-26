from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderItemCreate

class OrderRepository:
    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order:
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def get_orders_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list[Order]:
        return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, user_id: int) -> Order:
        db_order = Order(
            user_id=user_id,
            total_price=order_data.total_price,
            status=order_data.status,
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    @staticmethod
    def delete_order(db: Session, order: Order) -> None:
        db.delete(order)
        db.commit()

class OrderItemRepository:
    @staticmethod
    def create_order_item(db: Session, order_item_data: OrderItemCreate, order_id: int) -> OrderItem:
        db_order_item = OrderItem(
            order_id=order_id,
            product_id=order_item_data.product_id,
            quantity=order_item_data.quantity,
            price=order_item_data.price,
        )
        db.add(db_order_item)
        db.commit()
        db.refresh(db_order_item)
        return db_order_item

    @staticmethod
    def get_order_items_by_order_id(db: Session, order_id: int) -> list[OrderItem]:
        return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()