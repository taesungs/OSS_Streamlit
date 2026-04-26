import streamlit as st
from utils import init_state, start_quiz

st.set_page_config(page_title="난이도 선택", page_icon="⚾")

init_state()

if not st.session_state.is_login:
    st.warning("로그인이 필요합니다.")
    st.switch_page("pages/02_login.py")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 800px;
        margin: 0 auto;
        padding-top: 2rem;
    }

    .difficulty-wrapper {
        max-width: 800px;
        margin: 0 auto;
    }

    .difficulty-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        white-space: nowrap;
        margin-bottom: 28px;
    }

    .rule-box {
        background-color: #0f2f4f;
        color: #60a5fa;
        padding: 26px 32px;
        border-radius: 16px;
        font-size: 19px;
        line-height: 1.9;
        margin-bottom: 28px;
    }

    .recommend-box {
        background-color: #14532d;
        color: #4ade80;
        padding: 18px 22px;
        border-radius: 14px;
        text-align: center;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 28px;
    }

    .select-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label {
        font-size: 30px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="difficulty-wrapper">', unsafe_allow_html=True)

st.markdown(
    '<div class="difficulty-title">❓ 퀴즈 룰 설명</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="rule-box">
        • 선택한 난이도에 따라 MLB 선수 5명이 랜덤으로 출제됩니다.<br>
        • 사진을 보고 선수의 이름을 맞히면 됩니다.<br>
        • 각 문제는 4지선다형입니다.<br>
        • 이전/다음 버튼으로 문제를 이동할 수 있습니다.<br>
        • 제출하기를 누르면 최종 점수와 정답/오답 내역이 표시됩니다.
    </div>
    """,
    unsafe_allow_html=True
)

if st.session_state.recommended_difficulty is not None:
    st.markdown(
        f"""
        <div class="recommend-box">
            설문 결과 추천 난이도: {st.session_state.recommended_difficulty}단계
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="select-title">난이도를 선택하세요.</div>',
    unsafe_allow_html=True
)

difficulty = st.radio(
    "",
    [1, 2, 3],
    format_func=lambda x: {
        1: "1단계: 쉬움",
        2: "2단계: 보통",
        3: "3단계: 어려움"
    }[x],
    index=None
)

st.write("")

if st.button("퀴즈 풀기", use_container_width=True):
    if difficulty is None:
        st.warning("난이도를 선택해주세요.")
    else:
        success = start_quiz(difficulty)
        if success:
            st.switch_page("pages/05_quiz.py")

st.markdown('</div>', unsafe_allow_html=True)