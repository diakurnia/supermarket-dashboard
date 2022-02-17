import visualization, hypothesis, home
import streamlit as st

PAGES = {
    'Visualization': visualization,
    'Hypotesis': hypothesis
}

st.set_page_config(page_title="Supermarket Dashboard", page_icon=":bar_chart:", layout="wide")
st.sidebar.title('Navigation')
select_page = st.sidebar.radio('Navigation', list(PAGES.keys())) 
page = PAGES[select_page]
st.sidebar.markdown('**Note**: if your streamlit default theme is dark, you can change to light for better experience when see this dashboard')
page.app()
# st.set_page_config(page_title="Covid-19 Dashboard", page_icon=":bar_chart:", layout="wide")