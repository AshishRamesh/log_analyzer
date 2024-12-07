import streamlit as st
import pandas as pd
import plotly.express as px
from langchain_community.llms import Ollama
from pandasai import SmartDataframe

# Page Config
st.set_page_config(
    page_title="LogIQ - Graphs",
    page_icon="📊",
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

st.title("Generate Graphs with LogIQ 🤖")
st.markdown("---")

# Initialize LLM
llm = Ollama(model="llama3.1")
st.subheader("Upload your log files to visualize insights!")

# Sidebar for Info
with st.sidebar:
    st.info("🔍 **How it works:**\n1. Upload your log file.\n2. Describe the graph you want.\n3. Let the bot generate insights.", icon="ℹ️")
    st.markdown("**Supported Formats:** `.csv`")

# Initialize content as None
content = None


# File Upload Section
uploaded_file = st.file_uploader("Upload your log file (CSV only)", type="csv")

if uploaded_file:
    # Display File Details
    st.success(f"Uploaded: {uploaded_file.name}")
    st.text(f"File size: {uploaded_file.size / 1024:.2f} KB")

    data = pd.read_csv(uploaded_file)
    st.write("File Preview:")
    st.dataframe(data.head())
    df = SmartDataframe(data, config={"llm": llm})
    st.markdown("---")
    # Prompt for Graph Description
    prompt = st.text_area("Describe the graph you want...", placeholder="e.g., Can you give me a graph of the number of times each IP address occurs?")

    if st.button("Generate Graph"):
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            with st.spinner("Generating graph..."):
                try:
                    # Use the LLM to process the prompt
                    response = df.chat(prompt)
                    with st.chat_message("ai"):
                        st.write("Graph generated successfully!")
                        st.write(response)
                    st.markdown("### Generated Graph")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a description for the graph.")
else:
    st.warning("Please upload a CSV file to begin analysis!")

# Footer
st.markdown("---")
st.text("🚀 Project by Ameen & Ashish.")
