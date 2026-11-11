import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="SalesPilot",
    layout="wide"
)

st.title("SalesPilot")
st.subheader("Business Sales and Inventory Management")

try:
    response = requests.get(f"{API_URL}/products/?limit=100", timeout=5)
    response.raise_for_status()

    products = response.json()["products"]

    total_products = len(products)
    total_stock = sum(p["stock"] for p in products)
    inventory_value = sum(
        p["price"] * p["stock"] for p in products
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", total_products)
    col2.metric("Total Stock", total_stock)
    col3.metric("Inventory Value", f"₹{inventory_value:,.2f}")

    st.divider()

    st.subheader("Low Stock Alerts")

    low_stock = [
        p for p in products if p["stock"] <= 10
    ]

    if low_stock:
        st.warning("Some products have low stock.")
        st.dataframe(pd.DataFrame(low_stock), use_container_width=True)
    else:
        st.success("All products have sufficient stock.")

    st.subheader("Product Overview")

    if products:
        st.dataframe(pd.DataFrame(products), use_container_width=True)

except requests.RequestException as error:
    st.error(f"Backend connection failed: {error}")