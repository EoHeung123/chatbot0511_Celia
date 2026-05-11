import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(
    page_title="알쓸살롱",
    page_icon="☕",
    layout="centered"
)

# 라이트모드 + 교양 토크쇼 스타일 CSS
st.markdown(
    """
    <style>
    /* 전체 라이트 배경 */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(255, 245, 224, 0.9), transparent 34%),
            linear-gradient(180deg, #fffdf8 0%, #f7f8fa 100%);
        color: #191f28;
    }

    /* 기본 컨테이너 */
    .block-container {
        max-width: 760px;
        padding-top: 48px;
        padding-bottom: 120px;
    }

    /* Streamlit 기본 요소 숨김 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 히어로 카드 */
    .hero-card {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(229, 232, 235, 0.9);
        padding: 34px 30px 30px 30px;
        border-radius: 30px;
        box-shadow: 0 16px 48px rgba(25, 31, 40, 0.06);
        margin-bottom: 22px;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 12px;
        border-radius: 999px;
        background: #fff4dd;
        color: #9a6700;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 36px;
        font-weight: 850;
        line-height: 1.28;
        letter-spacing: -0.045em;
        color: #191f28;
        margin-bottom: 14px;
    }

    .hero-desc {
        font-size: 16px;
        line-height: 1.75;
        color: #6b7684;
        letter-spacing: -0.02em;
    }

    /* 질문 예시 카드 */
    .suggestion-card {
        background: #ffffff;
        border: 1px solid #eef0f3;
        padding: 22px;
        border-radius: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 28px rgba(25, 31, 40, 0.04);
    }

    .section-title {
        font-size: 17px;
        font-weight: 800;
        color: #191f28;
        margin-bottom: 10px;
        letter-spacing: -0.03em;
    }

    .question-list {
        display: grid;
        gap: 8px;
        margin-top: 12px;
    }

    .question-item {
        background: #f8f9fb;
        border: 1px solid #edf0f2;
        border-radius: 16px;
        padding: 12px 14px;
        color: #4e5968;
        font-size: 14px;
        line-height: 1.55;
        letter-spacing: -0.02em;
    }

    /* API 카드 */
    .api-card {
        background: #ffffff;
        border: 1px solid #eef0f3;
        padding: 22px;
        border-radius: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 28px rgba(25, 31, 40, 0.04);
    }

    .api-title {
        font-size: 17px;
        font-weight: 800;
        color: #191f28;
        margin-bottom: 6px;
        letter-spacing: -0.03em;
    }

    .api-desc {
        font-size: 14px;
        line-height: 1.65;
        color: #8b95a1;
        letter-spacing: -0.02em;
    }

    /* 입력창 */
    .stTextInput label {
        font-size: 14px;
        font-weight: 700;
        color: #4e5968;
    }

    .stTextInput input {
        border-radius: 16px;
        border: 1px solid #e5e8eb;
        padding: 14px 16px;
        font-size: 15px;
        background-color: #ffffff;
        color: #191f28;
    }

    .stTextInput input:focus {
        border-color: #b0894f;
        box-shadow: 0 0 0 3px rgba(176, 137, 79, 0.15);
    }

    /* 안내 메시지 */
    .stAlert {
        border-radius: 18px;
        border: 1px solid #edf0f2;
        background-color: #fffaf0;
        color: #4e5968;
    }

    /* 채팅 메시지 */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border: 1px solid #eef0f3;
        border-radius: 24px;
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 0 8px 26px rgba(25, 31, 40, 0.04);
    }

    [data-testid="stChatMessage"] p {
        font-size: 15px;
        line-height: 1.75;
        color: #191f28;
        letter-spacing: -0.02em;
    }

    /* 채팅 입력창 */
    [data-testid="stChatInput"] {
        background-color: #ffffff;
        border-radius: 24px;
        border: 1px solid #e5e8eb;
        box-shadow: 0 14px 40px rgba(25, 31, 40, 0.11);
    }

    [data-testid="stChatInput"] textarea {
        font-size: 15px;
        color: #191f28;
    }

    /* 버튼 */
    .stButton button {
        border-radius: 999px;
        border: 1px solid #e5e8eb;
        background: #ffffff;
        color: #4e5968;
        font-size: 14px;
        font-weight: 700;
        padding: 8px 14px;
    }

    .stButton button:hover {
        border-color: #b0894f;
        color: #7a5520;
        background: #fff8ec;
    }

    /* 링크 */
    a {
        color: #7a5520 !important;
        text-decoration: none;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 상단 소개 영역
st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">☕ 오늘의 잡학 대화</div>
        <div class="hero-title">
            사소한 궁금증도<br>
            이야기처럼 풀어드릴게요
        </div>
        <div class="hero-desc">
            역사, 과학, 심리, 문화, 음식, 일상 속 호기심까지.
            궁금한 것을 물어보면 여러 분야의 맥락을 엮어
            쉽고 흥미롭게 설명해주는 교양형 챗봇입니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 질문 예시 영역
st.markdown(
    """
    <div class="suggestion-card">
        <div class="section-title">이런 질문을 해볼 수 있어요</div>
        <div class="question-list">
            <div class="question-item">왜 사람들은 커피를 마시면 집중이 잘 된다고 느낄까요?</div>
            <div class="question-item">고대 사람들은 시간을 어떻게 측정했을까요?</div>
            <div class="question-item">왜 어떤 노래는 계속 머릿속에서 반복될까요?</div>
            <div class="question-item">김치가 발효되면 몸에 좋은 이유는 무엇인가요?</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# API 키 입력 영역
st.markdown(
    """
    <div class="api-card">
        <div class="api-title">대화를 시작하기 전에</div>
        <div class="api-desc">
            OpenAI API 키를 입력하면 챗봇을 사용할 수 있어요.
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
    st.info("API 키를 입력하면 알쓸살롱이 열려요.", icon="🗝️")

else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 대화 메시지 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 메시지 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("무엇이 궁금하신가요?"):

        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # 챗봇의 성격을 정의하는 시스템 메시지
        system_prompt = {
            "role": "system",
            "content": """
너는 '알쓸살롱'이라는 교양형 잡학 챗봇이다.
사용자가 궁금한 것을 물어보면 역사, 과학, 문화, 심리, 사회적 맥락을 연결해 쉽고 흥미롭게 설명한다.

답변 원칙:
1. 어려운 개념은 일상적인 비유로 설명한다.
2. 단순 정보 나열보다 '왜 그런지'를 중심으로 설명한다.
3. 사용자가 더 궁금해할 만한 연결 질문을 마지막에 하나 제안한다.
4. 확실하지 않은 정보는 단정하지 말고, 확인이 필요하다고 말한다.
5. 답변 톤은 친절한 교양 토크쇼 패널처럼 자연스럽게 유지한다.
6. 한국어로 답변한다.
"""
        }

        # AI 응답 생성
        stream = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                system_prompt,
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            ],
            stream=True,
        )

        # AI 응답 출력 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
