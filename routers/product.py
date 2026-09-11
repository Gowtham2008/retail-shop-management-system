from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.product import ProductCreate, ProductUpdate

from services.product_service import (
    get_products,
    get_product,
    add_product,
    update_product_data,
    patch_product_data,
    remove_product
)

router = APIRouter()


# GET ALL PRODUCTS
@router.get("/products")
def read_products(db: Session = Depends(get_db)):
    return get_products(db)


# GET PRODUCT BY ID
@router.get("/products/{product_id}")
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return get_product(db, product_id)


# CREATE PRODUCT
@router.post("/products", status_code=201)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return add_product(
        db,
        product.name,
        product.price
    )


# PUT - FULL UPDATE
@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return update_product_data(
        db,
        product_id,
        product.name,
        product.price
    )


# PATCH - PARTIAL UPDATE
@router.patch("/products/{product_id}")
def partial_update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    return patch_product_data(
        db,
        product_id,
        product.name,
        product.price
    )


# DELETE PRODUCT
@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return remove_product(db, product_id)

@router.patch("/products/{product_id}/stock")
def add_stock(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):

    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Stock quantity must be greater than 0"
        )

    product = get_product(db, product_id)

    product.stock_quantity += quantity

    db.commit()
    db.refresh(product)

    return {
        "message": "Stock added successfully",
        "stock_quantity": product.stock_quantity
    }