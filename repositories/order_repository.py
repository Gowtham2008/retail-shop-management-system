from sqlalchemy.orm import Session

from database.models import Order, OrderItem


def create_order(db: Session, order: Order):
    db.add(order)
    db.flush()
    return order


def create_order_item(db: Session, item: OrderItem):
    db.add(item)
    return item


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(
        Order.id == order_id
    ).first()


def get_all_orders(db: Session):
    return db.query(Order).all()


def update_order(db: Session, order: Order):
    db.commit()
    db.refresh(order)
    return order