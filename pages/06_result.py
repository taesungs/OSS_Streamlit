import streamlit as st
from utils import init_state, get_grade, start_quiz

st.set_page_config(page_title="퀴즈 결과", page_icon="⚾")

init_state()

if not st.session_state.is_login:
    st.warning("로그인이 필요합니다.")
    st.switch_page("pages/02_login.py")

if not st.session_state.quiz_players:
    st.warning("퀴즈 결과가 없습니다.")
    st.switch_page("pages/04_level.py")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1050px;
        margin: 0 auto;
        padding-top: 3rem;
        padding-bottom: 2rem;
    }

    .result-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        white-space: nowrap;
        margin-top: 10px;
        margin-bottom: 30px;
        line-height: 1.3;
    }

    .summary-card {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 18px;
        padding: 32px 28px;
        text-align: center;
        margin-bottom: 28px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
    }

    .score-text {
        font-size: 46px;
        font-weight: 900;
        margin-bottom: 12px;
    }

    .grade-text {
        font-size: 32px;
        font-weight: 800;
    }

    .message-box {
        padding: 18px 22px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 34px;
    }

    .message-success {
        background-color: #14532d;
        color: #4ade80;
    }

    .message-warning {
        background-color: #422006;
        color: #facc15;
    }

    .message-error {
        background-color: #3f0f0f;
        color: #f87171;
    }

    .review-title {
        font-size: 30px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .review-card {
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 20px;
        border: 1px solid #374151;
    }

    .correct {
        background-color: #052e1b;
        border-color: #14532d;
    }

    .wrong {
        background-color: #3f0f0f;
        border-color: #7f1d1d;
    }

    .review-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        object-position: top center;
        border-radius: 12px;
        margin-bottom: 14px;
    }

    .review-question {
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .answer-text {
        font-size: 17px;
        line-height: 1.7;
    }
    </style>
    """,
    unsafe_allow_html=True
)

score = 0

for i, player in enumerate(st.session_state.quiz_players):
    if st.session_state.answers.get(i) == player["name"]:
        score += 1

grade = get_grade(score, st.session_state.difficulty)

if grade == "MLB 초심자":
    message = "아직 MLB 선수들이 조금 낯설어요. 기초부터 차근차근 익혀보세요!"
    message_class = "message-error"

elif grade == "MLB 입문자":
    message = "기본적인 MLB 선수들을 알아가는 단계입니다."
    message_class = "message-warning"

elif grade == "MLB 팬":
    message = "MLB 선수들을 꽤 잘 알고 있습니다!"
    message_class = "message-success"

elif grade == "MLB 상급 팬":
    message = "상당한 수준입니다! MLB에 대한 이해도가 높습니다."
    message_class = "message-success"

else:  # 전문가
    message = "완벽합니다! 당신은 MLB 전문가입니다."
    message_class = "message-success"
    st.balloons()

st.markdown('<div class="result-title">📌 퀴즈 결과</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="summary-card">
        <div class="score-text">{score}/5</div>
        <div class="grade-text">등급: {grade}</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="message-box {message_class}">
        {message}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="review-title">제출 내용 확인</div>', unsafe_allow_html=True)

for row_start in range(0, len(st.session_state.quiz_players), 2):
    cols = st.columns(2)

    for col_index, col in enumerate(cols):
        player_index = row_start + col_index

        if player_index >= len(st.session_state.quiz_players):
            break

        player = st.session_state.quiz_players[player_index]
        user_answer = st.session_state.answers.get(player_index)
        correct_answer = player["name"]
        is_correct = user_answer == correct_answer
        card_class = "correct" if is_correct else "wrong"
        result_text = "정답" if is_correct else "오답"

        with col:
            st.markdown(
                f"""
                <div class="review-card {card_class}">
                    <img class="review-img" src="{player["image"]}">
                    <div class="review-question">{player_index + 1}번 {result_text}</div>
                    <div class="answer-text">
                        제출: {user_answer}<br>
                        정답: {correct_answer}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("재도전하기", use_container_width=True):
        start_quiz(st.session_state.difficulty)
        st.switch_page("pages/05_quiz.py")

with col2:
    if st.button("난이도 다시 선택하기", use_container_width=True):
        st.switch_page("pages/04_level.py")