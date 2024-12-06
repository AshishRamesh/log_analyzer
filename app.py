from langchain_community.llms import Ollama
import streamlit as st

llm = Ollama(model= "llama3.1")
st.title("LogIQ")

prompt = st.text_area("Enter your prompt here")

if st.button("Generate"):
    with st.spinner("Generating..."):
        st.write_stream(llm.stream(prompt))