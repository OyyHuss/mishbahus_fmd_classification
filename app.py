import streamlit as st

st.set_page_config(
    page_title="PMK Detection System",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Redirect otomatis ke beranda
st.switch_page("pages/beranda.py")