import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# App Title
st.set_page_config(page_title="Athletix Fitness Manager", layout="wide")
st.title("🏋️ Athletix Fitness - Member Management System")

# Sidebar for adding new members
st.sidebar.header("Add New Member")
with st.sidebar.form("member_form"):
    name = st.text_input("Member Name")
    contact = st.text_input("Contact Number")
    plan = st.selectbox("Select Plan", ["Monthly", "Quarterly", "Yearly"])
    joining_date = st.date_input("Joining Date", datetime.now())
    
    # Logic for Expiry Date
    if plan == "Monthly":
        expiry = joining_date + timedelta(days=30)
    elif plan == "Quarterly":
        expiry = joining_date + timedelta(days=90)
    else:
        expiry = joining_date + timedelta(days=365)
        
    submitted = st.form_submit_button("Save Member")

# Database (For demo purposes, we use a session state)
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Name", "Contact", "Plan", "Joining Date", "Expiry Date", "Status"])

if submitted:
    new_data = {
        "Name": name, 
        "Contact": contact, 
        "Plan": plan, 
        "Joining Date": joining_date, 
        "Expiry Date": expiry,
        "Status": "Active"
    }
    st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
    st.success(f"Member {name} added successfully!")

# Dashboard Views
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Members")
    st.write(len(st.session_state.db))

with col2:
    st.subheader("Active Subscriptions")
    st.write(len(st.session_state.db[st.session_state.db['Status'] == "Active"]))

# Display Member Table
st.subheader("Member Records")
st.dataframe(st.session_state.db, use_container_width=True)

# Export Feature
if not st.session_state.db.empty:
    csv = st.session_state.db.to_csv(index=False).encode('utf-8')
    st.download_button("Download Report (CSV)", data=csv, file_name="athletix_members.csv", mime="text/csv")