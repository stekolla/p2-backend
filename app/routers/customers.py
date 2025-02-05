from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

router = APIRouter()


@router.post("/customers", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    if crud.get_customer_by_email(db, customer.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_customer(db, customer)
