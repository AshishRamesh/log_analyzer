import streamlit as st

def page_2():
    st.title("LogIQ")

pg = st.navigation([st.Page(page_2), st.Page("chat.py"), st.Page("graph.py")])
pg.run()