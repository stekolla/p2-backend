from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models import Customer, Address, Order, OrderItem
import uuid

router = APIRouter()


class OrderCreate(BaseModel):
    customer_id: uuid.UUID
    billing_address_id: uuid.UUID


@router.post("/order/", response_model=dict)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(
        Customer.id == order.customer_id).first()
    billing_address = db.query(Address).filter(
        Address.id == order.billing_address_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if not billing_address:
        raise HTTPException(
            status_code=404, detail="Billing address not found")

    new_order = Order(
        id=uuid.uuid4(),
        customer_id=order.customer_id,
        billing_address_id=order.billing_address_id,
    )
    db.add(new_order)
    db.commit()
    return {"message": "Order created", "id": new_order.id}


@router.get("/order/{order_id}", response_model=dict)
def get_order(order_id: uuid.UUID, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "billing_address_id": order.billing_address_id,
        "created_at": order.created_at,
    }


class OrderItemCreate(BaseModel):
    description: str
    quantity: int
    address_id: Optional[uuid.UUID] = None
    is_in_store_pickup: bool


@router.post("/order/{order_id}/items/", response_model=dict)
def add_order_item(order_id: uuid.UUID, item: OrderItemCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_item = OrderItem(
        id=uuid.uuid4(),
        order_id=order_id,
        description=item.description,
        quantity=item.quantity,
        address_id=item.address_id,
        is_in_store_pickup=item.is_in_store_pickup,
    )
    db.add(new_item)
    db.commit()
    return {"message": "Item added", "id": new_item.id}


@router.get("/order/{order_id}/items/", response_model=list)
def get_order_items(order_id: uuid.UUID, db: Session = Depends(get_db)):
    items = db.query(OrderItem).filter(
        OrderItem.order_id == order_id).all()
    return [{
        "id": i.id,
        "description": i.description,
        "quantity": i.quantity,
        "address_id": i.address_id,
        "is_in_store_pickup": i.is_in_store_pickup,
    } for i in items]

