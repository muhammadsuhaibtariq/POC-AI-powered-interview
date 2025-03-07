import streamlit as st
import requests
import os
import re
from utils.display_logo import add_logo

# Read FASTAPI URL from environment variable with a default fallback
FASTAPI_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

# Page Configuration
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# Display Logo and Title
add_logo()
st.markdown("<h1 style='text-align: center;'>🔑 Login to AI-Powered Interview</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Function to Validate Email
def is_valid_email(email):
    """Validates an email format using regex."""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None

# Function to Handle Login
def login():
    """Handles user login by calling FastAPI and updating the UI."""
    if not st.session_state.name or not st.session_state.email:
        st.error("⚠ **Please enter both name and email.**")
        return  

    if not is_valid_email(st.session_state.email):
        st.error("❌ **Invalid email format!** Please enter a valid email (e.g., user@example.com).")
        return  

    # Call FastAPI backend to save user
    url = f"{FASTAPI_URL}/save-user/"
    payload = {"name": st.session_state.name, "email": st.session_state.email}
    
    try:
        response = requests.post(url, json=payload, timeout=10)  # Set timeout to avoid hanging

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("message") == "User already exists":
                st.success(f"👋 **Welcome back, {st.session_state.name}!** Redirecting to assessment... ⏳")
            else:
                st.success(f"✅ **Successfully logged in as {st.session_state.name} ({st.session_state.email})!**")

            # Store session state
            st.session_state["user_email"] = st.session_state.email
            st.session_state["user_name"] = st.session_state.name

            # Redirect to the assessment page after a short delay
            st.switch_page("pages/1_Assessment.py")

        else:
            # Display Backend Validation Errors in a Proper Box
            error_details = response.json().get("detail", "⚠ Failed to log in. Please try again.")

            # Check if error details are in list format (e.g., validation errors)
            if isinstance(error_details, list):
                formatted_errors = "\n".join([f"❌ {err.get('msg', 'Unknown error')}" for err in error_details])
                st.error(f"⚠ **Login Failed!**\n\n{formatted_errors}")
            else:
                st.error(f"⚠ **Login Failed!**\n\n{error_details}")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ **Login failed:** {e}")

# Layout for Centered Input Fields
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.text_input("👤 Enter your name:", key="name", placeholder="John Doe")
    st.text_input("📧 Enter your email address:", key="email", placeholder="john@example.com")

# Centered Login Button with Spacing
st.markdown("<br>", unsafe_allow_html=True)
col4, col5, col6 = st.columns([1, 2, 1])

with col5:
    if st.button("🚀 Login & Start Assessment", use_container_width=True):
        login()
