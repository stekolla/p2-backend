def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Pier 2 Imports API"