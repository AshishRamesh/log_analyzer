import streamlit as st
import pandas as pd
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.docstore.document import Document
from sentence_transformers import SentenceTransformer
from langchain_community.llms import Ollama
import benchmark as benchmark

# Page Config
local_llm = Ollama(model="llama3.1")
st.set_page_config(
    page_title="LogIQ",
    page_icon="📝",
    layout="centered"
)

# Inject custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #000000;  /* Black */
        color: #39FF14;  /* Neon green */
    }
    .stButton > button {
        background-color: #39FF14;
        color: #000000;
        border-radius: 5px;
    }
    .stTextInput > div > div > input {
        background-color: #1A1A1A;
        color: #39FF14;
        border: 1px solid #39FF14;
    }
    .stMarkdown, .stDataFrame {
        color: #39FF14;
    }
    textarea:focus {
        background-color: #1A1A1A;  /* Dark background */
        color: #39FF14;  /* Neon green text */
        border: none;  /* Remove border */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Chat with the LogIQ 🤖")
st.markdown("---")

# Sidebar for Info
with st.sidebar:
    st.info("🔍 **How it works:**\n1. Upload your log file.\n2. Let the bot analyze.\n3. Chat for detailed insights.", icon="ℹ️")
    st.markdown("**Supported Formats:** `.txt`, `.log`, `.csv`")
    st.markdown("---")
    st.text("🚀 Project by Ameen & Ashish.")

# Custom embedding class for SentenceTransformer
class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name="all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts):
        """Embed a list of documents."""
        return self.model.encode(texts, convert_to_numpy=True)
    
    def embed_query(self, text):
        """Embed a single query."""
        return self.model.encode([text], convert_to_numpy=True)[0]

# Initialize custom embeddings
sentence_embeddings = SentenceTransformerEmbeddings()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "retriever" not in st.session_state:
    st.session_state["retriever"] = None

# File Upload Section
uploaded_file = st.file_uploader("Upload your log file", type=["txt", "log", "csv"])

if uploaded_file:
    # Display File Details
    st.success(f"Uploaded: {uploaded_file.name}")
    st.text(f"File size: {uploaded_file.size / 1024:.2f} KB")
    file_extension = uploaded_file.name.split('.')[-1]

    with st.expander("File Preview", expanded=True):
        # Read and Display File Content
        if file_extension in ["txt", "log"]:
            content = uploaded_file.read().decode("utf-8")
            st.text_area("File Preview", content[:500], height=200)
        elif file_extension == "csv":
            data = pd.read_csv(uploaded_file)
            st.write("File Preview:")
            st.dataframe(data.head())
            content = data.to_string(index=False)

    # Process file for RAG
    with st.spinner("Processing file for retrieval..."):
        if file_extension in ["txt", "log"]:
                        text_splitter = CharacterTextSplitter(separator = ",",chunk_size=1000,chunk_overlap=200)

        else:
            text_splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        docs = text_splitter.split_text(content)
        documents = [Document(page_content=doc) for doc in docs]

        # Create FAISS vectorstore
        vectorstore = FAISS.from_documents(documents, sentence_embeddings)
        st.session_state["retriever"] = vectorstore.as_retriever()

    st.success("File successfully processed for retrieval!")
    st.markdown("---")

# Chatbot Section
if st.session_state["retriever"]:
    retriever_chain = ConversationalRetrievalChain.from_llm(
        llm=local_llm,
        retriever=st.session_state["retriever"],
        return_source_documents=True
    )

    # Display chat history in Streamlit UI
    for chat in st.session_state["chat_history"]:
        with st.chat_message(chat["role"]):
            st.write(chat["message"])

    # Input for the current user prompt
    if prompt := st.chat_input("Enter your prompt..."):
        # Append user message to session state
        st.session_state["chat_history"].append({"role": "user", "message": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            # benchmark.proc_util()
            benchmark.time_init()

        # Transform chat history to tuples
        chat_history_for_chain = [(msg["role"], msg["message"]) for msg in st.session_state["chat_history"]]

        # Generate response
        with st.spinner("Generating response..."):
            try:
                # Pass transformed chat history
                response = retriever_chain({"question": prompt, "chat_history": chat_history_for_chain})

                # Extract and display the answer
                answer = response.get("answer", "No answer generated.")
                st.session_state["chat_history"].append({"role": "assistant", "message": answer})
                with st.chat_message("assistant"):
                    st.write(answer)
                    benchmark.latency()
                    # benchmark.proc_util()

                # Display source documents (optional)
                # if "source_documents" in response:
                #     with st.expander("Source Documents"):
                #         for doc in response["source_documents"]:
                #             st.markdown(f"**Source:**\n\n{doc.page_content}")

            except Exception as e:
                error_message = f"An error occurred: {e}"
                st.session_state["chat_history"].append({"role": "assistant", "message": error_message})
                with st.chat_message("assistant"):
                    st.write(error_message)





# Footer
st.markdown("---")
