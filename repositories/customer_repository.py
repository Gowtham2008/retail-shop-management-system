from sqlalchemy.orm import Session
from database.models import Customer


def get_all_customers(db: Session):
    return db.query(Customer).all()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(
        Customer.id == customer_id
    ).first()


def create_customer(db: Session, customer: Customer):
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer: Customer):
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer: Customer):
    db.delete(customer)
    db.commit()