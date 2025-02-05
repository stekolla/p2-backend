from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order

router = APIRouter()


@router.get("/orders")
def get_orders(customer_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.customer_id == customer_id).all()
