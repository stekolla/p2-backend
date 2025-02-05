from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    orders = relationship("Order", back_populates="customer")


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "billing" or "shipping"
    order_id = Column(Integer, ForeignKey("orders.id"))


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_time = Column(DateTime)
    store_purchase = Column(Boolean, default=False)
    customer = relationship("Customer", back_populates="orders")
    billing_address = relationship(
        "Address", primaryjoin="and_(Order.id==Address.order_id, Address.type=='billing')")
    shipping_addresses = relationship(
        "Address", primaryjoin="and_(Order.id==Address.order_id, Address.type=='shipping')")
