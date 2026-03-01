from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "id" in response.json()

def test_login_user():
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_user():
    response = client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

def test_create_product():
    response = client.post("/products/", json={"name": "Product A", "price": 100.0})
    assert response.status_code == 200
    assert response.json()["name"] == "Product A"

def test_create_order():
    response = client.post("/orders/", json={"user_id": 1, "product_id": 1, "quantity": 2})
    assert response.status_code == 200
    assert response.json()["quantity"] == 2