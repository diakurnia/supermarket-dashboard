import visualization, hypothesis, home
import streamlit as st

# st.set_page_config(page_title="Supermarket Dashboard", 
#                     page_icon=":bar_chart:", 
#                     layout="wide")
PAGES = {
    'Home':home,
    'Visualization': visualization,
    'Hypotesis': hypothesis
}
# st.set_page_config(page_title="Supermarket Dashboard", 
#                         page_icon=":bar_chart:", 
#                         layout="wide")
st.sidebar.title('Navigation')
select_page = st.sidebar.selectbox('Navigation', list(PAGES.keys()))
page = PAGES[select_page]
page.app(
    # st.set_page_config(page_title="Supermarket Dashboard", 
    #                 page_icon=":bar_chart:", 
    #                 layout="wide")
)