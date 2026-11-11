from fastapi import FastAPI
from app.routers import products, sales, customers, dashboard

app = FastAPI(
    title="SalesPilot API",
    description="Business Sales and Inventory Management Platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to SalesPilot API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

app.include_router(products.router)
app.include_router(sales.router)
app.include_router(customers.router)
app.include_router(dashboard.router)