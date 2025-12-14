# streamlit_app.py

import streamlit as st
import pandas as pd

# Week 8 database functions
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user
from app.data.incidents import get_all_incidents, insert_incident


# Connect to DB
conn = connect_database('DATA/intelligence_platform.db')

#SESSION STATE SETUP
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

#LOGIN PAGE
if not st.session_state.logged_in:
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        success, msg = login_user(username, password)
        st.info(msg)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            
    
    st.write("---")
    st.write("New user? Register below:")
    new_username = st.text_input("New Username", key="reg_user")
    new_password = st.text_input("New Password", type="password", key="reg_pass")
    role = st.selectbox("Role", ["user", "analyst"], key="reg_role")
    
    if st.button("Register"):
        success, msg = register_user(new_username, new_password, role)
        st.info(msg)
        if success:
            st.experimental_rerun()

#DASHBOARD PAGE
else:
    st.title(f"Data Science Incidents Dashboard - Welcome {st.session_state.username}")
    
    # Show all incidents
    incidents = get_all_incidents()
    st.dataframe(incidents, use_container_width=True)

    # Add new incident
    with st.form("new_incident"):
        title = st.text_input("Incident Title")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
        submitted = st.form_submit_button("Add Incident")
        
        if submitted and title:
            insert_incident(title, severity, status, st.session_state.username)
            st.success("Incident added successfully")
            

    st.write("---")
    
    # Logout button
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        

    # Sample metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accuracy", "94.2%")
    with col2:
        st.metric("Precision", "91.8%")
    with col3:
        st.metric("Recall", "89.5%")

    # Sample training history chart
    history = pd.DataFrame({
        "epoch": [1, 2, 3, 4, 5],
        "loss": [0.45, 0.32, 0.24, 0.18, 0.15],
        "accuracy": [0.78, 0.85, 0.89, 0.92, 0.94]
    })
    st.line_chart(history.set_index("epoch"))
