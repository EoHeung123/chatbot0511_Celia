import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 챗봇",
    page_icon="💬",
    layout="centered"
)

# 토스 스타일 CSS
st.markdown(
    """
    <style>
    /* 전체 배경 */
    .stApp {
        background-color: #f9fafb;
    }

    /* 기본 컨테이너 폭 */
    .block-container {
        max-width: 720px;
        padding-top: 48px;
        padding-bottom: 120px;
    }

    /* Streamlit 기본 메뉴 숨김 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 상단 히어로 영역 */
    .hero-card {
        background: #ffffff;
        padding: 32px 28px;
        border-radius: 28px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04);
        margin-bottom: 24px;
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background-color: #eef4ff;
        color: #3182f6;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 32px;
        font-weight: 800;
        line-height: 1.35;
        color: #191f28;
        margin-bottom: 12px;
        letter-spacing: -0.03em;
    }

    .hero-desc {
        font-size: 16px;
        line-height: 1.7;
        color: #6b7684;
        letter-spacing: -0.02em;
    }

    /* API 키 입력 영역 */
    .api-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 24px;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.035);
        margin-bottom: 24px;
    }

    .api-title {
        font-size: 18px;
        font-weight: 700;
        color: #191f28;
        margin-bottom: 6px;
    }

    .api-desc {
        font-size: 14px;
        color: #8b95a1;
        margin-bottom: 16px;
        line-height: 1.6;
    }

    /* 입력창 */
    .stTextInput input {
        border-radius: 16px;
        border: 1px solid #e5e8eb;
        padding: 14px 16px;
        font-size: 15px;
        background-color: #f9fafb;
    }

    .stTextInput input:focus {
        border-color: #3182f6;
        box-shadow: 0 0 0 2px rgba(49, 130, 246, 0.15);
    }

    /* 안내 메시지 */
    .stAlert {
        border-radius: 18px;
        background-color: #f2f4f6;
        border: none;
        color: #4e5968;
    }

    /* 채팅 메시지 */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border-radius: 22px;
        padding: 16px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03);
    }

    [data-testid="stChatMessage"] p {
        font-size: 15px;
        line-height: 1.7;
        color: #191f28;
    }

    /* 채팅 입력창 */
    [data-testid="stChatInput"] {
        background-color: #ffffff;
        border-radius: 24px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    }

    [data-testid="stChatInput"] textarea {
        font-size: 15px;
        color: #191f28;
    }

    /* 링크 컬러 */
    a {
        color: #3182f6 !important;
        text-decoration: none;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 상단 소개 카드
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-badge">AI Chat</div>
        <div class="hero-title">
            필요한 답변을<br>
            빠르게 물어보세요
        </div>
        <div class="hero-desc">
            OpenAI 모델을 사용해 질문에 답변하는 간단한 챗봇입니다.
            API 키를 입력하면 바로 대화를 시작할 수 있어요.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# API 키 입력 카드
st.markdown(
    """
    <div class="api-card">
        <div class="api-title">API 키 입력</div>
        <div class="api-desc">
            OpenAI API 키는 안전하게 입력되며, 현재 세션에서만 사용됩니다.
            API 키는 <a href="https://platform.openai.com/account/api-keys" target="_blank">OpenAI 대시보드</a>에서 발급받을 수 있어요.
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
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 채팅 메시지 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("궁금한 내용을 입력해보세요"):

        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # AI 응답 스트리밍 표시 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
