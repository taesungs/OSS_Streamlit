import streamlit as st
from utils import init_state, get_recommended_difficulty

st.set_page_config(page_title="난이도 추천 설문", page_icon="⚾")

init_state()

if not st.session_state.is_login:
    st.warning("로그인이 필요합니다.")
    st.switch_page("pages/02_login.py")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 720px;
        margin: 0 auto;
        padding-top: 2rem;
    }

    .survey-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        white-space: nowrap;
        margin-bottom: 26px;
    }

    .survey-box {
        background-color: #0f2f4f;
        color: #60a5fa;
        padding: 22px 28px;
        border-radius: 14px;
        font-size: 18px;
        line-height: 1.7;
        margin-bottom: 28px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="survey-title">📝 난이도 추천 설문조사</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="survey-box">
        퀴즈를 시작하기 전에 간단한 설문을 통해 적절한 난이도를 추천해드립니다.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* 질문 텍스트 (라벨) 크기 */
    div[data-testid="stRadio"] > label {
        font-size: 22px !important;
        font-weight: 600;
    }

    /* 선택지 텍스트 크기 */
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        font-size: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

q1 = st.radio(
    "1. MLB 경기를 얼마나 자주 보나요?",
    ["거의 보지 않는다", "가끔 본다", "자주 본다"],
    index=None
)

q2 = st.radio(
    "2. MLB 선수 이름을 얼마나 알고 있나요?",
    ["유명 선수만 조금 안다", "주요 선수는 어느 정도 안다", "여러 팀의 선수까지 안다"],
    index=None
)

q3 = st.radio(
    "3. 선수 사진만 보고 이름을 맞히는 데 자신 있나요?",
    ["자신 없다", "어느 정도 가능하다", "자신 있다"],
    index=None
)

if st.button("추천 난이도 확인", use_container_width=True):
    if q1 is None or q2 is None or q3 is None:
        st.warning("모든 문항에 응답해주세요.")
    else:
        score = 0
        score += ["거의 보지 않는다", "가끔 본다", "자주 본다"].index(q1)
        score += ["유명 선수만 조금 안다", "주요 선수는 어느 정도 안다", "여러 팀의 선수까지 안다"].index(q2)
        score += ["자신 없다", "어느 정도 가능하다", "자신 있다"].index(q3)

        recommended = get_recommended_difficulty(score)
        st.session_state.recommended_difficulty = recommended

        st.success(f"추천 난이도는 {recommended}단계입니다.")

if st.session_state.recommended_difficulty is not None:
    if st.button("난이도 선택 화면으로 이동", use_container_width=True):
        st.switch_page("pages/04_level.py")