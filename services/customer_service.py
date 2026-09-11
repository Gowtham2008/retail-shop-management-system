from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import Customer

from repositories.customer_repository import (
    get_all_customers,
    get_customer_by_id,
    create_customer,
    update_customer,
    delete_customer
)


def get_customers(db: Session):
    return get_all_customers(db)


def get_customer(db: Session, customer_id: int):

    customer = get_customer_by_id(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


def add_customer(
    db: Session,
    name: str,
    phone: str,
    email: str | None,
    address: str | None
):

    customer = Customer(
        name=name,
        phone=phone,
        email=email,
        address=address
    )

    return create_customer(db, customer)


def update_customer_data(
    db: Session,
    customer_id: int,
    name: str,
    phone: str,
    email: str | None,
    address: str | None
):

    customer = get_customer_by_id(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.name = name
    customer.phone = phone
    customer.email = email
    customer.address = address

    return update_customer(db, customer)


def remove_customer(db: Session, customer_id: int):

    customer = get_customer_by_id(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    delete_customer(db, customer)

    return {
        "message": "Customer deleted successfully"
    }