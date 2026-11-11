from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from app import store

router = APIRouter(prefix="/sales", tags=["Sales"])

sales = []
next_sale_id = 1


class SaleCreate(BaseModel):
    product_id: int
    product_name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    total: float = Field(gt=0)
    customer: str
    date: str


@router.get("/")
def get_sales():
    return sales


@router.post("/")
def create_sale(sale: SaleCreate):
    global next_sale_id

    product = next(
        (p for p in store.products if p["id"] == sale.product_id),
        None
    )

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product["stock"] < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    if sale.unit_price != product["price"]:
        raise HTTPException(status_code=400, detail="Invalid product price")

    new_sale = sale.model_dump()
    new_sale["total"] = product["price"] * sale.quantity
    new_sale["id"] = next_sale_id

    product["stock"] -= sale.quantity
    sales.append(new_sale)
    next_sale_id += 1

    return new_sale