from fastapi import APIRouter
from app import store
from app.routers import sales

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def dashboard_summary():
    total_products = len(store.products)
    total_stock = sum(p["stock"] for p in store.products)
    inventory_value = sum(
        p["price"] * p["stock"] for p in store.products
    )

    total_sales = len(sales.sales)
    total_revenue = sum(s["total"] for s in sales.sales)

    total_units_sold = sum(
        s["quantity"] for s in sales.sales
    )

    return {
        "total_products": total_products,
        "total_stock": total_stock,
        "inventory_value": round(inventory_value, 2),
        "total_sales": total_sales,
        "total_revenue": round(total_revenue, 2),
        "total_units_sold": total_units_sold
    }


@router.get("/top-products")
def top_products():
    product_sales = {}

    for sale in sales.sales:
        name = sale["product_name"]
        product_sales[name] = (
            product_sales.get(name, 0) + sale["quantity"]
        )

    return [
        {"product": name, "quantity_sold": quantity}
        for name, quantity in sorted(
            product_sales.items(),
            key=lambda item: item[1],
            reverse=True
        )
    ]
@router.get("/low-stock")
def low_stock():
    return [
        product for product in store.products
        if product["stock"] <= 10
    ]