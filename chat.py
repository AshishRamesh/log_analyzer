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

# Initialize content as None
content = None

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
            # Convert CSV data to string format for LLM
            content = data.to_string(index=False)
    st.markdown("---")
    # Chatbot Section
    prompt = st.text_area("Enter your prompt here...", placeholder="e.g., What caused the spike in server errors?")

    # Check if both content and prompt are valid
    if st.button("Generate Response"):
        if content and prompt:
            with st.chat_message("user"):
                    st.write(prompt)
            with st.spinner("Generating response..."):
                try:
                    # Use the LLM to stream the response
                    response = llm.stream(f"Analyze the following log data and answer the query: {prompt}\n\nLog Data:\n{content}")
                    with st.chat_message("ai"):
                        st.write(response)
                    print(response)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload a valid file and enter a query.")
    else:
        if not uploaded_file:
            st.warning("Please upload a file to begin analysis!")

# Footer
st.markdown("---")
st.text("🚀 Project by Ameen & Ashish.")