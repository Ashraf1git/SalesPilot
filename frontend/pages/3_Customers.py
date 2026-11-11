import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Customers | SalesPilot", layout="wide")

st.title("Customer Management")

st.subheader("Add New Customer")

with st.form("customer_form"):
    name = st.text_input("Customer Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    address = st.text_area("Address")

    submitted = st.form_submit_button("Add Customer")

    if submitted:
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address
        }

        try:
            response = requests.post(
                f"{API_URL}/customers/",
                json=data,
                timeout=5
            )
            response.raise_for_status()
            st.success("Customer added successfully.")
            st.rerun()
        except requests.RequestException as error:
            st.error(str(error))

st.divider()

st.subheader("Customer Directory")

try:
    response = requests.get(f"{API_URL}/customers/", timeout=5)
    response.raise_for_status()
    customers = response.json()

    if customers:
        st.dataframe(
            pd.DataFrame(customers),
            use_container_width=True
        )

        customer_ids = [c["id"] for c in customers]

        delete_id = st.selectbox(
            "Select Customer ID to Delete",
            customer_ids
        )

        if st.button("Delete Customer"):
            result = requests.delete(
                f"{API_URL}/customers/{delete_id}",
                timeout=5
            )
            result.raise_for_status()
            st.success("Customer deleted.")
            st.rerun()
    else:
        st.info("No customers registered yet.")

except requests.RequestException as error:
    st.error(f"Unable to connect: {error}")