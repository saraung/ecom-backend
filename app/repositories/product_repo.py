from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductRepository:
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_all_products(db: Session, skip: int = 0, limit: int = 10) -> list[Product]:
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        db_product = Product(**product_data.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def update_product(db: Session, product: Product, product_data: ProductUpdate) -> Product:
        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()