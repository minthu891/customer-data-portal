import streamlit as st
import pandas as pd
from openpyxl import load_workbook

# Path to the Excel file
excel_path = "20250719_172622.xlsx"

st.title("Customer Data Entry Portal")

# Form for customer data input
with st.form("customer_form"):
    customer_id = st.text_input("Customer ID")
    full_name = st.text_input("Full Name")
    nrc_number = st.text_input("NRC Number")
    dob = st.date_input("Date of Birth")
    created_date = st.date_input("Created Date")
    submitted = st.form_submit_button("Submit")

    if submitted:
        # Prepare data for 'compliance ' sheet
        compliance_data = {
            "Case ID": customer_id,
            "Registered Date": created_date.strftime("%Y-%m-%d"),
            "Full Name": full_name,
            "DOB": dob.strftime("%Y-%m-%d"),
            "NRC": nrc_number,
            "Request Date": created_date.strftime("%Y-%m-%d")
        }

        # Prepare data for 'customer data' sheet
        customer_data = {
            "ID": customer_id,
            "First Name": full_name,
            "Date of Birth": dob.strftime("%Y-%m-%d"),
            "KYC Identity ID": nrc_number,
            "Ticket Requested Date": created_date.strftime("%Y-%m-%d")
        }

        # Load existing data
        compliance_df = pd.read_excel(excel_path, sheet_name="compliance ", engine="openpyxl")
        customer_df = pd.read_excel(excel_path, sheet_name="customer data", engine="openpyxl")

        # Append new data
        compliance_df = pd.concat([compliance_df, pd.DataFrame([compliance_data])], ignore_index=True)
        customer_df = pd.concat([customer_df, pd.DataFrame([customer_data])], ignore_index=True)

        # Save back to Excel
        with pd.ExcelWriter(excel_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            compliance_df.to_excel(writer, sheet_name="compliance ", index=False)
            customer_df.to_excel(writer, sheet_name="customer data", index=False)

        st.success("Customer data successfully added to both sheets.")
