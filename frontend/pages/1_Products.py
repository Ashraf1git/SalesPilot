import streamlit as st
import pandas as pd
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Products", layout="wide")
st.title("Product Management")

search = st.text_input("Search products")
category = st.text_input("Filter by category")

try:
    response = requests.get(
        f"{API}/products/",
        params={"search": search, "category": category},
        timeout=5
    )
    response.raise_for_status()
    products = response.json()["products"]

    st.subheader("Product List")
    st.dataframe(pd.DataFrame(products), use_container_width=True)

except requests.RequestException as e:
    st.error(str(e))
    st.stop()

st.divider()
st.subheader("Add Product")

with st.form("add_product"):
    name = st.text_input("Product name")
    cat = st.text_input("Category")
    price = st.number_input("Price", min_value=0.01, value=100.0)
    stock = st.number_input("Stock", min_value=0, step=1)
    description = st.text_area("Description")

    if st.form_submit_button("Add Product"):
        if not name.strip() or not cat.strip():
            st.error("Name and category are required.")
        else:
            try:
                r = requests.post(
                    f"{API}/products/",
                    json={
                        "name": name,
                        "category": cat,
                        "price": price,
                        "stock": stock,
                        "description": description
                    },
                    timeout=5
                )
                r.raise_for_status()
                st.success("Product added.")
                st.rerun()
            except requests.RequestException as e:
                st.error(str(e))

st.divider()
st.subheader("Update or Delete Product")

all_response = requests.get(f"{API}/products/", timeout=5)
all_response.raise_for_status()
all_products = all_response.json()["products"]

if all_products:
    selected = st.selectbox(
        "Select product",
        all_products,
        format_func=lambda p: f'{p["id"]} - {p["name"]}'
    )

    with st.form("update_product"):
        new_name = st.text_input("Name", selected["name"])
        new_category = st.text_input("Category", selected["category"])
        new_price = st.number_input(
            "Price", min_value=0.01,
            value=float(selected["price"])
        )
        new_stock = st.number_input(
            "Stock", min_value=0,
            value=int(selected["stock"])
        )
        new_description = st.text_area(
            "Description", selected["description"]
        )

        if st.form_submit_button("Update Product"):
            try:
                r = requests.put(
                    f'{API}/products/{selected["id"]}',
                    json={
                        "name": new_name,
                        "category": new_category,
                        "price": new_price,
                        "stock": new_stock,
                        "description": new_description
                    },
                    timeout=5
                )
                r.raise_for_status()
                st.success("Product updated.")
                st.rerun()
            except requests.RequestException as e:
                st.error(str(e))

    if st.button("Delete Selected Product"):
        try:
            r = requests.delete(
                f'{API}/products/{selected["id"]}',
                timeout=5
            )
            r.raise_for_status()
            st.success("Product deleted.")
            st.rerun()
        except requests.RequestException as e:
            st.error(str(e))