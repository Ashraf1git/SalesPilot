import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Analytics | SalesPilot", layout="wide")

st.title("Business Analytics")

try:
    response = requests.get(
        f"{API_URL}/dashboard/summary",
        timeout=5
    )
    response.raise_for_status()
    summary = response.json()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"₹{summary['total_revenue']:,.2f}")
    col2.metric("Total Sales", summary["total_sales"])
    col3.metric("Units Sold", summary["total_units_sold"])

    col4, col5, col6 = st.columns(3)

    col4.metric("Total Products", summary["total_products"])
    col5.metric("Available Stock", summary["total_stock"])
    col6.metric("Inventory Value", f"₹{summary['inventory_value']:,.2f}")

    st.divider()

    st.subheader("Top-Selling Products")

    top_response = requests.get(
        f"{API_URL}/dashboard/top-products",
        timeout=5
    )
    top_response.raise_for_status()

    top_products = top_response.json()

    if top_products:
        df = pd.DataFrame(top_products)

        st.bar_chart(
            df.set_index("product")["quantity_sold"]
        )

        st.dataframe(df, use_container_width=True)
    else:
        st.info("No sales data available yet.")

except requests.RequestException as error:
    st.error(f"Unable to load analytics: {error}")