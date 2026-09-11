#Repository as the database worker.

from sqlalchemy.orm import Session
from database.models import Product


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(
        Product.id == product_id
    ).first()


def create_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def update_product(db: Session, product: Product):
    db.commit()
    db.refresh(product)

    return product


def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()