# app.py
import streamlit as st

# Try to import LangChain's SRT loader; show a friendly error if missing
try:
    from langchain_community.document_loaders import SRTLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_openai import ChatOpenAI
except Exception as e:
    st.error("Missing langchain or loader import error or openai or chroma. See README instructions.")
    st.stop()
    


st.set_page_config(page_title="RAG - SRT Loader Test")
st.title("SRT Loader — Quick Test")
rag_prompt = ""  # Initialize rag_prompt to avoid reference before assignment
# ---------- Sidebar: OpenAI API Key ----------
st.sidebar.header("OpenAI Configuration")
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")

st.write("Enter the path to a local .srt file. The app will attempt to load it using LangChain's SRTLoader.")

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore =  None


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
                splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                chunks = splitter.split_documents(docs)

                st.success("ok — chunks created successfully.")
                st.write(f"Total chunks: {len(chunks)}")
                st.caption(f"Chunk size: {500}, overlap: {50}")
                st.session_state.chunks = chunks
                # Optional: Show a preview of the first chunk
                if len(chunks) > 0 :
                    st.text(chunks[0].page_content[:1000])
            else:
                # some loaders return [] for empty / unreadable files
                st.warning("Loaded but no documents were returned (0 items). Check the file content.")
        except Exception as ex:
            st.error(f"Failed to load file: {ex}")
            # Extra helpful hint
            st.caption("Hints: ensure the path is correct, file is a valid .srt, and you have read permissions.")


# step 3 embeddings + vectorstore

if st.session_state.chunks is None:
    st.info("first load and run chunk above")
else: 
    if st.button("create embeddings + vectorstore"):
        try:
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vs = Chroma.from_documents(
                documents=st.session_state.chunks,
                embedding=embeddings
                )
            st.session_state.vectorstore = vs
            st.success("ok — vectorstore created successfully.")
            
        except Exception as ex:
            st.error(f"Failed to create embeddings/vectorstore: {ex}")



# step 4:  Test Retrieval ( similarity search / RAG context)
if st.session_state.vectorstore is None:
    st.info("first create embeddings + vectorstore above")
else:
    user_question = st.text_input("Enter a test question for retrieval:")
    
    if st.button("Retrieve Answer"):
        if not user_question:
            st.warning("Please enter a question first.")
        else:
            # get top 3 most similar chunks
            try:
                results = st.session_state.vectorstore.similarity_search(user_question, k=3)
                st.write(f"Retrieved {len(results)} results:")

                for i, doc in enumerate(results):
                    st.markdown(f"**chunk {i}:**")
                    st.text(doc.page_content[:1000])  # show first 1000 chars
                
                # build an rag prompt that user can copy to use with LLM
                if results:
                    combined_context = "\n\n".join([doc.page_content[:1000] for doc in results])
                    rag_prompt =  f"""Use only the context below to answer the question.
                    context:
                    {combined_context}
                    question: {user_question}
                    if the answer is not contained within the context, respond with 'I don't know.'"""
                    st.session_state.rag_prompt = rag_prompt
            except Exception as ex:
                st.error(f"Retrieval failed: {ex}")


# step 5 : Rag answer with LLM
st.subheader("Ask and Get answer with LLM + RAG")

if st.session_state.vectorstore is None:
    st.info("first create embeddings + vectorstore above")
else:
    if not openai_key:
        st.warning("Please enter your OpenAI API key in the sidebar")
    else:
        if(st.button("Get LLM Answer")):
            if not st.session_state.rag_prompt:
                st.warning("Please perform retrieval first to generate the RAG prompt.")
            else:                
                llm = ChatOpenAI(openai_api_key=openai_key,
                        model="gpt-4o-mini", temperature=0)
                with st.spinner("Generating answer..."):
                    response = llm.invoke(st.session_state.rag_prompt)
                    st.markdown("**LLM Response:**")
                    st.write(response.content)
   
        
