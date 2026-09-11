from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db

from schemas.customer import (
    CustomerCreate,
    CustomerResponse
)

from services.customer_service import (
    get_customers,
    get_customer,
    add_customer,
    update_customer_data,
    remove_customer
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.get("/", response_model=list[CustomerResponse])
def read_customers(
    db: Session = Depends(get_db)
):
    return get_customers(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return get_customer(db, customer_id)


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    return add_customer(
        db,
        customer.name,
        customer.phone,
        customer.email,
        customer.address
    )


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    return update_customer_data(
        db,
        customer_id,
        customer.name,
        customer.phone,
        customer.email,
        customer.address
    )


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return remove_customer(db, customer_id)