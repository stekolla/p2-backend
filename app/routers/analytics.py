from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from app.database import get_db
from app.models import Customer, Address, Order, OrderItem
from typing import List

router = APIRouter()


@router.get("/analytics/orders/billing/", response_model=List[dict])
def get_orders_by_billing_zip(
    order: str = Query("desc", description="Sort order: 'asc' or 'desc'"),
    db: Session = Depends(get_db)
):
    sort_order = desc if order == "desc" else asc

    results = (
        db.query(Address.zip_code, func.count(Order.id).label("order_count"))
        .join(Order, Address.id == Order.billing_address_id)
        .group_by(Address.zip_code)
        .order_by(sort_order("order_count"))
        .all()
    )

    return [{"zip_code": row.zip_code, "order_count": row.order_count} for row in results]


@router.get("/analytics/orders/shipping/", response_model=List[dict])
def get_orders_by_shipping_zip(
    order: str = Query("desc", description="Sort order: 'asc' or 'desc'"),
    db: Session = Depends(get_db)
):
    sort_order = desc if order == "desc" else asc

    results = (
        db.query(Address.zip_code, func.count(OrderItem.order_id).label("order_count"))
        .join(OrderItem, Address.id == OrderItem.address_id)
        .group_by(Address.zip_code)
        .order_by(sort_order("order_count"))
        .all()
    )

    return [{"zip_code": row.zip_code, "order_count": row.order_count} for row in results]


@router.get("/analytics/orders/time/", response_model=List[dict])
def get_in_store_orders_by_time(db: Session = Depends(get_db)):
    results = (
        db.query(
            func.extract('hour', Order.created_at).label("hour"),
            func.count(Order.id).label("order_count")
        )
        .join(OrderItem, Order.id == OrderItem.order_id)
        .filter(OrderItem.is_in_store_pickup == True)
        .group_by("hour")
        .order_by("order_count")
        .all()
    )

    return [{"hour": row.hour, "order_count": row.order_count} for row in results]


@router.get("/analytics/orders/top/", response_model=List[dict])
def get_top_in_store_customers(db: Session = Depends(get_db)):
    results = (
        db.query(Customer.id, Customer.first_name, Customer.last_name, func.count(OrderItem.id).label("pickup_count"))
        .join(Order, Order.customer_id == Customer.id)
        .join(OrderItem, Order.id == OrderItem.order_id)
        .filter(OrderItem.is_in_store_pickup == True)
        .group_by(Customer.id)
        .order_by(desc("pickup_count"))
        .limit(5)
        .all()
    )

    return [
        {
            "customer_id": row.id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "pickup_count": row.pickup_count,
        } for row in results
    ]