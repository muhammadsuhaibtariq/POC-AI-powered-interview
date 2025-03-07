import streamlit as st
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def add_logo():
    img_base64 = get_base64_image("frontend/assets/mobizlogo.png")
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url("data:image/png;base64,{img_base64}");
                background-repeat: no-repeat;
                padding-top: 140px;
                background-position: 20px 20px;
                background-size: 200px auto;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
