import random
import streamlit as st
from players_data import get_players

st.set_page_config(page_title="MLB 선수 퀴즈", page_icon="⚾")


@st.cache_data
def load_players():
    return get_players()


def init_state():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "is_login" not in st.session_state:
        st.session_state.is_login = False
    if "quiz_players" not in st.session_state:
        st.session_state.quiz_players = []
    if "quiz_options" not in st.session_state:
        st.session_state.quiz_options = []
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}


def get_grade(score):
    if score <= 1:
        return "야알못"
    elif score == 2:
        return "MLB 입문자"
    elif score <= 4:
        return "MLB 팬"
    else:
        return "MLB 전문가"


def reset_quiz():
    players = load_players()
    quiz_players = random.sample(players, 5)
    all_names = [player["name"] for player in players]

    quiz_options = []

    for player in quiz_players:
        wrong_names = [name for name in all_names if name != player["name"]]
        options = random.sample(wrong_names, 3) + [player["name"]]
        random.shuffle(options)
        quiz_options.append(options)

    st.session_state.quiz_players = quiz_players
    st.session_state.quiz_options = quiz_options
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.page = "quiz"


def logout():
    st.session_state.is_login = False
    st.session_state.page = "home"
    st.session_state.quiz_players = []
    st.session_state.quiz_options = []
    st.session_state.current_index = 0
    st.session_state.answers = {}


def show_top_login_bar():
    left, center, right = st.columns([5, 2, 1.3])

    with center:
        st.success("로그인 상태")
    with right:
        if st.button("로그아웃", use_container_width=True):
            logout()
            st.rerun()


def home_page():
    left, center, right = st.columns([1, 2, 1])

    with center:
        st.markdown(
            "<h1 style='text-align:center;'>⚾ MLB 선수 맞히기 퀴즈 ⚾️</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style='display:flex; justify-content:center; margin-top:20px;'>
                <img src="https://www.mlbstatic.com/team-logos/share/mlb.jpg?v=2" width="420">
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style='text-align:center; font-size:28px; font-weight:bold; margin-top:30px;'>
                학번: 2023204067<br>
                이름: 엄태성
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        st.write("")

        if st.button("로그인 하기", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()


def login_page():
    left, center, right = st.columns([1, 2, 1])

    with center:
        st.title("로그인")

        user_id = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")

        if st.button("로그인", use_container_width=True):
            if user_id == "mlb" and password == "1234":
                st.session_state.is_login = True
                st.session_state.page = "quiz_intro"
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 틀렸습니다.")

        if st.button("첫 화면으로 돌아가기", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()


def quiz_intro_page():
    show_top_login_bar()

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.title("⚾ 퀴즈 룰 설명")

        st.info(
            """
            - 총 선수 데이터 중 랜덤으로 5명이 출제됩니다.
            - 사진을 보고 MLB 선수의 이름을 맞히면 됩니다.
            - 각 문제는 4지선다형입니다.
            - 이전/다음 버튼으로 문제를 이동할 수 있습니다.
            - 제출하기를 누르면 최종 점수와 정답/오답 내역이 표시됩니다.
            """
        )

        if st.button("퀴즈 풀기", use_container_width=True):
            reset_quiz()
            st.rerun()


def quiz_page():
    show_top_login_bar()

    index = st.session_state.current_index
    player = st.session_state.quiz_players[index]
    options = st.session_state.quiz_options[index]

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.progress((index + 1) / 5)
        st.write(f"### {index + 1}번 문제 / 5문제")

        st.image(player["image"], width=320)

        selected_answer = st.radio(
            "이 선수의 이름은?",
            options,
            index=None,
            key=f"answer_{index}"
        )

        if selected_answer is not None:
            st.session_state.answers[index] = selected_answer

        st.divider()

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
                    st.session_state.page = "result"
                    st.rerun()


def result_page():
    show_top_login_bar()

    score = 0

    for i, player in enumerate(st.session_state.quiz_players):
        if st.session_state.answers.get(i) == player["name"]:
            score += 1

    grade = get_grade(score)

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.title("📌 퀴즈 결과")
        st.metric("총점", f"{score}/5")
        st.subheader(f"등급: {grade}")

        if grade == "야알못":
            st.error("아직 MLB 선수들이 조금 낯설어요. 다시 도전해보세요!")
        elif grade == "MLB 입문자":
            st.warning("기본적인 MLB 스타 선수들을 알아가는 단계입니다.")
        elif grade == "MLB 팬":
            st.success("MLB 선수들을 꽤 잘 알고 있습니다!")
        else:
            st.balloons()
            st.success("완벽합니다! 당신은 MLB 전문가입니다.")

        st.divider()
        st.subheader("제출 내용 확인")

        for i, player in enumerate(st.session_state.quiz_players):
            user_answer = st.session_state.answers.get(i)
            correct_answer = player["name"]

            if user_answer == correct_answer:
                st.success(f"{i + 1}번 정답 | 제출: {user_answer}")
            else:
                st.error(f"{i + 1}번 오답 | 제출: {user_answer} / 정답: {correct_answer}")

        st.divider()

        if st.button("재도전하기", use_container_width=True):
            reset_quiz()
            st.rerun()

        if st.button("퀴즈 설명 화면으로 돌아가기", use_container_width=True):
            st.session_state.page = "quiz_intro"
            st.rerun()


init_state()

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "quiz_intro":
    quiz_intro_page()
elif st.session_state.page == "quiz":
    quiz_page()
elif st.session_state.page == "result":
    result_page()