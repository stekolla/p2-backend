from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Customer Schema
class CustomerBase(BaseModel):
    email: EmailStr
    phone: str
    first_name: str
    last_name: str


class CustomerCreate(CustomerBase):
    pass  # Used for creating a customer


class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True  # Allows ORM conversion

# Address Schema
class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    type: str  # "billing" or "shipping"


class AddressResponse(AddressBase):
    id: int

    class Config:
        from_attributes = True

# Order Schema
class OrderBase(BaseModel):
    customer_id: int
    order_time: datetime
    store_purchase: bool


class OrderCreate(OrderBase):
    pass  # Used when creating an order


class OrderResponse(OrderBase):
    id: int
    billing_address: Optional[AddressResponse] = None
    shipping_addresses: List[AddressResponse] = []

    class Config:
        from_attributes = True
