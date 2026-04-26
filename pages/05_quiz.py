import streamlit as st
from utils import init_state

st.set_page_config(page_title="퀴즈", page_icon="⚾")

init_state()

if not st.session_state.is_login:
    st.warning("로그인이 필요합니다.")
    st.switch_page("pages/02_login.py")

if not st.session_state.quiz_players:
    st.warning("퀴즈가 시작되지 않았습니다.")
    st.switch_page("pages/04_level.py")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 760px;
        margin: 0 auto;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    .quiz-card {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        text-align: center;
        margin-top: 12px;
        margin-bottom: 14px;
    }

    .quiz-title {
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .quiz-sub {
        color: #9ca3af;
        font-size: 15px;
        margin-bottom: 0;
    }

    .quiz-image-box {
        display: flex;
        justify-content: center;
        margin-bottom: 12px;
    }

    .quiz-image {
        width: 100%;
        max-width: 330px;
        height: 260px;
        object-fit: cover;
        object-position: top center;
        border-radius: 14px;
    }

    div[data-testid="stRadio"] {
        margin-top: -4px;
    }

    div[data-testid="stRadio"] > label {
        font-size: 18px !important;
        font-weight: 700 !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label {
        font-size: 17px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

index = st.session_state.current_index
player = st.session_state.quiz_players[index]
options = st.session_state.quiz_options[index]
answered_count = len(st.session_state.answers)

st.progress((index + 1) / 5)
st.write(f"현재 진행: {answered_count}/5 문제 완료")

st.markdown(
    f"""
    <div class="quiz-card">
        <div class="quiz-title">{index + 1}번 문제 / 5문제</div>
        <div class="quiz-sub">사진을 보고 MLB 선수의 이름을 선택하세요.</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="quiz-image-box">
        <img class="quiz-image" src="{player["image"]}">
    </div>
    """,
    unsafe_allow_html=True
)

previous_answer = st.session_state.answers.get(index)

selected_answer = st.radio(
    "이 선수의 이름은?",
    options,
    index=options.index(previous_answer) if previous_answer in options else None,
    key=f"answer_{index}"
)

if selected_answer is not None:
    st.session_state.answers[index] = selected_answer

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("이전", disabled=index == 0, use_container_width=True):
        st.session_state.current_index -= 1
        st.rerun()

with col2:
    if st.button("다음", disabled=index == 4, use_container_width=True):
        st.session_state.current_index += 1
        st.rerun()

with col3:
    if st.button("제출하기", use_container_width=True):
        if len(st.session_state.answers) < 5:
            st.warning("아직 풀지 않은 문제가 있습니다.")
        else:
            st.switch_page("pages/06_result.py")