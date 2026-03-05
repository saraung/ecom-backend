from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product_repo import ProductRepository


class ProductService:
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product | None:
        return ProductRepository.get_product_by_id(db, product_id)

    @staticmethod
    def get_all_products(
        db: Session, skip: int = 0, limit: int = 20
    ) -> list[Product]:
        return ProductRepository.get_all_products(db, skip=skip, limit=limit)

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        return ProductRepository.create_product(db, product_data)

    @staticmethod
    def update_product(
        db: Session, product_id: int, product_data: ProductUpdate
    ) -> Product | None:
        product = ProductRepository.get_product_by_id(db, product_id)
        if not product:
            return None
        return ProductRepository.update_product(db, product, product_data)

    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        product = ProductRepository.get_product_by_id(db, product_id)
        if not product:
            return False
        ProductRepository.delete_product(db, product)
        return True