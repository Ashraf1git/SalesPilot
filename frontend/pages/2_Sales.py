import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Sales | SalesPilot", layout="wide")

st.title("Sales Management")

# Get products
try:
    response = requests.get(f"{API_URL}/products/?limit=100")
    response.raise_for_status()
    products = response.json()["products"]
except requests.RequestException:
    st.error("Backend is not running.")
    st.stop()

if not products:
    st.warning("Add products before recording sales.")
    st.stop()

st.subheader("Record a New Sale")

with st.form("sales_form"):
    product_options = {
        f'{p["name"]} (Stock: {p["stock"]})': p
        for p in products
        if p["stock"] > 0
    }

    if not product_options:
        st.warning("No products are currently in stock.")
        st.stop()

    selected_name = st.selectbox(
        "Select Product",
        list(product_options.keys())
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=int(product_options[selected_name]["stock"]),
        step=1
    )

    customer = st.text_input("Customer Name")
    submitted = st.form_submit_button("Record Sale")

    if submitted:
        product = product_options[selected_name]

        sale_data = {
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": product["price"],
            "total": quantity * product["price"],
            "customer": customer,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            result = requests.post(
                f"{API_URL}/sales/",
                json=sale_data,
                timeout=5
            )
            result.raise_for_status()
            st.success("Sale recorded successfully.")
            st.rerun()
        except requests.RequestException as error:
            st.error(f"Unable to record sale: {error}")

st.divider()

st.subheader("Sales History")

try:
    response = requests.get(f"{API_URL}/sales/", timeout=5)
    response.raise_for_status()
    sales = response.json()

    if sales:
        st.dataframe(sales, use_container_width=True)
    else:
        st.info("No sales recorded yet.")

except requests.RequestException:
    st.error("Unable to retrieve sales history.")