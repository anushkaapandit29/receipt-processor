import streamlit as st
import pandas as pd
from PIL import Image
import os
import database
from database import create_connection, delete_expense_by_id, clear_all_receipts

# Initialize DB on start
database.init_db()

st.set_page_config(page_title="Smart Receipt Processor", page_icon="🧾", layout="wide")

st.title("🧾 Smart Receipt & Invoice Processor")
st.subheader("Automated Expense & Invoice Management System")

# Sidebar for API Key
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# Tabs for Upload vs Dashboard
tab1, tab2 = st.tabs(["📤 Upload & Process", "📊 Expense Dashboard"])

with tab1:
    st.write("Upload a clear receipt image (PNG, JPG, JPEG) to automatically parse its contents.")
    
    uploaded_file = st.file_uploader("Choose a receipt image...", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Receipt", use_container_width=True)
            
            temp_path = "temp_receipt.png"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        with col2:
            st.info("Click the button below to extract details using Cloud AI.")
            
            if st.button("🚀 Process Receipt"):
                if not api_key:
                    st.error("Please enter your Gemini API Key in the sidebar!")
                else:
                    # Import ai_processor dynamically inside button click to prevent startup lags
                    import ai_processor
                    with st.spinner("Analyzing receipt with Cloud AI..."):
                        extracted_data = ai_processor.extract_receipt_details(temp_path, api_key)

                        if extracted_data:
                            st.success("Extraction Complete!")
                            st.json(extracted_data)

                            database.save_receipt(
                                vendor=extracted_data.get("vendor", "Unknown"),
                                date=extracted_data.get("date", "N/A"),
                                total_amount=float(extracted_data.get("total_amount", 0.0)),
                                tax=float(extracted_data.get("tax", 0.0)),
                                items=str(extracted_data.get("items", ""))
                            )
                            st.success("Saved to database successfully!")
                        else:
                            st.error("Failed to parse receipt data.")

with tab2:
    st.header("Saved Receipts & Data Analytics")
    records = database.fetch_all_receipts()

    if records:
        df = pd.DataFrame(records, columns=["ID", "Vendor", "Date", "Total Amount", "Tax", "Items"])
        
        # Display Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Invoices Processed", len(df))
        col2.metric("Total Spent", f"₹{df['Total Amount'].sum():,.2f}")
        col3.metric("Total Tax Paid", f"₹{df['Tax'].sum():,.2f}")

        st.divider()

        # Display Data Table
        st.subheader("All Transaction Records")
        st.dataframe(df, use_container_width=True)

        # Actions Row: Delete specific row or clear all
        col_action1, col_action2 = st.columns(2)
        
        with col_action1:
            delete_id = st.selectbox("Select Record ID to Delete", options=[None] + list(df['ID']))
            if delete_id is not None:
                if st.button("🗑️ Delete Selected Record"):
                    delete_expense_by_id(delete_id)
                    st.success(f"Record ID {delete_id} deleted successfully!")
                    st.rerun()

        with col_action2:
            st.write("")
            st.write("")
            if st.button("⚠️ Clear All Records"):
                clear_all_receipts()
                st.success("All records cleared!")
                st.rerun()

        st.divider()

        # Download CSV Option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Data as CSV",
            data=csv,
            file_name="receipt_expenses.csv",
            mime="text/csv"
        )
    else:
        st.info("No records found. Upload a receipt in the first tab to populate data!")
