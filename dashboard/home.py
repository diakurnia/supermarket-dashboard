import streamlit as st
import numpy as np

def app():
    # st.set_page_config(page_title="Supermarket Dashboard", 
    #                     page_icon=":bar_chart:", 
    #                     layout="wide")
    # st.title("Home")
    st.write("Welcom to Supermarket Analysist Dashboard")
    # st.set_page_config(page_title="Supermarket Dashboard", 
    #                     page_icon=":bar_chart:", 
    #                     layout="wide")
    st.markdown('Streamlit is **_really_ cool**.')
    st.header('This is a header')
    st.subheader("subheader")
    st.caption("this is caption")
    st.text("text")
    st.latex("\int a x^2 \, dx")