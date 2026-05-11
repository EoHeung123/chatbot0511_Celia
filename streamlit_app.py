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

MODEL = "gpt-4o-mini"

# =========================
# 패널 페르소나
# =========================
PERSONAS = {
    "all": {
        "emoji": "✨",
        "name": "통합 패널",
        "role": "여러 분야의 관점을 엮어 설명하는 교양 패널",
        "desc": "질문에 따라 역사, 과학, 문화, 사회적 맥락을 함께 엮어 균형 있게 답변합니다.",
        "tone": "여러 패널이 함께 대화하듯, 핵심 관점을 나누어 설명한다.",
        "examples": [
            "왜 사람들은 커피를 마시면 집중이 잘 된다고 느낄까요?",
            "왜 어떤 노래는 계속 머릿속에서 반복될까요?",
            "인간은 왜 쓸데없는 이야기에 끌릴까요?",
        ],
    },
    "architect": {
        "emoji": "🏛️",
        "name": "건축학자",
        "role": "공간, 도시, 건축, 생활환경의 관점으로 설명하는 건축학자",
        "desc": "공간 구조, 도시의 흐름, 건축 양식, 사람이 공간을 사용하는 방식을 중심으로 답변합니다.",
        "tone": "공간과 구조를 중심으로, 일상적인 장소 경험과 연결해 설명한다.",
        "examples": [
            "왜 오래된 골목은 걷기 좋게 느껴질까요?",
            "좋은 카페 공간은 왜 편안하게 느껴질까요?",
            "도시는 왜 점점 비슷한 모습이 되어갈까요?",
        ],
    },
    "physicist": {
        "emoji": "🧲",
        "name": "물리학자",
        "role": "자연현상, 에너지, 시간, 빛, 소리의 원리를 설명하는 물리학자",
        "desc": "일상 속 현상을 물리 법칙과 원리로 쉽게 풀어 설명합니다.",
        "tone": "어려운 수식보다는 직관적인 비유를 사용해 원리를 설명한다.",
        "examples": [
            "하늘은 왜 파랗게 보이나요?",
            "전자레인지는 음식을 어떻게 데우나요?",
            "왜 엘리베이터가 출발할 때 몸이 무겁게 느껴질까요?",
        ],
    },
    "historian": {
        "emoji": "📜",
        "name": "역사학자",
        "role": "사건의 배경, 시대 흐름, 문화적 맥락을 설명하는 역사학자",
        "desc": "지금의 현상이 과거의 어떤 흐름에서 왔는지 맥락 중심으로 답변합니다.",
        "tone": "연도 나열보다 시대의 변화와 사람들의 선택을 중심으로 설명한다.",
        "examples": [
            "고대 사람들은 시간을 어떻게 측정했을까요?",
            "커피는 어떻게 전 세계로 퍼졌을까요?",
            "왜 어떤 도시는 역사적으로 더 빨리 발전했을까요?",
        ],
    },
    "psychologist": {
        "emoji": "🧠",
        "name": "심리학자",
        "role": "인간의 감정, 기억, 행동, 선택을 설명하는 심리학자",
        "desc": "사람이 왜 그렇게 느끼고 행동하는지 심리와 인지 관점에서 답변합니다.",
        "tone": "사용자가 자신의 경험과 연결해 이해할 수 있도록 부드럽게 설명한다.",
        "examples": [
            "왜 사람은 미룰수록 더 하기 싫어질까요?",
            "왜 어떤 말은 오래 기억에 남을까요?",
            "왜 우리는 익숙한 것을 더 안전하다고 느낄까요?",
        ],
    },
    "sociologist": {
        "emoji": "🌐",
        "name": "사회학자",
        "role": "사회 구조, 관계, 문화, 트렌드의 관점으로 설명하는 사회학자",
        "desc": "개인의 선택처럼 보이는 현상을 사회적 구조와 문화 흐름으로 풀어 설명합니다.",
        "tone": "개인 문제가 아니라 사회적 조건과 연결해 넓은 시야로 설명한다.",
        "examples": [
            "왜 요즘 사람들은 혼자 있는 시간을 더 중요하게 생각할까요?",
            "유행은 어떻게 만들어질까요?",
            "왜 특정 세대는 일과 삶의 균형을 더 중요하게 볼까요?",
        ],
    },
    "food_researcher": {
        "emoji": "🍚",
        "name": "음식문화 연구자",
        "role": "음식, 발효, 식문화, 생활사의 관점으로 설명하는 음식문화 연구자",
        "desc": "음식의 과학적 원리와 문화적 의미를 함께 설명합니다.",
        "tone": "맛, 생활, 문화, 과학을 함께 엮어 친근하게 설명한다.",
        "examples": [
            "김치가 발효되면 몸에 좋은 이유는 무엇인가요?",
            "왜 국물 음식은 위로가 된다고 느낄까요?",
            "사람들은 왜 매운맛을 좋아할까요?",
        ],
    },
    "economist": {
        "emoji": "📈",
        "name": "경제학자",
        "role": "선택, 비용, 시장, 소비 행동의 관점으로 설명하는 경제학자",
        "desc": "사람들의 선택과 사회 현상을 비용, 효용, 인센티브 관점에서 설명합니다.",
        "tone": "딱딱한 경제 이론보다 일상의 선택 구조를 중심으로 설명한다.",
        "examples": [
            "왜 사람들은 한정판에 더 끌릴까요?",
            "구독 서비스는 왜 이렇게 많아졌을까요?",
            "가격이 비싸면 왜 더 좋아 보일 때가 있을까요?",
        ],
    },
}

# =========================
# 공통 시스템 프롬프트
# =========================
BASE_SYSTEM_PROMPT = """
너는 '알쓸챗'이라는 교양형 잡학 챗봇이다.
사용자가 사소한 궁금증을 물어보면, 알쓸신잡 패널처럼 지적이지만 어렵지 않게 설명한다.

공통 답변 원칙:
- 한국어로 답변한다.
- 단순한 정보 나열보다 '왜 그런지'를 중심으로 설명한다.
- 어려운 개념은 일상적인 비유로 쉽게 풀어준다.
- 너무 장황하지 않게, 하지만 맥락은 충분히 제공한다.
- 확실하지 않은 내용은 단정하지 않고 확인이 필요하다고 말한다.
- 마지막에는 사용자가 이어서 물어볼 만한 질문을 한 문장으로 제안한다.
"""

def build_system_prompt(persona_key):
    persona = PERSONAS[persona_key]

    return f"""
{BASE_SYSTEM_PROMPT}

오늘 사용자가 선택한 패널:
- 이름: {persona["name"]}
- 역할: {persona["role"]}
- 답변 관점: {persona["desc"]}
- 말투/전개 방식: {persona["tone"]}

답변 형식:
1. 먼저 질문의 핵심을 한두 문장으로 짚는다.
2. 선택된 패널의 관점으로 원리나 배경을 설명한다.
3. 필요하다면 다른 분야의 맥락도 짧게 연결한다.
4. 마지막에 이어서 궁금해할 만한 질문을 하나 제안한다.
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
       Inputs
       ========================= */

    .stTextInput label,
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
       Custom Chat Messages
       ========================= */

    .message-row {
        display: flex;
        width: 100%;
        margin-bottom: 14px;
    }

    .message-row.user {
        justify-content: flex-end;
    }

    .message-row.assistant {
        justify-content: flex-start;
    }

    .message-bubble {
        max-width: 78%;
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
       Custom Chat Input
       ========================= */

    [data-testid="stForm"] {
        border: 1px solid #e5e8eb !important;
        border-radius: 28px !important;
        padding: 16px !important;
        background-color: #ffffff !important;
        box-shadow: 0 12px 36px rgba(25, 31, 40, 0.08) !important;
        margin-top: 24px !important;
    }

    [data-testid="stForm"] div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    .chat-input-title {
        font-size: 14px;
        font-weight: 800;
        color: #4e5968;
        letter-spacing: -0.02em;
        margin-bottom: 12px;
    }

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

    div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
        background-color: #1b64da !important;
        color: #ffffff !important;
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
# 유틸 함수
# =========================
def render_message(role, content):
    safe_content = html.escape(content)

    if role == "user":
        st.markdown(
            f"""
            <div class="message-row user">
                <div class="message-bubble user">{safe_content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="message-row assistant">
                <div class="message-bubble assistant">{safe_content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_assistant_stream(placeholder, content):
    safe_content = html.escape(content)

    placeholder.markdown(
        f"""
        <div class="message-row assistant">
            <div class="message-bubble assistant">{safe_content}</div>
        </div>
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
            답변은 패널처럼 흥미롭게
        </div>
        <div class="hero-desc">
            건축학자, 물리학자, 역사학자, 심리학자처럼
            서로 다른 관점을 가진 패널에게 질문해보세요.
            사소한 궁금증도 맥락 있는 이야기로 풀어드립니다.
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
# 기존 메시지 출력
# =========================
if st.session_state.messages:
    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

for message in st.session_state.messages:
    render_message(message["role"], message["content"])

# =========================
# 질문 입력
# =========================
with st.form("chat_form", clear_on_submit=True):
    st.markdown(
        f"""
        <div class="chat-input-title">
            {selected_persona["emoji"]} {selected_persona["name"]}에게 물어보기
        </div>
        """,
        unsafe_allow_html=True,
    )

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

    render_message("user", user_prompt)

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

    assistant_placeholder = st.empty()
    response = ""

    try:
        for chunk in generate_response():
            response += chunk
            render_assistant_stream(assistant_placeholder, response)

    except Exception as error:
        response = (
            "답변을 생성하는 중 문제가 발생했어요. "
            "API 키, 모델명, 사용량 한도를 확인해주세요.\n\n"
            f"오류 내용: {error}"
        )
        render_assistant_stream(assistant_placeholder, response)

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
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()
