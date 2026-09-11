from sqlalchemy.orm import Session
from fastapi import HTTPException

from database.models import Product
from repositories.product_repository import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)


def get_products(db: Session):
    return get_all_products(db)


def get_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


def add_product(db: Session, name: str, price: float):
    new_product = Product(
        name=name,
        price=price
    )

    return create_product(db, new_product)


def update_product_data(
    db: Session,
    product_id: int,
    name: str,
    price: float
):
    product = get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = name
    product.price = price

    return update_product(db, product)


def patch_product_data(
    db: Session,
    product_id: int,
    name: str | None,
    price: float | None
):
    product = get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if name is not None:
        product.name = name

    if price is not None:
        product.price = price

    return update_product(db, product)


def remove_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    delete_product(db, product)

    return {
        "message": "Product deleted successfully"
    }