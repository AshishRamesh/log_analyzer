import streamlit as st
import pandas as pd
from langchain_community.llms import Ollama

# Page Config
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
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Chat with the LogIQ 🤖")
st.markdown("---")

# Initialize LLM
llm = Ollama(model="llama3.1")
st.subheader("Upload your log files and get insights!")

# Sidebar for Info
with st.sidebar:
    st.info("🔍 **How it works:**\n1. Upload your log file.\n2. Let the bot analyze.\n3. Chat for detailed insights.", icon="ℹ️")
    st.markdown("**Supported Formats:** `.txt`, `.log`, `.csv`")
    st.markdown("---")
    st.text("🚀 Project by Ameen & Ashish.")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "content" not in st.session_state:
    st.session_state["content"] = None

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
            st.session_state["content"] = uploaded_file.read().decode("utf-8")
            st.text_area("File Preview", st.session_state["content"][:500], height=200)
        elif file_extension == "csv":
            data = pd.read_csv(uploaded_file)
            st.write("File Preview:")
            st.dataframe(data.head())
            # Convert CSV data to string format for LLM
            st.session_state["content"] = data.to_string(index=False)
    st.markdown("---")

# Chatbot Section
if st.session_state["content"]:
    # Display chat history
    for chat in st.session_state["chat_history"]:
        with st.chat_message(chat["role"]):
            st.write(chat["message"])

    # Input for the current user prompt
    if prompt := st.chat_input("Enter your prompt..."):
        # Append user message to chat history
        st.session_state["chat_history"].append({"role": "user", "message": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate response
        with st.spinner("Generating response..."):
            try:
                response = llm.stream(f"Analyze the following log data and answer the query: {prompt}\n\nLog Data:\n{st.session_state['content']}")
                st.session_state["chat_history"].append({"role": "ai", "message": response})
                with st.chat_message("ai"):
                    st.write(response)
            except Exception as e:
                error_message = f"An error occurred: {e}"
                st.session_state["chat_history"].append({"role": "ai", "message": error_message})
                with st.chat_message("ai"):
                    st.write(error_message)

# Footer
st.markdown("---")
