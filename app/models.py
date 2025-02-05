import uuid
from sqlalchemy import (
    Column, String, Boolean, Integer, ForeignKey, Text, TIMESTAMP, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)

    orders = relationship("Order", back_populates="customer")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey(
        "customers.id", ondelete="CASCADE"), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)  # Assuming US states
    zip_code = Column(String(10), nullable=False)

    customer = relationship("Customer")
    orders = relationship("Order", back_populates="billing_address")


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey(
        "customers.id", ondelete="CASCADE"), nullable=False)
    billing_address_id = Column(UUID(as_uuid=True), ForeignKey(
        "addresses.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    customer = relationship("Customer", back_populates="orders")
    billing_address = relationship("Address", back_populates="orders")
    items = relationship("OrderItem", back_populates="order",
                         cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey(
        "orders.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now())
    address_id = Column(UUID(as_uuid=True), ForeignKey(
        "addresses.id", ondelete="SET NULL"), nullable=True)
    is_in_store_pickup = Column(Boolean, nullable=False)

    order = relationship("Order", back_populates="items")
    address = relationship("Address")
