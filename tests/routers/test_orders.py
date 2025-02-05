import uuid


def test_add_order(db, client):
    # Create a customer
    customer = client.post("/customer/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890"
    })
    customer_id = customer.json()["id"]

    # Create an address
    address = client.post(f"/customer/{customer_id}/addresses/", json={
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345"
    })
    address_id = address.json()["id"]

    # Add an order
    response = client.post("/order/", json={
        "customer_id": customer_id,
        "billing_address_id": address_id
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Order created"


def test_add_order_item_success(db, client):
    customer_id = client.get(
        "/customer/", params={"email": "john.doe@example.com"}).json()["id"]
    address_id = client.get(
        f"/customer/{customer_id}/addresses/").json()[0]["id"]
    order_id = client.get(f"/customer/{customer_id}/orders/").json()[0]["id"]

    # Add an order item
    response = client.post(f"/order/{order_id}/items/", json={
        "description": "Test Item",
        "quantity": 1,
        "address_id": address_id,
        "is_in_store_pickup": False
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Item added"


def test_add_order_item_order_not_found(db, client):
    # Try to add an order item to a non-existent order
    response = client.post(f"/order/{uuid.uuid4()}/items/", json={
        "description": "Test Item",
        "quantity": 1,
        "address_id": str(uuid.uuid4()),
        "is_in_store_pickup": False
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"
