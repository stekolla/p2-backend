# Used to seed the database with sample data; mostly for running locally and not really meant for testing

import uuid
import random
import datetime
from models import Base, Customer, Address, Order, OrderItem
from database import get_db

def create_sample_data(session):
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Steven", "Emily"]
    last_names = ["Smith", "Johnson", "Brown", "Lee", "Kollars", "Davis"]
    item_descriptions = ["Sofa Set", "Dining Table", "Office Chair", "Bookshelf", "Bed Frame", "Coffee Table", "Lamp"]
    city_state_zip = [
        ("New York", "NY", "10001"),
        ("Los Angeles", "CA", "90001"),
        ("Chicago", "IL", "60007"),
        ("Houston", "TX", "77001")
    ]
    
    # Create Customers
    for i in range(6):
        customer = Customer(
            id=uuid.uuid4(),
            first_name=first_names[i],
            last_name=last_names[i],
            email=f"user{i}@example.com",
            phone=f"555-000{i}"
        )
        session.add(customer)

        addresses = []
        for _ in range(random.randint(3, 8)):
            city, state, zip_code = random.choice(city_state_zip)
            address = Address(
                id=uuid.uuid4(),
                customer_id=customer.id,
                street=f"{random.randint(100, 999)} Main St",
                city=city,
                state=state,
                zip_code=zip_code
            )
            session.add(address)
            addresses.append(address)

        orders = []
        order_items = []
        for _ in range(random.randint(3, 8)):
            order = Order(
                id=uuid.uuid4(),
                customer_id=customer.id,
                billing_address_id=random.choice(addresses).id,
                created_at=datetime.datetime(
                    random.randint(datetime.datetime.now().year - 2, datetime.datetime.now().year),
                    random.randint(1, 12),
                    random.randint(1, 28),
                    random.randint(8, 18),
                    random.randint(0, 59),
                    random.randint(0, 59)
                )
            )
            session.add(order)
            orders.append(order)

            for _ in range(random.randint(3, 8)):
                is_pickup = random.choice([True, False])
                item = OrderItem(
                    id=uuid.uuid4(),
                    order_id=order.id,
                    description=random.choice(item_descriptions),
                    quantity=random.randint(1, 5),
                    address_id=None if is_pickup else random.choice(addresses).id,
                    is_in_store_pickup=is_pickup
                )
                session.add(item)
                order_items.append(item)

    session.commit()
    print("Sample data successfully inserted!")


if __name__ == "__main__":
    create_sample_data(next(get_db()))
