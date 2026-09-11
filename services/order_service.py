from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import Order, OrderItem, Product, Customer

from repositories.order_repository import (
    create_order,
    create_order_item,
    get_order_by_id,
    get_all_orders,
    update_order
)


def create_new_order(
    db: Session,
    customer_id: int,
    items
):
    # 1. Check customer
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # 2. Create empty order
    order = Order(
        customer_id=customer_id,
        total_amount=0,
        status="Pending"
    )

    create_order(db, order)

    total_amount = 0

    # 3. Process each product
    for item in items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        # Product doesn't exist
        if product is None:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        # 4. Check stock
        if product.stock_quantity < item.quantity:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}"
            )

        # 5. Calculate subtotal
        subtotal = product.price * item.quantity

        # 6. Create order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
            subtotal=subtotal
        )

        create_order_item(db, order_item)

        # 7. Reduce stock
        product.stock_quantity -= item.quantity

        # 8. Add to total
        total_amount += subtotal

    # 9. Update order total
    order.total_amount = total_amount

    # 10. Save everything
    db.commit()
    db.refresh(order)

    return order


def get_orders(db: Session):
    orders = get_all_orders(db)

    return [
        {
            "id": order.id,
            "customer_id": order.customer_id,
            "order_date": order.order_date,
            "total_amount": order.total_amount,
            "status": order.status,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal
                }
                for item in order.items
            ]
        }
        for order in orders
    ]


def get_order(db: Session, order_id: int):
    order = get_order_by_id(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "order_date": order.order_date,
        "total_amount": order.total_amount,
        "status": order.status,
        "items": [
            {
                "product_id": item.product_id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal
            }
            for item in order.items
        ]
    }


def change_order_status(db: Session, order_id: int, status: str):

    order = get_order_by_id(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    allowed_statuses = ["Pending", "Completed", "Cancelled"]

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid order status"
        )

    # Don't allow changes after cancellation
    if order.status == "Cancelled":
        raise HTTPException(
            status_code=400,
            detail="Cancelled order cannot be changed"
        )

    # Completed order cannot be cancelled
    if order.status == "Completed" and status == "Cancelled":
        raise HTTPException(
            status_code=400,
            detail="Completed order cannot be cancelled"
        )

    # Restore stock when cancelling
    if status == "Cancelled":

        for item in order.items:
            item.product.stock_quantity += item.quantity

    order.status = status

    return update_order(db, order)

def get_customer_orders(db: Session, customer_id: int):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer.orders