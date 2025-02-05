from sqlalchemy.orm import Session
from app import models, schemas

# CRUD for Customer
def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()


def get_customer_by_phone(db: Session, phone: str):
    return db.query(models.Customer).filter(models.Customer.phone == phone).first()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    new_customer = models.Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

# CRUD for Order
def create_order(db: Session, order: schemas.OrderCreate):
    new_order = models.Order(**order.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_orders_by_customer(db: Session, customer_id: int):
    return db.query(models.Order).filter(models.Order.customer_id == customer_id).all()

# Analytics Functions
def get_order_count_by_billing_zip(db: Session):
    return db.execute("SELECT zip_code, COUNT(*) FROM addresses WHERE type='billing' GROUP BY zip_code ORDER BY COUNT(*) DESC").fetchall()


def get_top_customers(db: Session):
    return db.execute("SELECT customer_id, COUNT(*) FROM orders WHERE store_purchase=1 GROUP BY customer_id ORDER BY COUNT(*) DESC LIMIT 5").fetchall()
