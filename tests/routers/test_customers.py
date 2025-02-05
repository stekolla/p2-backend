import uuid


def test_create_customer(db, client):
    response = client.post("/customer/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Customer created"


def test_create_existing_customer(db, client):
    client.post("/customer/", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "0987654321"
    })
    response = client.post("/customer/", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "0987654321"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Customer already exists"


def test_find_customer_by_email(db, client):
    response = client.get(
        "/customer/", params={"email": "john.doe@example.com"})
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"


def test_find_customer_by_phone(db, client):
    response = client.get("/customer/", params={"phone": "1234567890"})
    assert response.status_code == 200
    assert response.json()["phone"] == "1234567890"


def test_find_customer_not_found(db, client):
    response = client.get(
        "/customer/", params={"email": "nonexistent@example.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_get_customer(db, client):
    customer_id = client.get(
        "/customer/", params={"email": "john.doe@example.com"}).json()["id"]
    response = client.get(f"/customer/{customer_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"


def test_get_customer_not_found(db, client):
    response = client.get(f"/customer/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_get_customer_orders(db, client):
    customer_id = client.get(
        "/customer/", params={"email": "john.doe@example.com"}).json()["id"]
    response = client.get(f"/customer/{customer_id}/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_customer_address(db, client):
    customer_id = client.get(
        "/customer/", params={"email": "john.doe@example.com"}).json()["id"]
    response = client.post(f"/customer/{customer_id}/addresses/", json={
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Address added"


def test_get_customer_addresses(db, client):
    customer_id = client.get(
        "/customer/", params={"email": "john.doe@example.com"}).json()["id"]
    response = client.get(f"/customer/{customer_id}/addresses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
