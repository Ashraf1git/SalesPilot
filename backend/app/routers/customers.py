from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app import store

router = APIRouter(prefix="/customers", tags=["Customers"])

customers = []
next_customer_id = 1


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2)
    email: str
    phone: str
    address: str = ""


@router.get("/")
def get_customers():
    return customers


@router.post("/")
def add_customer(customer: CustomerCreate):
    global next_customer_id

    new_customer = customer.model_dump()
    new_customer["id"] = next_customer_id
    new_customer["purchase_history"] = []

    customers.append(new_customer)
    next_customer_id += 1

    return new_customer


@router.get("/{customer_id}")
def get_customer(customer_id: int):
    for customer in customers:
        if customer["id"] == customer_id:
            return customer

    raise HTTPException(status_code=404, detail="Customer not found")


@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    for index, customer in enumerate(customers):
        if customer["id"] == customer_id:
            return customers.pop(index)

    raise HTTPException(status_code=404, detail="Customer not found")