import streamlit as st
from openai import OpenAI

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="알쓸챗",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """
너는 '알쓸챗'이라는 교양형 잡학 챗봇이다.

역할:
- 사용자의 사소한 궁금증을 역사, 과학, 문화, 심리, 사회적 맥락과 연결해 설명한다.
- 단순히 정답만 말하지 않고, 왜 그런지 이야기처럼 풀어준다.
- 어려운 개념은 일상적인 비유로 쉽게 설명한다.
- 한국어로 답변한다.

답변 스타일:
- 친절하지만 과하게 가볍지 않게 답변한다.
- 교양 프로그램 패널처럼 흥미롭게 설명한다.
- 문단을 적절히 나누어 읽기 쉽게 답변한다.
- 확실하지 않은 내용은 단정하지 않고 확인이 필요하다고 말한다.
- 마지막에는 사용자가 이어서 물어볼 만한 질문을 한 문장으로 제안한다.
"""

# =========================
# CSS
# =========================
st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
    }

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #f9fafb !important;
        color: #191f28 !important;
    }

    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo",
                     "Pretendard", "Noto Sans KR", sans-serif;
    }

    .block-container {
        max-width: 760px;
        padding-top: 56px;
        padding-bottom: 80px;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    /* =========================
       Header
       ========================= */

    .hero {
        margin-bottom: 28px;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        padding: 7px 12px;
        border-radius: 999px;
        background-color: #eef4ff;
        color: #3182f6;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        line-height: 1.24;
        letter-spacing: -0.05em;
        color: #191f28;
        margin-bottom: 14px;
    }

    .hero-desc {
        font-size: 16px;
        line-height: 1.75;
        color: #6b7684;
        letter-spacing: -0.02em;
        max-width: 620px;
    }

    /* =========================
       Card
       ========================= */

    .card {
        background-color: #ffffff;
        border: 1px solid #edf0f2;
        border-radius: 28px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(25, 31, 40, 0.04);
    }

    .card-title {
        font-size: 18px;
        font-weight: 800;
        color: #191f28;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
    }

    .card-desc {
        font-size: 14px;
        line-height: 1.7;
        color: #6b7684;
        letter-spacing: -0.02em;
    }

    .question-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
        margin-top: 16px;
    }

    .question-chip {
        background-color: #f9fafb;
        border: 1px solid #edf0f2;
        border-radius: 18px;
        padding: 13px 15px;
        font-size: 14px;
        line-height: 1.55;
        color: #4e5968;
        letter-spacing: -0.02em;
    }

    .soft-divider {
        width: 100%;
        height: 1px;
        background-color: #edf0f2;
        margin: 30px 0 22px 0;
    }

    /* =========================
       API Key Input
       ========================= */

    .stTextInput label {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #4e5968 !important;
        letter-spacing: -0.02em !important;
    }

    .stTextInput input {
        height: 50px !important;
        border-radius: 16px !important;
        border: 1px solid #e5e8eb !important;
        background-color: #ffffff !important;
        color: #191f28 !important;
        font-size: 15px !important;
        padding: 0 15px !important;
        box-shadow: none !important;
    }

    .stTextInput input:focus {
        border-color: #3182f6 !important;
        box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.14) !important;
    }

    .stAlert {
        border-radius: 18px !important;
        border: none !important;
        background-color: #eef4ff !important;
        color: #4e5968 !important;
    }

    /* =========================
       Chat Messages
       ========================= */

    [data-testid="stChatMessage"] {
        background: transparent !important;
        padding: 4px 0 !important;
        margin-bottom: 12px !important;
        box-shadow: none !important;
        border: none !important;
    }

    [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    [data-testid="stChatMessageContent"] {
        padding: 0 !important;
    }

    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        max-width: 78%;
        padding: 14px 16px;
        border-radius: 22px;
        font-size: 15px;
        line-height: 1.75;
        letter-spacing: -0.02em;
    }

    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
        margin: 0;
        font-size: 15px;
        line-height: 1.75;
        letter-spacing: -0.02em;
    }

    [data-testid="stChatMessage"]:has([aria-label="assistant avatar"]) {
        display: flex !important;
        justify-content: flex-start !important;
    }

    [data-testid="stChatMessage"]:has([aria-label="assistant avatar"]) [data-testid="stMarkdownContainer"] {
        background-color: #ffffff !important;
        border: 1px solid #edf0f2 !important;
        color: #191f28 !important;
        border-top-left-radius: 8px !important;
        box-shadow: 0 6px 18px rgba(25, 31, 40, 0.04) !important;
    }

    [data-testid="stChatMessage"]:has([aria-label="assistant avatar"]) [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"]:has([aria-label="assistant avatar"]) [data-testid="stMarkdownContainer"] li {
        color: #191f28 !important;
    }

    [data-testid="stChatMessage"]:has([aria-label="user avatar"]) {
        display: flex !important;
        justify-content: flex-end !important;
    }

    [data-testid="stChatMessage"]:has([aria-label="user avatar"]) [data-testid="stMarkdownContainer"] {
        background-color: #3182f6 !important;
        color: #ffffff !important;
        border-top-right-radius: 8px !important;
        box-shadow: 0 6px 18px rgba(49, 130, 246, 0.22) !important;
    }

    [data-testid="stChatMessage"]:has([aria-label="user avatar"]) [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"]:has([aria-label="user avatar"]) [data-testid="stMarkdownContainer"] li {
        color: #ffffff !important;
    }

    /* =========================
       Custom Chat Input
       st.chat_input 미사용 버전
       ========================= */

    .chat-input-card {
        background-color: #ffffff;
        border: 1px solid #e5e8eb;
        border-radius: 28px;
        padding: 14px 16px;
        margin-top: 24px;
        box-shadow: 0 12px 36px rgba(25, 31, 40, 0.08);
    }

    .chat-input-title {
        font-size: 14px;
        font-weight: 700;
        color: #4e5968;
        letter-spacing: -0.02em;
        margin-bottom: 10px;
    }

    /* form 기본 여백 제거 */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    [data-testid="stForm"] div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    /* 채팅 입력용 text input */
    div[data-testid="stForm"] .stTextInput input {
        height: 54px !important;
        border-radius: 20px !important;
        border: 1px solid #edf0f2 !important;
        background-color: #f9fafb !important;
        color: #191f28 !important;
        font-size: 15px !important;
        padding: 0 16px !important;
    }

    div[data-testid="stForm"] .stTextInput input:focus {
        background-color: #ffffff !important;
        border-color: #3182f6 !important;
        box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.12) !important;
    }

    /* 전송 버튼 */
    div[data-testid="stForm"] .stButton button,
    div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
        height: 54px !important;
        width: 100% !important;
        border-radius: 20px !important;
        border: none !important;
        background-color: #3182f6 !important;
        color: #ffffff !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        box-shadow: none !important;
    }

    div[data-testid="stForm"] .stButton button:hover,
    div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
        background-color: #1b64da !important;
        color: #ffffff !important;
    }

    /* 보조 버튼 */
    .clear-button-wrap {
        margin-top: 10px;
    }

    .stButton button {
        border-radius: 16px !important;
        border: 1px solid #e5e8eb !important;
        background-color: #ffffff !important;
        color: #4e5968 !important;
        font-weight: 700 !important;
    }

    .stButton button:hover {
        border-color: #3182f6 !important;
        color: #3182f6 !important;
    }

    a {
        color: #3182f6 !important;
        text-decoration: none !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 상단 콘텐츠
# =========================
st.markdown(
    """
    <section class="hero">
        <div class="hero-badge">알아두면 쓸데 있는 대화</div>
        <div class="hero-title">
            궁금한 건 가볍게,<br>
            답변은 흥미롭게
        </div>
        <div class="hero-desc">
            역사, 과학, 심리, 문화, 음식, 일상 속 호기심까지.
            궁금한 것을 물어보면 여러 분야의 맥락을 엮어
            쉽게 설명해주는 교양형 챗봇입니다.
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card">
        <div class="card-title">이런 질문을 해볼 수 있어요</div>
        <div class="card-desc">
            정답만 짧게 알려주기보다, 왜 그런지 이야기처럼 풀어서 설명해드려요.
        </div>
        <div class="question-grid">
            <div class="question-chip">왜 사람들은 커피를 마시면 집중이 잘 된다고 느낄까요?</div>
            <div class="question-chip">고대 사람들은 시간을 어떻게 측정했을까요?</div>
            <div class="question-chip">왜 어떤 노래는 계속 머릿속에서 반복될까요?</div>
            <div class="question-chip">김치가 발효되면 몸에 좋은 이유는 무엇인가요?</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card">
        <div class="card-title">대화를 시작하기 전에</div>
        <div class="card-desc">
            OpenAI API 키를 입력하면 바로 대화를 시작할 수 있어요.
            입력한 키는 현재 세션에서만 사용됩니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# API 키 입력
# =========================
openai_api_key = st.text_input(
    "OpenAI API 키",
    type="password",
    placeholder="sk-...",
)

if not openai_api_key:
    st.info("API 키를 입력하면 챗봇을 사용할 수 있어요.", icon="🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# =========================
# 세션 상태
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# 기존 메시지 출력
# =========================
if st.session_state.messages:
    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# 채팅 입력 영역
# =========================
st.markdown(
    """
    <div class="chat-input-card">
        <div class="chat-input-title">궁금한 것을 물어보세요</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("chat_form", clear_on_submit=True):
    input_col, button_col = st.columns([5, 1.15])

    with input_col:
        prompt = st.text_input(
            "질문 입력",
            placeholder="무엇이 궁금하신가요?",
            label_visibility="collapsed",
        )

    with button_col:
        submitted = st.form_submit_button("전송")

# =========================
# 답변 생성
# =========================
if submitted and prompt.strip():
    user_prompt = prompt.strip()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    messages_for_api = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        *[
            {
                "role": message["role"],
                "content": message["content"],
            }
            for message in st.session_state.messages
        ],
    ]

    def generate_response():
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages_for_api,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    with st.chat_message("assistant"):
        response = st.write_stream(generate_response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

# =========================
# 대화 초기화
# =========================
if st.session_state.messages:
    st.markdown('<div class="clear-button-wrap">', unsafe_allow_html=True)

    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
