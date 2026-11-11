from fastapi import APIRouter, HTTPException, Query
from app import store
from app.schemas import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def get_products(
    search: str = "",
    category: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    filtered = store.products

    if search:
        filtered = [
            p for p in filtered
            if search.lower() in p["name"].lower()
        ]

    if category:
        filtered = [
            p for p in filtered
            if p["category"].lower() == category.lower()
        ]

    start = (page - 1) * limit

    return {
        "total": len(filtered),
        "page": page,
        "limit": limit,
        "products": filtered[start:start + limit]
    }


@router.get("/{product_id}")
def get_product(product_id: int):
    for product in store.products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


@router.post("/")
def add_product(product: ProductCreate):
    new_product = product.model_dump()
    new_product["id"] = store.next_product_id
    store.next_product_id += 1
    store.products.append(new_product)
    return new_product


@router.put("/{product_id}")
def update_product(product_id: int, updated_product: ProductUpdate):
    for index, product in enumerate(store.products):
        if product["id"] == product_id:
            store.products[index] = {
                "id": product_id,
                **updated_product.model_dump()
            }
            return store.products[index]

    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(store.products):
        if product["id"] == product_id:
            return store.products.pop(index)

    raise HTTPException(status_code=404, detail="Product not found")