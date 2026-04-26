import random
import streamlit as st
from players_data import get_players


@st.cache_data
def load_players():
    return get_players()


def init_state():
    if "is_login" not in st.session_state:
        st.session_state.is_login = False
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = None
    if "recommended_difficulty" not in st.session_state:
        st.session_state.recommended_difficulty = None
    if "quiz_players" not in st.session_state:
        st.session_state.quiz_players = []
    if "quiz_options" not in st.session_state:
        st.session_state.quiz_options = []
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}


def get_grade(score, difficulty):
    # 쉬움
    if difficulty == 1:
        if score <= 1:
            return "MLB 초심자"
        elif score == 2:
            return "MLB 입문자"
        elif score <= 4:
            return "MLB 팬"
        else:
            return "MLB 전문가"

    # 보통
    elif difficulty == 2:
        if score <= 1:
            return "MLB 입문자"
        elif score <= 3:
            return "MLB 팬"
        elif score == 4:
            return "MLB 상급 팬"
        else:
            return "MLB 전문가"

    # 어려움
    else:
        if score <= 1:
            return "MLB 팬"
        elif score <= 3:
            return "상급 팬"
        else:
            return "MLB 전문가"


def get_recommended_difficulty(score):
    if score <= 2:
        return 1
    elif score <= 4:
        return 2
    else:
        return 3


def start_quiz(difficulty):
    players = load_players()
    filtered_players = [
        player for player in players
        if player.get("difficulty") == difficulty
    ]

    if len(filtered_players) < 5:
        st.error("해당 난이도의 선수가 5명보다 적습니다.")
        return False

    quiz_players = random.sample(filtered_players, 5)
    all_names = [player["name"] for player in players]

    quiz_options = []

    for player in quiz_players:
        wrong_names = [name for name in all_names if name != player["name"]]
        options = random.sample(wrong_names, 3) + [player["name"]]
        random.shuffle(options)
        quiz_options.append(options)

    st.session_state.difficulty = difficulty
    st.session_state.quiz_players = quiz_players
    st.session_state.quiz_options = quiz_options
    st.session_state.current_index = 0
    st.session_state.answers = {}

    return True