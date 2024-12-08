import streamlit as st

def home():
    # Page title and description
    st.markdown("""
    <style>
    .header {
        text-align: center;
        color: #39FF14;
        font-size: 3rem;
        font-weight: bold;
        padding-top: 0px;
    }
    .subheader {
        text-align: center;
        color: #fff;
        font-size: 1.5rem;
        margin-top: 0px;
        padding-bottom: 10px;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding-top: 20px;
    }
    .stImage {
        max-width: 100%;
        margin-top: 20px;
        border-radius: 8px;
    }
    .footer {
        text-align: center;
        font-size: 1rem;
        color: #39FF14;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Full-width background image (optional)
    st.markdown("""
    <div style="background-image: url('D:\Ameen\Internship\log_analyzer\bg_image.jpg'); background-size: cover; height: 240px; padding: 20px 0;">
        <h1 class="header">Welcome to LogIQ 🤖</h1>
        <p class="subheader">AI-powered log analysis tool for real-time insights and risk detection.</p>
    </div>
    """, unsafe_allow_html=True)

    # Description Section
    st.markdown("""
    **LogIQ** is an AI tool that helps you analyze your network logs, detect risks, and provide actionable insights based on real-time data. Whether you're an IT professional or a network administrator, LogIQ simplifies the task of log analysis and helps you troubleshoot faster.

    **Key Features:**
    - Real-time log analysis using advanced AI algorithms.
    - Chat-based interface to interact with the system for detailed insights.
    - Support for common log file formats like `.txt`, `.log`, and `.csv`.

    With **LogIQ**, stay ahead of potential issues and optimize your system performance without the hassle of manual log analysis.
    """)

    # Display a couple of images (for demo purposes, replace with actual project images)
    st.image("D:\Ameen\Internship\log_analyzer\log_file.png", caption="Sample Logs", use_container_width=True)
    # Footer with project information
    st.markdown("""
    <div class="footer">
        🚀 Project by Ameen & Ashish | Powered by Streamlit & AI
    </div>
    """, unsafe_allow_html=True)

# Navigation Setup
pg = st.navigation([st.Page(home), st.Page("chat.py"), st.Page("graph.py")])
pg.run()
