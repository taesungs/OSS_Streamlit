import streamlit as st

st.set_page_config(page_title="MLB 선수 퀴즈", page_icon="⚾")

if "is_login" not in st.session_state:
    st.session_state.is_login = False

st.switch_page("pages/01_main.py")