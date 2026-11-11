import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert "products" in response.json()


def test_add_product():
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "category": "Testing",
            "price": 150,
            "stock": 20,
            "description": "Test item"
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"


def test_invalid_product():
    response = client.post(
        "/products/",
        json={
            "name": "A",
            "category": "Testing",
            "price": -10,
            "stock": -1
        }
    )
    assert response.status_code == 422