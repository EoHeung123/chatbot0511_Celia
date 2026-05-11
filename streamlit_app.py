import streamlit as st
from openai import OpenAI

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="알쓸챗",
    page_icon="💬",
    layout="centered"
)

# =========================
# Toss-style Light Mode CSS
# =========================
st.markdown(
    """
    <style>
    /* 전체 라이트모드 고정 */
    .stApp {
        background-color: #f9fafb;
        color: #191f28;
    }

    .block-container {
        max-width: 760px;
        padding-top: 56px;
        padding-bottom: 120px;
    }

    /* Streamlit 기본 UI 숨김 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 전체 폰트 톤 */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo",
                     "Pretendard", "Noto Sans KR", sans-serif;
    }

    /* 상단 히어로 영역 */
    .hero {
        margin-bottom: 32px;
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
        font-size: 40px;
        font-weight: 800;
        line-height: 1.28;
        letter-spacing: -0.045em;
        color: #191f28;
        margin-bottom: 14px;
    }

    .hero-desc {
        font-size: 16px;
        line-height: 1.75;
        letter-spacing: -0.02em;
        color: #6b7684;
        max-width: 620px;
    }

    /* 안내 카드 */
    .info-card {
        background-color: #ffffff;
        border-radius: 28px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(25, 31, 40, 0.04);
        border: 1px solid #edf0f2;
        margin-bottom: 20px;
    }

    .info-title {
        font-size: 18px;
        font-weight: 800;
        color: #191f28;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
    }

    .info-desc {
        font-size: 14px;
        line-height: 1.7;
        color: #6b7684;
        letter-spacing: -0.02em;
    }

    /* 질문 예시 */
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

    /* API 입력 */
    .stTextInput label {
        font-size: 14px;
        font-weight: 700;
        color: #4e5968;
        letter-spacing: -0.02em;
    }

    .stTextInput input {
        height: 48px;
        border-radius: 16px;
        border: 1px solid #e5e8eb;
        background-color: #ffffff;
        color: #191f28;
        font-size: 15px;
        padding: 0 15px;
    }

    .stTextInput input:focus {
        border-color: #3182f6;
        box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.14);
    }

    /* 안내 알림 */
    .stAlert {
        border-radius: 18px;
        border: none;
        background-color: #eef4ff;
        color: #4e5968;
    }

    /* 채팅 영역 전체 */
    [data-testid="stChatMessage"] {
        background: transparent;
        padding: 4px 0;
        margin-bottom: 12px;
        box-shadow: none;
        border: none;
    }

    /* 아바타 숨김: 토스처럼 더 담백하게 */
    [data-testid="stChatMessageAvatar"] {
        display: none;
    }

    /* 메시지 내부 여백 제거 */
    [data-testid="stChatMessageContent"] {
        padding: 0;
    }

    /* 말풍선 기본 */
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

    /* Assistant 말풍선 */
    [data-testid="stChatMessage"]:has([aria-label="assistant avatar"]) {
        display: flex;
        justify-content: flex-start;
    }

    [data-testid="stChatMessage"]:has([aria-label="assistant avatar"]) [data-testid="stMarkdownContainer"] {
        background-color: #ffffff;
        border: 1px solid #edf0f2;
        color: #191f28;
        border-top-left-radius: 8px;
        box-shadow: 0 6px 18px rgba(25, 31, 40, 0.04);
    }

    [data-testid="stChatMessage"]:has([aria-label="assistant avatar"]) [data-testid="stMarkdownContainer"] p {
        color: #191f28;
    }

    /* User 말풍선 */
    [data-testid="stChatMessage"]:has([aria-label="user avatar"]) {
        display: flex;
        justify-content: flex-end;
    }

    [data-testid="stChatMessage"]:has([aria-label="user avatar"]) [data-testid="stMarkdownContainer"] {
        background-color: #3182f6;
        color: #ffffff;
        border-top-right-radius: 8px;
        box-shadow: 0 6px 18px rgba(49, 130, 246, 0.22);
    }

    [data-testid="stChatMessage"]:has([aria-label="user avatar"]) [data-testid="stMarkdownContainer"] p {
        color: #ffffff;
    }

    /* 채팅 입력창 */
    [data-testid="stChatInput"] {
        background-color: #ffffff;
        border: 1px solid #e5e8eb;
        border-radius: 24px;
        box-shadow: 0 12px 36px rgba(25, 31, 40, 0.10);
    }

    [data-testid="stChatInput"] textarea {
        font-size: 15px;
        color: #191f28;
        letter-spacing: -0.02em;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #8b95a1;
    }

    /* 링크 */
    a {
        color: #3182f6 !important;
        text-decoration: none;
        font-weight: 700;
    }

    /* 구분선 */
    .soft-divider {
        height: 1px;
        background-color: #edf0f2;
        margin: 28px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Header
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
    unsafe_allow_html=True
)

# =========================
# Suggestion Card
# =========================
st.markdown(
    """
    <div class="info-card">
        <div class="info-title">이런 질문을 해볼 수 있어요</div>
        <div class="info-desc">
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
    unsafe_allow_html=True
)

# =========================
# API Key Section
# =========================
st.markdown(
    """
    <div class="info-card">
        <div class="info-title">대화를 시작하기 전에</div>
        <div class="info-desc">
            OpenAI API 키를 입력하면 바로 대화를 시작할 수 있어요.
            입력한 키는 현재 세션에서만 사용됩니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

openai_api_key = st.text_input(
    "OpenAI API 키",
    type="password",
    placeholder="sk-..."
)

if not openai_api_key:
    st.info("API 키를 입력하면 챗봇을 사용할 수 있어요.", icon="🗝️")

else:
    client = OpenAI(api_key=openai_api_key)

    # =========================
    # Session State
    # =========================
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # =========================
    # Existing Messages
    # =========================
    if st.session_state.messages:
        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # =========================
    # Chat Input
    # =========================
    if prompt := st.chat_input("무엇이 궁금하신가요?"):

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # 챗봇 성격 정의
        system_prompt = """
너는 '알쓸챗'이라는 교양형 잡학 챗봇이다.

역할:
- 사용자의 사소한 궁금증을 역사, 과학, 문화, 심리, 사회적 맥락과 연결해 설명한다.
- 단순한 정보 나열보다 '왜 그런지'를 중심으로 답변한다.
- 어려운 개념은 일상적인 비유로 쉽게 풀어준다.
- 한국어로 답변한다.

답변 스타일:
- 친절하지만 과하게 가볍지 않게 답변한다.
- 교양 프로그램 패널처럼 흥미롭게 설명한다.
- 사용자가 이해하기 쉽도록 문단을 나누어 답변한다.
- 확실하지 않은 내용은 단정하지 않고 확인이 필요하다고 말한다.
- 마지막에는 사용자가 이어서 물어볼 만한 질문을 한 문장으로 제안한다.
"""

        # 이전 대화 구성
        input_messages = [
            {
                "role": "developer",
                "content": system_prompt
            }
        ]

        for m in st.session_state.messages:
            input_messages.append(
                {
                    "role": m["role"],
                    "content": m["content"]
                }
            )

        # 스트리밍 응답 생성 함수
        def stream_response():
            full_response = ""

            stream = client.responses.create(
                model="gpt-5.4-mini",
                input=input_messages,
                stream=True,
            )

            for event in stream:
                if event.type == "response.output_text.delta":
                    delta = event.delta
                    full_response += delta
                    yield delta

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response
                }
            )

        # AI 메시지 출력
        with st.chat_message("assistant"):
            st.write_stream(stream_response)
