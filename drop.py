import streamlit as st
import pandas as pd
from datetime import datetime

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

st.subheader("Upload your log files and get insights!")

# Sidebar for Info
with st.sidebar:
    st.info("🔍 **How it works:**\n1. Upload your log file.\n2. Let the bot analyze.\n3. Chat for detailed insights.", icon="ℹ️")
    st.markdown("**Supported Formats:** `.txt`, `.log`, `.csv`")

# File Upload Section
uploaded_file = st.file_uploader("Upload your log file", type=["txt", "log", "csv"])

if uploaded_file:
    # Display File Details
    st.success(f"Uploaded: {uploaded_file.name}")
    st.text(f"File size: {uploaded_file.size / 1024:.2f} KB")
    file_extension = uploaded_file.name.split('.')[-1]

    # File Preview
    if file_extension in ["txt", "log"]:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("File Preview", content[:500], height=200)
    elif file_extension == "csv":
        data = pd.read_csv(uploaded_file)
        st.write("File Preview:")
        st.dataframe(data.head())

    # Analysis Section
    st.markdown("---")
    st.header("Analysis Results")
    st.info("⚡ Analyzing your logs, please wait...")

    # Simulate Log Analysis (Dummy Output for Now)
    insights = [
        "Found 5 login anomalies.",
        "Detected 2 potential network intrusions.",
        "Server error spike detected at 2023-10-28 14:45:00.",
    ]
    for insight in insights:
        st.write(f"• {insight}")

    # Chatbot Section
    st.markdown("---")
    st.header("Chat with the Log Analyzer Bot 🤖")
    user_input = st.text_input("Type your query here...", placeholder="e.g., What caused the spike in server errors?")
    if user_input:
        # Dummy response
        response = "This looks like a result of high traffic combined with misconfigured server settings. Would you like suggestions on fixing it?"
        st.text_area("Chatbot Reply", response, height=100, disabled=True)

else:
    st.warning("Please upload a file to begin analysis!")

# Footer
st.markdown("---")
st.caption("🚀 Project by Ameen & Ashish.")
