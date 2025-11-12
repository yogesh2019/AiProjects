import streamlit as st
from langchain_openai import ChatOpenAI

# --- Page Setup ---
st.set_page_config(page_title="Chatbot Interface", page_icon="🤖", layout="wide")
st.title("Chatbot Interface  🤖")

# --- sidebar ---
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("OpenAi API key", type="password")

if not api_key:
    st.warning("Please enter you OpenAi API key in the sidebar")
    st.stop()


# --- initialize LLM ---
llm  = ChatOpenAI(
    api_key= api_key,
    model="gpt-4o-mini",
    temperature=0.3
)

user_prompt = st.text_input("Enter a simple Question for the chatbot:")
if(st.button("Get Answer")):
    if user_prompt:
        with st.spinner("Generating response..."):
            response = llm.invoke(user_prompt)
        st.markdown("### Response:")
        st.write(response.text)
    else:
        st.warning("Please enter a question to get an answer.")