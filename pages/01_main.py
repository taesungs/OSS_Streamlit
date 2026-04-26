import streamlit as st
from utils import init_state

st.set_page_config(page_title="MLB 선수 퀴즈", page_icon="⚾")

init_state()

st.markdown(
    """
    <style>
    .block-container {
        max-width: 520px;
        margin: 0 auto;
        padding-top: 3rem;
    }

    .main-title {
        text-align: center;
        font-size: 44px;
        font-weight: 800;
        white-space: nowrap;
        margin-bottom: 28px;
    }

    .student-info {
        text-align: center;
        font-size: 30px;
        font-weight: 800;
        margin-top: 36px;
        margin-bottom: 28px;
        line-height: 1.7;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">⚾ MLB 선수 맞히기 퀴즈 ⚾</div>',
    unsafe_allow_html=True
)

st.image("assets/main.png", use_container_width=True)

st.markdown(
    """
    <div class="student-info">
        학번: 2023204067<br>
        이름: 엄태성
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("로그인 하기", use_container_width=True):
    st.switch_page("pages/02_login.py")