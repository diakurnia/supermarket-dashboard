import visualization, hypothesis, home
import streamlit as st

PAGES = {
    'Visualization': visualization,
    'Hypotesis': hypothesis
}

st.set_page_config(page_title="Covid-19 Dashboard", page_icon=":bar_chart:", layout="wide")
st.sidebar.title('Navigation')
select_page = st.sidebar.radio('Navigation', list(PAGES.keys())) 
page = PAGES[select_page]
page.app()
# st.set_page_config(page_title="Covid-19 Dashboard", page_icon=":bar_chart:", layout="wide")