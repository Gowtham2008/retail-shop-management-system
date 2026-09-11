from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.order import (OrderCreate,OrderStatusUpdate,OrderResponse)

from services.order_service import (
    create_new_order,
    get_orders,
    get_order,
    change_order_status
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# CREATE ORDER
@router.post("/")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    return create_new_order(
        db,
        order.customer_id,
        order.items
    )


# GET ALL ORDERS
@router.get("/", response_model=list[OrderResponse])
def read_orders(
    db: Session = Depends(get_db)
):
    return get_orders(db)


# GET ORDER BY ID
@router.get("/{order_id}",response_model=OrderResponse)
def read_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return get_order(db, order_id)


# UPDATE ORDER STATUS
@router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    return change_order_status(
        db,
        order_id,
        data.status
    )

from services.order_service import (create_new_order, get_orders,get_order, change_order_status, get_customer_orders)
@router.get("/customer/{customer_id}")
def read_customer_orders(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return get_customer_orders(db, customer_id)