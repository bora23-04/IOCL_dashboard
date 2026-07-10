import streamlit as st
import base64


def apply_theme():

    with open("assets/fonts/JosefinSans-Regular.ttf", "rb") as f:
        font = base64.b64encode(f.read()).decode()

    css = f"""
    <style>

    @font-face {{
        font-family: 'Josefin Sans';
        src: url(data:font/ttf;base64,{font}) format('truetype');
    }}

    /* Main App */
    .stApp {{
        font-family: 'Josefin Sans', sans-serif;
    }}

    /* Headings */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Josefin Sans', sans-serif !important;
    }}

    /* Paragraphs */
    p {{
        font-family: 'Josefin Sans', sans-serif !important;
    }}

    /* Labels */
    label {{
        font-family: 'Josefin Sans', sans-serif !important;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        font-family: 'Josefin Sans', sans-serif;
    }}

    section[data-testid="stSidebar"] label {{
        font-family: 'Josefin Sans', sans-serif !important;
    }}

    /* Buttons */
    button {{
        font-family: 'Josefin Sans', sans-serif !important;
    }}

    /* Metrics */
    [data-testid="stMetric"] {{
        font-family: 'Josefin Sans', sans-serif !important;
    }}

    /* DataFrames & Tables */
    table {{
        font-family: 'Josefin Sans', sans-serif !important;
    }}

    </style>
    """

    st.markdown(css, unsafe_allow_html=True)