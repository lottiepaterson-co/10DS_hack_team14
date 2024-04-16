import streamlit as st
from dotenv import load_dotenv

st.session_state["output"] = "N/A"

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)