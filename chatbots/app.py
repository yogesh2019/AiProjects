import os
import streamlit as st
from datetime import datetime
import openai

#Page setup
st.set_page_config(
    page_title = "Eva - Banker Chatbot", page_icon = "😂"
)
st.title("Eva your banking assistant")

st.write("this is a banking chat bot app ")


# GEt api key from streamlit secrets or env
OPENAI_API_KEY = None

try:
    OPENAI_API_KEY = st.secrets.get("OPEN_API_KEY")
except Exception:
    OPENAI_API_KEY = None

if not OPENAI_API_KEY:
    st.warning("No open api key found")
    st.stop()

