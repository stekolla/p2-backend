from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


@router.get("/analytics/billing_zip")
def orders_by_billing_zip(db: Session = Depends(get_db)):
    return db.execute("SELECT zip_code, COUNT(*) FROM addresses WHERE type='billing' GROUP BY zip_code ORDER BY COUNT(*) DESC").fetchall()


@router.get("/analytics/top_customers")
def top_customers(db: Session = Depends(get_db)):
    return db.execute("SELECT customer_id, COUNT(*) as order_count FROM orders WHERE store_purchase=1 GROUP BY customer_id ORDER BY order_count DESC LIMIT 5").fetchall()
