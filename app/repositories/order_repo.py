from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderItemCreate


class OrderRepository:
    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order | None:
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def get_orders_by_user_id(
        db: Session, user_id: int, skip: int = 0, limit: int = 10
    ) -> list[Order]:
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_order(
        db: Session,
        user_id: int,
        total_amount: float,
        status: str = "pending",
        address_line1: str | None = None,
        address_line2: str | None = None,
        city: str | None = None,
        state: str | None = None,
        pincode: str | None = None,
        country: str | None = "India",
    ) -> Order:
        db_order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status=status,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            pincode=pincode,
            country=country,
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    @staticmethod
    def get_all_orders(
        db: Session, skip: int = 0, limit: int = 50
    ) -> list[Order]:
        return (
            db.query(Order)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_order_status(db: Session, order: Order, new_status: str) -> Order:
        order.status = new_status
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def delete_order(db: Session, order: Order) -> None:
        db.delete(order)
        db.commit()


class OrderItemRepository:
    @staticmethod
    def create_order_item(
        db: Session,
        order_id: int,
        product_id: int,
        quantity: int,
        price_at_purchase: float,
    ) -> OrderItem:
        db_order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_at_purchase=price_at_purchase,
        )
        db.add(db_order_item)
        db.commit()
        db.refresh(db_order_item)
        return db_order_item

    @staticmethod
    def get_order_items_by_order_id(
        db: Session, order_id: int
    ) -> list[OrderItem]:
        return (
            db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        )