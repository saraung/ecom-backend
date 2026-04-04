from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.order import Order
from app.schemas.order import OrderCreate
from app.repositories.order_repo import OrderRepository, OrderItemRepository
from app.repositories.product_repo import ProductRepository


class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, user_id: int) -> Order:
        """Create order, auto-calculating total_amount from product prices."""
        total_amount = 0.0
        line_items = []

        for item in order_data.items:
            product = ProductRepository.get_product_by_id(db, item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} not found",
                )
            if product.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product {product.name}",
                )
            price = float(product.price)
            total_amount += price * item.quantity
            line_items.append(
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price_at_purchase": price,
                }
            )

        # Create the order
        addr = order_data.shipping_address
        db_order = OrderRepository.create_order(
            db,
            user_id=user_id,
            total_amount=total_amount,
            status=order_data.status or "pending",
            address_line1=addr.address_line1,
            address_line2=addr.address_line2,
            city=addr.city,
            state=addr.state,
            pincode=addr.pincode,
            country=addr.country,
        )

        # Create order items and decrement stock
        for li in line_items:
            OrderItemRepository.create_order_item(
                db,
                order_id=db_order.id,
                product_id=li["product_id"],
                quantity=li["quantity"],
                price_at_purchase=li["price_at_purchase"],
            )
            # Decrement stock
            product = ProductRepository.get_product_by_id(db, li["product_id"])
            product.stock_quantity -= li["quantity"]
            db.commit()

        db.refresh(db_order)
        return db_order

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order | None:
        return OrderRepository.get_order_by_id(db, order_id)

    @staticmethod
    def get_all_orders(
        db: Session, skip: int = 0, limit: int = 50
    ) -> list[Order]:
        return OrderRepository.get_all_orders(db, skip=skip, limit=limit)

    @staticmethod
    def update_order_status(db: Session, order_id: int, new_status: str) -> Order | None:
        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            return None
        return OrderRepository.update_order_status(db, order, new_status)

    @staticmethod
    def get_orders_by_user(
        db: Session, user_id: int, skip: int = 0, limit: int = 10
    ) -> list[Order]:
        return OrderRepository.get_orders_by_user_id(
            db, user_id, skip=skip, limit=limit
        )

    @staticmethod
    def delete_order(db: Session, order_id: int) -> bool:
        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            return False
        OrderRepository.delete_order(db, order)
        return True