from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app.models import Customer, Order, Address
import uuid

router = APIRouter()


class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str


@router.post("/customer/", response_model=dict)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    existing = db.query(Customer).filter(
        (Customer.email == customer.email) | (Customer.phone == customer.phone)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Customer already exists")

    new_customer = Customer(
        id=uuid.uuid4(),
        first_name=customer.first_name,
        last_name=customer.last_name,
        email=customer.email,
        phone=customer.phone,
    )
    db.add(new_customer)
    db.commit()
    return {"message": "Customer created", "id": new_customer.id}


@router.get("/customer/", response_model=dict)
def find_customer(
    email: str = Query(None, description="Customer's email address"),
    phone: str = Query(None, description="Customer's phone number"),
    db: Session = Depends(get_db)
):
    if not email and not phone:
        raise HTTPException(
            status_code=400, detail="Email or phone number is required")

    customer_query = db.query(Customer)
    if email:
        customer_query = customer_query.filter(Customer.email == email)
    if phone:
        customer_query = customer_query.filter(Customer.phone == phone)

    customer = customer_query.first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "id": customer.id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone": customer.phone,
    }


@router.get("/customer/{customer_id}", response_model=dict)
def get_customer(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {
        "id": customer.id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone": customer.phone,
    }


@router.get("/customer/{customer_id}/orders/", response_model=List[dict])
def get_customer_orders(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(
        Order.customer_id == customer_id).all()
    return [{
        "id": o.id,
        "customer_id": o.customer_id,
        "billing_address_id": o.billing_address_id,
    } for o in orders]


class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


@router.post("/customer/{customer_id}/addresses/", response_model=dict)
def add_customer_address(customer_id: uuid.UUID, address: AddressCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    new_address = Address(
        id=uuid.uuid4(),
        customer_id=customer_id,
        street=address.street,
        city=address.city,
        state=address.state,
        zip_code=address.zip_code,
    )
    db.add(new_address)
    db.commit()
    return {"message": "Address added", "id": new_address.id}


@router.get("/customer/{customer_id}/addresses/", response_model=List[dict])
def get_customer_addresses(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    addresses = db.query(Address).filter(
        Address.customer_id == customer_id).all()
    return [{"id": a.id, "street": a.street, "city": a.city, "state": a.state, "zip_code": a.zip_code} for a in addresses]
