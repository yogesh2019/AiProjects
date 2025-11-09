import os
import streamlit as st

from langchain_openai import ChatOpenAI
from langchian.schema import SystemMessage, HumanMessage, AIMessage

#Page setup
st.set_page_config(
    page_title = "Eva - Banker Chatbot", page_icon = "😂"
)
st.title("Eva your banking assistant")

st.write("This is a minimal streamlit app   ")

if(st.button("Say hi")):
    st.success("Working success")