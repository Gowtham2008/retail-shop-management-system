from pydantic import BaseModel, Field
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: str

class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    order_date: datetime
    total_amount: float
    status: str
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True
 