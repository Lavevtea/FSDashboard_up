import streamlit as st

def show_sidebar_menu(df, uploaded):
    if "menu_sidebar" not in st.session_state:
        st.session_state.menu_sidebar = "WorkOrder Chart"
    st.sidebar.title("Sidebar Menu")
    if st.sidebar.button("WorkOrder Chart"):
        st.session_state.menu_sidebar = "WorkOrder Chart"
    if st.sidebar.button("Status Chart"):
        st.session_state.menu_sidebar = "Status Chart"
    if st.sidebar.button("SLA Summary"):
        st.session_state.menu_sidebar = "SLA Summary"
    if st.sidebar.button("Export SLA"):
        st.session_state.menu_sidebar = "Export SLA"
    if st.sidebar.button("Status Information"):
        st.session_state.menu_sidebar = "Status Information"
    # if st.sidebar.button("Data Comparation"):
    #     st.session_state.menu_sidebar = "Data Comparation"
    # if st.sidebar.button("Merge Files"):
    #     st.session_state.menu_sidebar = "Merge Files"
    # menu_sidebar= st.session_state.menu_sidebar
