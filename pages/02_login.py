import streamlit as st
from utils import init_state

st.set_page_config(page_title="로그인", page_icon="⚾")

init_state()

left, center, right = st.columns([1, 2, 1])

with center:
    st.title("로그인")

    user_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인", use_container_width=True):
        if user_id == "mlb" and password == "1234":
            st.session_state.is_login = True
            st.switch_page("pages/03_survey.py")
        else:
            st.error("아이디 또는 비밀번호가 틀렸습니다.")

    if st.button("첫 화면으로 돌아가기", use_container_width=True):
        st.switch_page("pages/01_main.py")