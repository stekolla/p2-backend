
def test_get_orders_by_billing_zip(db, client):
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
    order = client.post("/order/", json={
        "customer_id": customer_id,
        "billing_address_id": address_id,
    })
    order_id = order.json()["id"]

    client.post(f"/order/{order_id}/items/", json={
        "description": "Test Item",
        "quantity": 1,
        "address_id": address_id,
        "is_in_store_pickup": False
    })

    client.post(f"/order/{order_id}/items/", json={
        "description": "Test Item",
        "quantity": 1,
        "is_in_store_pickup": True
    })

    response = client.get("/analytics/orders/billing/")
    assert response.status_code == 200
    assert response.json() == [{"zip_code": "12345", "order_count": 1}]


def test_get_orders_by_shipping_zip(db, client):
    response = client.get("/analytics/orders/shipping/")
    assert response.status_code == 200
    assert response.json() == [{"zip_code": "12345", "order_count": 1}]


def test_get_in_store_orders_by_time(db, client):
    customer = client.get(
        "/customer/", params={"email": "john.doe@example.com"})
    customer_id = customer.json()["id"]

    order_id = client.get(f"/customer/{customer_id}/orders/").json()[0]["id"]
    order = client.get(f"/order/{order_id}").json()
    order_hour = order["created_at"].split("T")[1].split(":")[0]

    response = client.get("/analytics/orders/time/")
    assert response.status_code == 200
    assert response.json() == [{"hour": order_hour, "order_count": 1}]


def test_get_top_in_store_customers(db, client):
    customer = client.get(
        "/customer/", params={"email": "john.doe@example.com"})
    customer_id = customer.json()["id"]

    response = client.get("/analytics/orders/top/")

    assert response.status_code == 200
    assert response.json() == [{
        "customer_id": customer_id,
        "first_name": "John",
        "last_name": "Doe",
        "pickup_count": 1
    }]
