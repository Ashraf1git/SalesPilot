import requests

API_URL = "http://127.0.0.1:8000"


def get_products():
    response = requests.get(f"{API_URL}/products/")
    response.raise_for_status()
    return response.json()


def add_product(data):
    response = requests.post(f"{API_URL}/products/", json=data)
    response.raise_for_status()
    return response.json()


def update_product(product_id, data):
    response = requests.put(
        f"{API_URL}/products/{product_id}",
        json=data
    )
    response.raise_for_status()
    return response.json()


def delete_product(product_id):
    response = requests.delete(f"{API_URL}/products/{product_id}")
    response.raise_for_status()
    return response.json()