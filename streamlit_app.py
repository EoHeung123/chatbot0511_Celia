import html
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

MODEL = "gpt-5.4-mini"

# =========================
# 패널 페르소나
# =========================
PERSONAS = {
    "all": {
        "emoji": "✨",
        "name": "통합 패널",
        "role": "질문에 맞는 패널이 자연스럽게 등장하는 알쓸신잡형 통합 모드",
        "desc": "질문에 따라 물리학자, 건축학자, 역사학자, 심리학자 등 적절한 패널이 답변합니다. 여러 관점이 필요하면 여러 명이 각자의 이야기로 풀어줍니다.",
        "voice": "여러 패널이 실제 대화하듯 자연스럽게 이어받아 말한다.",
        "examples": [
            "왜 사람들은 커피를 마시면 집중이 잘 된다고 느낄까요?",
            "왜 오래된 골목은 걷기 좋게 느껴질까요?",
            "왜 어떤 노래는 계속 머릿속에서 반복될까요?",
        ],
    },
    "architect": {
        "emoji": "🏛️",
        "name": "건축학자",
        "role": "공간, 도시, 건축, 생활환경의 관점으로 설명하는 패널",
        "desc": "공간 구조, 도시의 흐름, 건축 양식, 사람이 공간을 사용하는 방식을 중심으로 답변합니다.",
        "voice": "공간을 직접 걸어보며 설명하듯, 장소감과 구조를 구어체로 풀어낸다.",
        "examples": [
            "왜 오래된 골목은 걷기 좋게 느껴질까요?",
            "좋은 카페 공간은 왜 편안하게 느껴질까요?",
            "도시는 왜 점점 비슷한 모습이 되어갈까요?",
        ],
    },
    "physicist": {
        "emoji": "🧲",
        "name": "물리학자",
        "role": "자연현상, 에너지, 시간, 빛, 소리의 원리를 설명하는 패널",
        "desc": "일상 속 현상을 물리 법칙과 원리로 쉽게 풀어 설명합니다.",
        "voice": "어려운 수식 대신 직관적인 비유를 쓰고, 신기한 현상을 옆에서 설명하듯 말한다.",
        "examples": [
            "하늘은 왜 파랗게 보이나요?",
            "전자레인지는 음식을 어떻게 데우나요?",
            "엘리베이터가 출발할 때 몸이 왜 무겁게 느껴질까요?",
        ],
    },
    "historian": {
        "emoji": "📜",
        "name": "역사학자",
        "role": "사건의 배경, 시대 흐름, 문화적 맥락을 설명하는 패널",
        "desc": "지금의 현상이 과거의 어떤 흐름에서 왔는지 맥락 중심으로 답변합니다.",
        "voice": "연도 암기처럼 말하지 않고, 당시 사람들의 선택과 시대 분위기를 이야기하듯 들려준다.",
        "examples": [
            "고대 사람들은 시간을 어떻게 측정했을까요?",
            "커피는 어떻게 전 세계로 퍼졌을까요?",
            "왜 어떤 도시는 역사적으로 더 빨리 발전했을까요?",
        ],
    },
    "psychologist": {
        "emoji": "🧠",
        "name": "심리학자",
        "role": "인간의 감정, 기억, 행동, 선택을 설명하는 패널",
        "desc": "사람이 왜 그렇게 느끼고 행동하는지 심리와 인지 관점에서 답변합니다.",
        "voice": "사용자가 자기 경험을 떠올릴 수 있도록 부드럽고 대화하듯 설명한다.",
        "examples": [
            "왜 사람은 미룰수록 더 하기 싫어질까요?",
            "왜 어떤 말은 오래 기억에 남을까요?",
            "왜 우리는 익숙한 것을 더 안전하다고 느낄까요?",
        ],
    },
    "sociologist": {
        "emoji": "🌐",
        "name": "사회학자",
        "role": "사회 구조, 관계, 문화, 트렌드의 관점으로 설명하는 패널",
        "desc": "개인의 선택처럼 보이는 현상을 사회적 구조와 문화 흐름으로 풀어 설명합니다.",
        "voice": "개인의 취향처럼 보이는 일도 사회적 분위기와 연결해 넓게 풀어준다.",
        "examples": [
            "왜 요즘 사람들은 혼자 있는 시간을 더 중요하게 생각할까요?",
            "유행은 어떻게 만들어질까요?",
            "왜 특정 세대는 일과 삶의 균형을 더 중요하게 볼까요?",
        ],
    },
    "food_researcher": {
        "emoji": "🍚",
        "name": "음식문화 연구자",
        "role": "음식, 발효, 식문화, 생활사의 관점으로 설명하는 패널",
        "desc": "음식의 과학적 원리와 문화적 의미를 함께 설명합니다.",
        "voice": "맛, 생활, 문화, 과학을 한 상 차리듯 친근하게 엮어 말한다.",
        "examples": [
            "김치가 발효되면 몸에 좋은 이유는 무엇인가요?",
            "왜 국물 음식은 위로가 된다고 느낄까요?",
            "사람들은 왜 매운맛을 좋아할까요?",
        ],
    },
    "economist": {
        "emoji": "📈",
        "name": "경제학자",
        "role": "선택, 비용, 시장, 소비 행동의 관점으로 설명하는 패널",
        "desc": "사람들의 선택과 사회 현상을 비용, 효용, 인센티브 관점에서 설명합니다.",
        "voice": "딱딱한 경제 이론보다 일상의 선택 구조를 예시로 들어 쉽게 말한다.",
        "examples": [
            "왜 사람들은 한정판에 더 끌릴까요?",
            "구독 서비스는 왜 이렇게 많아졌을까요?",
            "가격이 비싸면 왜 더 좋아 보일 때가 있을까요?",
        ],
    },
    "linguist": {
        "emoji": "💬",
        "name": "언어학자",
        "role": "말, 표현, 의미, 문화적 언어 습관을 설명하는 패널",
        "desc": "우리가 쓰는 말과 표현이 어떻게 의미를 만들고 관계를 바꾸는지 설명합니다.",
        "voice": "말투와 표현의 미묘한 차이를 실제 대화 사례처럼 풀어준다.",
        "examples": [
            "왜 같은 말도 말투에 따라 다르게 들릴까요?",
            "유행어는 왜 갑자기 퍼졌다가 사라질까요?",
            "사람들은 왜 줄임말을 많이 쓰게 될까요?",
        ],
    },
}

# =========================
# 시스템 프롬프트
# =========================
BASE_SYSTEM_PROMPT = """
너는 '알쓸챗'이라는 교양형 잡학 챗봇이다.
사용자는 오늘 방송에 게스트로 나온 사람이다.
사용자가 질문하면, 알쓸신잡 패널처럼 지적이지만 어렵지 않게, 구어체로 자연스럽게 답변한다.

공통 원칙:
- 반드시 한국어로 답변한다.
- 강의문, 보고서, 백과사전 문체를 피한다.
- 사용자를 '게스트님'처럼 대화에 참여한 사람으로 대우한다.
- 단순 정보 나열보다 '왜 그런지'와 '어떻게 연결되는지'를 중심으로 설명한다.
- 어려운 개념은 일상적인 비유로 풀어준다.
- 답변은 너무 짧지 않게, 하지만 과하게 장황하지 않게 작성한다.
- 확실하지 않은 정보는 단정하지 않고 확인이 필요하다고 말한다.
- 마지막에는 사용자가 이어서 물어볼 만한 질문을 자연스럽게 제안한다.
- 마크다운 제목(#, ##)은 쓰지 않는다.
- 답변은 실제 패널이 말하는 것처럼 자연스러운 문단으로 작성한다.
"""

def build_system_prompt(persona_key):
    persona = PERSONAS[persona_key]

    if persona_key == "all":
        return f"""
{BASE_SYSTEM_PROMPT}

현재 모드: 통합 패널 모드

통합 패널 모드의 답변 방식:
- 사용자의 질문을 보고 가장 적절한 패널을 1명 선택해 답변해도 된다.
- 여러 분야의 관점이 함께 필요하면 2~3명의 패널이 차례로 짧게 이야기해도 된다.
- 답변에는 패널 이름을 자연스럽게 붙인다.
  예: "🧲 물리학자: 이건 사실 힘의 문제로 보면 꽤 재밌어요."
  예: "🏛️ 건축학자: 저는 이걸 공간의 경험으로도 볼 수 있다고 생각해요."
- 여러 명이 말할 때는 서로 다른 지식을 가진 사람들이 한 테이블에서 이야기하는 느낌을 준다.
- 사용자가 방송의 게스트로 참여한 듯이, 질문을 받아서 패널들이 대화해주는 느낌을 만든다.
- 단순히 분야별 목록을 나열하지 말고, 하나의 이야기처럼 이어지게 답변한다.

오늘의 패널 후보:
- 🏛️ 건축학자
- 🧲 물리학자
- 📜 역사학자
- 🧠 심리학자
- 🌐 사회학자
- 🍚 음식문화 연구자
- 📈 경제학자
- 💬 언어학자
"""

    return f"""
{BASE_SYSTEM_PROMPT}

현재 선택된 패널:
- 이름: {persona["name"]}
- 역할: {persona["role"]}
- 답변 관점: {persona["desc"]}
- 말투: {persona["voice"]}

답변 방식:
- 답변 첫 문장은 반드시 "{persona["emoji"]} {persona["name"]}:"로 시작한다.
- 실제 방송 패널이 게스트 질문을 받고 답하는 것처럼 자연스럽게 말한다.
- "좋은 질문이에요", "이건 생각보다 재밌는 지점이 있어요"처럼 구어체를 사용할 수 있다.
- 다만 너무 가볍거나 장난스럽게 흐르지 않도록 한다.
- 선택된 패널의 전문 관점이 답변의 중심이 되어야 한다.
- 필요하면 다른 분야의 맥락을 한두 문장 정도 곁들인다.
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
        padding-bottom: 240px;
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
        max-width: 640px;
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

    .soft-divider {
        width: 100%;
        height: 1px;
        background-color: #edf0f2;
        margin: 30px 0 22px 0;
    }

    /* =========================
       Persona
       ========================= */

    .persona-card {
        background-color: #ffffff;
        border: 1px solid #edf0f2;
        border-radius: 28px;
        padding: 22px 24px;
        margin: 14px 0 18px 0;
        box-shadow: 0 8px 24px rgba(25, 31, 40, 0.04);
    }

    .persona-kicker {
        font-size: 13px;
        font-weight: 700;
        color: #3182f6;
        letter-spacing: -0.02em;
        margin-bottom: 8px;
    }

    .persona-title {
        font-size: 20px;
        font-weight: 850;
        color: #191f28;
        letter-spacing: -0.04em;
        margin-bottom: 8px;
    }

    .persona-desc {
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

    /* =========================
       Streamlit Inputs
       ========================= */

    .stTextInput label,
    .stTextArea label,
    .stSelectbox label {
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
        -webkit-text-fill-color: #191f28 !important;
        font-size: 15px !important;
        padding: 0 15px !important;
        box-shadow: none !important;
    }

    .stTextInput input::placeholder {
        color: #8b95a1 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #8b95a1 !important;
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

    /* Selectbox */

    [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #e5e8eb !important;
        border-radius: 16px !important;
        min-height: 50px !important;
        box-shadow: none !important;
    }

    [data-baseweb="select"] span {
        color: #191f28 !important;
        font-size: 15px !important;
    }

    /* =========================
       Custom Chat Messages
       ========================= */

    .message-row {
        display: flex;
        width: 100%;
        margin-bottom: 16px;
    }

    .message-row.user {
        justify-content: flex-end;
    }

    .message-row.assistant {
        justify-content: flex-start;
    }

    .message-stack {
        max-width: 82%;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .message-row.user .message-stack {
        align-items: flex-end;
    }

    .message-row.assistant .message-stack {
        align-items: flex-start;
    }

    .message-label {
        font-size: 12px;
        font-weight: 800;
        color: #8b95a1;
        letter-spacing: -0.02em;
        padding: 0 4px;
    }

    .message-bubble {
        padding: 14px 16px;
        border-radius: 22px;
        font-size: 15px;
        line-height: 1.75;
        letter-spacing: -0.02em;
        word-break: keep-all;
        white-space: pre-wrap;
    }

    .message-bubble.user {
        background-color: #3182f6;
        color: #ffffff;
        border-top-right-radius: 8px;
        box-shadow: 0 6px 18px rgba(49, 130, 246, 0.22);
    }

    .message-bubble.assistant {
        background-color: #ffffff;
        color: #191f28;
        border: 1px solid #edf0f2;
        border-top-left-radius: 8px;
        box-shadow: 0 6px 18px rgba(25, 31, 40, 0.04);
    }

    /* =========================
       Fixed Bottom Chat Form
       ========================= */

    [data-testid="stForm"] {
        position: fixed !important;
        left: 50% !important;
        bottom: 22px !important;
        transform: translateX(-50%) !important;
        width: min(760px, calc(100vw - 44px)) !important;
        z-index: 9999 !important;

        border: 1px solid #e5e8eb !important;
        border-radius: 28px !important;
        padding: 16px !important;
        background-color: rgba(255, 255, 255, 0.96) !important;
        backdrop-filter: blur(18px) !important;
        -webkit-backdrop-filter: blur(18px) !important;
        box-shadow: 0 18px 48px rgba(25, 31, 40, 0.14) !important;
    }

    [data-testid="stForm"] [data-testid="stVerticalBlock"] {
        gap: 12px !important;
    }

    .guest-seat-title {
        font-size: 14px;
        font-weight: 850;
        color: #191f28;
        letter-spacing: -0.03em;
        margin-bottom: -2px;
    }

    .guest-seat-subtitle {
        font-size: 13px;
        font-weight: 600;
        color: #6b7684;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }

    [data-testid="InputInstructions"] {
        display: none !important;
    }

    [data-testid="stTextArea"] div[data-baseweb="textarea"] {
        border: 1px solid #edf0f2 !important;
        border-radius: 20px !important;
        background-color: #f9fafb !important;
        box-shadow: none !important;
        min-height: 54px !important;
    }

    [data-testid="stTextArea"] div[data-baseweb="textarea"]:focus-within {
        border-color: #3182f6 !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.12) !important;
    }

    [data-testid="stTextArea"] textarea {
        min-height: 54px !important;
        max-height: 120px !important;
        resize: none !important;
        border: none !important;
        outline: none !important;
        background-color: transparent !important;
        color: #191f28 !important;
        -webkit-text-fill-color: #191f28 !important;
        font-size: 15px !important;
        line-height: 1.55 !important;
        letter-spacing: -0.02em !important;
        padding: 14px 16px !important;
        box-shadow: none !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #8b95a1 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #8b95a1 !important;
    }

    [data-testid="stFormSubmitButton"] button {
        height: 54px !important;
        width: 100% !important;
        border-radius: 20px !important;
        border: none !important;
        background-color: #3182f6 !important;
        color: #ffffff !important;
        box-shadow: none !important;
        padding: 0 18px !important;
    }

    [data-testid="stFormSubmitButton"] button p {
        color: #ffffff !important;
        font-size: 15px !important;
        font-weight: 850 !important;
        letter-spacing: -0.02em !important;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #1b64da !important;
        color: #ffffff !important;
        border: none !important;
    }

    [data-testid="stFormSubmitButton"] button:hover p {
        color: #ffffff !important;
    }

    .bottom-safe-area {
        height: 190px;
    }

    /* Clear Button */

    .stButton button {
        border-radius: 16px !important;
        border: 1px solid #e5e8eb !important;
        background-color: #ffffff !important;
        color: #4e5968 !important;
        font-weight: 700 !important;
    }

    .stButton button p {
        color: #4e5968 !important;
    }

    .stButton button:hover {
        border-color: #3182f6 !important;
        color: #3182f6 !important;
    }

    .stButton button:hover p {
        color: #3182f6 !important;
    }

    a {
        color: #3182f6 !important;
        text-decoration: none !important;
        font-weight: 700 !important;
    }

    @media (max-width: 640px) {
        .hero-title {
            font-size: 34px;
        }

        [data-testid="stForm"] {
            width: calc(100vw - 28px) !important;
            bottom: 14px !important;
            padding: 14px !important;
        }

        .message-stack {
            max-width: 90%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 유틸 함수
# =========================
def render_message(role, content, speaker_label=None):
    safe_content = html.escape(content)

    if role == "user":
        label = speaker_label or "🎙️ 오늘의 게스트"
        st.markdown(
            f"""
            <div class="message-row user">
                <div class="message-stack">
                    <div class="message-label">{html.escape(label)}</div>
                    <div class="message-bubble user">{safe_content}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        label = speaker_label or "💬 패널석"
        st.markdown(
            f"""
            <div class="message-row assistant">
                <div class="message-stack">
                    <div class="message-label">{html.escape(label)}</div>
                    <div class="message-bubble assistant">{safe_content}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_assistant_stream(placeholder, content, speaker_label):
    safe_content = html.escape(content)
    safe_label = html.escape(speaker_label)

    placeholder.markdown(
        f"""
        <div class="message-row assistant">
            <div class="message-stack">
                <div class="message-label">{safe_label}</div>
                <div class="message-bubble assistant">{safe_content}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def get_assistant_label(persona_key):
    persona = PERSONAS[persona_key]
    if persona_key == "all":
        return "✨ 알쓸챗 패널석"
    return f'{persona["emoji"]} {persona["name"]}'

# =========================
# 상단 콘텐츠
# =========================
st.markdown(
    """
    <section class="hero">
        <div class="hero-badge">알아두면 쓸데 있는 대화</div>
        <div class="hero-title">
            오늘의 게스트처럼 묻고,<br>
            패널처럼 답변을 들어보세요
        </div>
        <div class="hero-desc">
            건축학자, 물리학자, 역사학자, 심리학자처럼 서로 다른 관점을 가진 패널에게 질문해보세요.
            사소한 궁금증도 한 테이블 위의 대화처럼 자연스럽게 풀어드립니다.
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# =========================
# 패널 선택
# =========================
persona_keys = list(PERSONAS.keys())

selected_persona_key = st.selectbox(
    "오늘 질문할 패널을 선택해주세요",
    options=persona_keys,
    format_func=lambda key: f'{PERSONAS[key]["emoji"]} {PERSONAS[key]["name"]}',
)

selected_persona = PERSONAS[selected_persona_key]

st.markdown(
    f"""
    <div class="persona-card">
        <div class="persona-kicker">오늘의 패널</div>
        <div class="persona-title">
            {selected_persona["emoji"]} {selected_persona["name"]}
        </div>
        <div class="persona-desc">
            {selected_persona["desc"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

example_html = ""
for question in selected_persona["examples"]:
    example_html += f'<div class="question-chip">{html.escape(question)}</div>'

st.markdown(
    f"""
    <div class="card">
        <div class="card-title">이런 질문을 해볼 수 있어요</div>
        <div class="card-desc">
            선택한 패널의 관점에 맞춰 질문 예시가 달라집니다.
            통합 패널을 선택하면 질문에 따라 여러 패널이 함께 답변할 수 있어요.
        </div>
        <div class="question-grid">
            {example_html}
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
# 대화 영역
# =========================
if st.session_state.messages:
    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        render_message(
            role=message["role"],
            content=message["content"],
            speaker_label=message.get("speaker_label"),
        )

# =========================
# 대화 초기화
# =========================
if st.session_state.messages:
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# =========================
# 하단 고정 입력창
# =========================
with st.form("fixed_guest_question_form", clear_on_submit=True):
    st.markdown(
        f"""
        <div class="guest-seat-title">
            🎙️ 게스트 질문석
        </div>
        <div class="guest-seat-subtitle">
            {selected_persona["emoji"]} {selected_persona["name"]}에게 궁금한 것을 물어보세요
        </div>
        """,
        unsafe_allow_html=True,
    )

    input_col, button_col = st.columns([5, 1.15])

    with input_col:
        prompt = st.text_area(
            "질문 입력",
            placeholder="예: 왜 사람들은 오래된 공간을 더 감성적으로 느낄까요?",
            label_visibility="collapsed",
            height=54,
        )

    with button_col:
        submitted = st.form_submit_button("질문")

# 입력창에 가려지지 않도록 하단 여백 확보
st.markdown('<div class="bottom-safe-area"></div>', unsafe_allow_html=True)

# =========================
# 답변 생성
# =========================
if submitted and prompt.strip():
    user_prompt = prompt.strip()
    assistant_label = get_assistant_label(selected_persona_key)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
            "speaker_label": "🎙️ 오늘의 게스트",
        }
    )

    messages_for_api = [
        {
            "role": "system",
            "content": build_system_prompt(selected_persona_key),
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
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    with chat_container:
        render_message(
            role="user",
            content=user_prompt,
            speaker_label="🎙️ 오늘의 게스트",
        )

        assistant_placeholder = st.empty()
        response = ""

        try:
            for chunk in generate_response():
                response += chunk
                render_assistant_stream(
                    placeholder=assistant_placeholder,
                    content=response,
                    speaker_label=assistant_label,
                )

        except Exception as error:
            response = (
                "답변을 생성하는 중 문제가 발생했어요. "
                "API 키, 모델명, 사용량 한도, 또는 현재 계정에서 사용할 수 있는 모델인지 확인해주세요.\n\n"
                f"오류 내용: {error}"
            )
            render_assistant_stream(
                placeholder=assistant_placeholder,
                content=response,
                speaker_label=assistant_label,
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "speaker_label": assistant_label,
        }
    )
