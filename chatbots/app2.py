# app.py
import streamlit as st

# Try to import LangChain's SRT loader; show a friendly error if missing
try:
    from langchain_community.document_loaders import SRTLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except Exception as e:
    st.error("Missing langchain or loader import error. See README instructions.")
    st.stop()
    
st.set_page_config(page_title="RAG - SRT Loader Test")
st.title("SRT Loader — Quick Test")

st.write("Enter the path to a local .srt file. The app will attempt to load it using LangChain's SRTLoader.")

srt_path = "chatbots/sample.srt"  

if st.button("Load SRT"):
    if not srt_path:
        st.warning("Please provide a file path first.")
    else:
        try:
            loader = SRTLoader(srt_path)
            docs = loader.load()  # returns list of Document objects
            count = len(docs) if docs is not None else 0
            if count > 0:
                st.success("ok — file loaded successfully.")
                st.write(f"Documents loaded: {count}")
                # optionally show small preview
                if st.checkbox("Show preview of first document text"):
                    st.text(docs[0].page_content[:1000])
            else:
                # some loaders return [] for empty / unreadable files
                st.warning("Loaded but no documents were returned (0 items). Check the file content.")
        except Exception as ex:
            st.error(f"Failed to load file: {ex}")
            # Extra helpful hint
            st.caption("Hints: ensure the path is correct, file is a valid .srt, and you have read permissions.")
