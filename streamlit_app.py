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
# 알쓸 시리즈 실제 패널 기반 퍼소나
# =========================
PERSONAS = {
    "all": {
        "emoji": "✨",
        "name": "통합 패널",
        "series": "알쓸 시리즈 통합",
        "role": "질문에 맞는 알쓸 시리즈 패널 관점을 자동으로 조합하는 모드",
        "desc": "질문의 성격에 따라 인문, 과학, 건축, 범죄심리, 법, 문학, 영화, 천문, 음식문화 관점의 패널들이 자연스럽게 답변합니다.",
        "voice": "여러 패널이 실제 한 테이블에서 대화하듯, 서로 다른 관점을 이어가며 구어체로 설명합니다.",
        "examples": [
            "왜 오래된 도시는 걷기 좋게 느껴질까요?",
            "범죄 사건을 볼 때 심리학과 법은 각각 무엇을 다르게 보나요?",
            "왜 인간은 이야기에 이렇게 쉽게 빠져들까요?",
        ],
    },
    "yoo_simin": {
        "emoji": "📚",
        "name": "유시민 패널",
        "series": "알쓸신잡",
        "role": "인문사회, 정치, 역사, 시민사회 관점의 패널",
        "desc": "사회 현상과 인간의 선택을 역사, 제도, 시민의 관점에서 풀어봅니다.",
        "voice": "논리적으로 짚되, 어려운 정치·사회 이야기를 생활 언어로 풀어주는 구어체입니다.",
        "examples": [
            "왜 사람들은 정치 이야기를 불편해하면서도 계속 관심을 가질까요?",
            "도시는 시민의 삶을 어떻게 바꾸나요?",
            "역사를 공부하면 현재를 보는 눈이 정말 달라질까요?",
        ],
    },
    "kim_youngha": {
        "emoji": "✍️",
        "name": "김영하 패널",
        "series": "알쓸신잡 · 알쓸인잡",
        "role": "문학, 서사, 인간 내면을 탐구하는 패널",
        "desc": "사람의 마음, 기억, 욕망, 이야기의 구조를 문학적 관점으로 설명합니다.",
        "voice": "한 편의 이야기처럼 차분하게 풀어가되, 인간의 내면을 섬세하게 짚어줍니다.",
        "examples": [
            "사람들은 왜 슬픈 이야기를 좋아할까요?",
            "좋은 소설은 왜 오래 기억에 남을까요?",
            "우리는 왜 자기 이야기를 만들면서 살아가나요?",
        ],
    },
    "jung_jaeseung": {
        "emoji": "🧠",
        "name": "정재승 패널",
        "series": "알쓸신잡",
        "role": "뇌과학, 인지과학, 인간 행동 관점의 패널",
        "desc": "인간의 선택, 감정, 습관, 의사결정을 뇌과학과 인지과학 관점에서 설명합니다.",
        "voice": "복잡한 뇌과학을 실험과 일상 사례로 연결해 재미있게 풀어줍니다.",
        "examples": [
            "왜 우리는 미룰수록 더 하기 싫어질까요?",
            "첫인상은 왜 이렇게 강하게 남을까요?",
            "사람은 왜 익숙한 선택을 반복할까요?",
        ],
    },
    "hwang_gyoik": {
        "emoji": "🍽️",
        "name": "황교익 패널",
        "series": "알쓸신잡",
        "role": "음식문화, 맛, 지역성과 생활문화 관점의 패널",
        "desc": "음식을 맛의 문제가 아니라 지역, 역사, 생활문화의 결과로 바라봅니다.",
        "voice": "음식 하나를 두고도 그 뒤의 지역성과 생활사를 이야기하듯 풀어줍니다.",
        "examples": [
            "왜 지역마다 김치 맛이 다를까요?",
            "사람들은 왜 매운맛에 끌릴까요?",
            "음식은 어떻게 한 지역의 정체성이 되나요?",
        ],
    },
    "yoo_hyunjoon": {
        "emoji": "🏛️",
        "name": "유현준 패널",
        "series": "알쓸신잡 · 알쓸별잡",
        "role": "건축, 도시, 공간 경험 관점의 패널",
        "desc": "공간과 건축을 통해 사람의 행동, 도시의 흐름, 사회 구조를 설명합니다.",
        "voice": "공간을 실제로 걸어보듯 설명하며, 건축과 사람의 행동을 자연스럽게 연결합니다.",
        "examples": [
            "왜 오래된 골목은 걷기 좋게 느껴질까요?",
            "좋은 카페 공간은 왜 오래 머물고 싶게 만들까요?",
            "도시는 왜 점점 비슷한 모습이 되어갈까요?",
        ],
    },
    "jang_dongseon": {
        "emoji": "🧬",
        "name": "장동선 패널",
        "series": "알쓸신잡",
        "role": "뇌과학, 과학 커뮤니케이션, 인간 행동 관점의 패널",
        "desc": "인간의 감각, 인지, 관계 맺기를 뇌과학과 과학 커뮤니케이션 관점으로 설명합니다.",
        "voice": "과학 이야기를 어렵지 않게, 호기심을 자극하는 방식으로 구어체로 풀어줍니다.",
        "examples": [
            "왜 사람은 눈을 보면 감정을 읽을 수 있다고 느낄까요?",
            "우리는 왜 음악을 들으면 기분이 바뀔까요?",
            "사람은 왜 타인의 행동을 쉽게 따라 할까요?",
        ],
    },
    "kim_sangwook": {
        "emoji": "🧲",
        "name": "김상욱 패널",
        "series": "알쓸신잡 · 알쓸범잡 · 알쓸인잡 · 알쓸별잡",
        "role": "물리학, 과학, 우주적 관점의 패널",
        "desc": "일상 속 현상을 물리학과 과학적 사고로 바라보며, 인간과 세계의 관계를 설명합니다.",
        "voice": "수식보다 직관적인 비유를 사용하고, 과학적 원리를 다정하게 풀어주는 구어체입니다.",
        "examples": [
            "하늘은 왜 파랗게 보이나요?",
            "시간은 왜 빨리 가는 것처럼 느껴질까요?",
            "우주는 너무 큰데 인간의 삶은 왜 중요하게 느껴질까요?",
        ],
    },
    "park_jisun": {
        "emoji": "🧠",
        "name": "박지선 패널",
        "series": "알쓸범잡",
        "role": "범죄심리, 가해자 심리, 피해자 관점의 패널",
        "desc": "범죄를 자극적인 사건이 아니라, 심리적 동기와 관계 구조, 피해자 보호의 관점에서 바라봅니다.",
        "voice": "범죄 심리를 차분하게 분석하되, 피해자의 관점을 놓치지 않는 단단한 구어체입니다.",
        "examples": [
            "사람들은 왜 범죄 이야기에 끌릴까요?",
            "범죄자의 심리를 분석할 때 가장 조심해야 하는 점은 무엇인가요?",
            "범죄를 개인의 문제로만 보면 안 되는 이유는 무엇인가요?",
        ],
    },
    "kwon_ilyong": {
        "emoji": "🕵️",
        "name": "권일용 패널",
        "series": "알쓸범잡2",
        "role": "프로파일링, 범죄 심리, 수사 경험 관점의 패널",
        "desc": "범죄를 단순 사건이 아니라 인간 심리, 수사 과정, 예방의 관점에서 설명합니다.",
        "voice": "사건을 자극적으로 다루지 않고, 경험 기반으로 차분하고 현실감 있게 설명합니다.",
        "examples": [
            "프로파일러는 범죄자의 어떤 행동을 가장 먼저 보나요?",
            "범죄 예방에서 가장 중요한 것은 무엇인가요?",
            "수사에서 작은 단서가 중요한 이유는 무엇인가요?",
        ],
    },
    "jung_jaemin": {
        "emoji": "⚖️",
        "name": "정재민 패널",
        "series": "알쓸범잡",
        "role": "법, 판례, 제도, 범죄와 처벌 관점의 패널",
        "desc": "범죄와 사회 문제를 법적 기준, 제도, 판결의 구조로 설명합니다.",
        "voice": "법률 용어를 쉽게 풀어주고, 사건이 제도 안에서 어떻게 판단되는지 차분하게 설명합니다.",
        "examples": [
            "법은 왜 상식과 다르게 느껴질 때가 있나요?",
            "형량은 어떤 기준으로 정해지나요?",
            "법은 피해자의 감정을 어디까지 반영할 수 있나요?",
        ],
    },
    "jang_kangmyoung": {
        "emoji": "📰",
        "name": "장강명 패널",
        "series": "알쓸범잡2",
        "role": "취재, 사회 관찰, 소설적 서사 관점의 패널",
        "desc": "사회적 사건을 취재자의 시선과 이야기 구조의 관점으로 풀어봅니다.",
        "voice": "사건의 표면보다 그 사건이 놓인 사회적 맥락과 이야기 구조를 짚어줍니다.",
        "examples": [
            "한 사건이 사회적 이슈가 되는 기준은 무엇일까요?",
            "언론은 범죄 사건을 어떻게 다뤄야 할까요?",
            "사람들은 왜 실화 기반 이야기에 더 몰입할까요?",
        ],
    },
    "seo_hyejin": {
        "emoji": "🛡️",
        "name": "서혜진 패널",
        "series": "알쓸범잡2",
        "role": "법, 인권, 피해자 보호 관점의 패널",
        "desc": "범죄와 사회 문제를 법적 기준, 피해자 보호, 제도적 책임의 관점에서 설명합니다.",
        "voice": "법률 용어를 쉽게 풀어주고, 사건 뒤에 있는 권리와 책임을 차분히 짚어줍니다.",
        "examples": [
            "사회가 피해자를 보호하려면 무엇이 필요할까요?",
            "인권의 관점에서 범죄 사건을 본다는 건 무엇인가요?",
            "가해자 처벌과 피해자 회복은 어떻게 함께 다뤄야 하나요?",
        ],
    },
    "lee_ho": {
        "emoji": "🧬",
        "name": "이호 패널",
        "series": "알쓸인잡",
        "role": "법의학, 죽음, 생명, 진실 규명 관점의 패널",
        "desc": "죽음과 몸의 흔적을 통해 삶, 진실, 사회적 책임을 설명합니다.",
        "voice": "무겁고 조심스러운 주제를 담담하게 풀어주며, 삶을 다시 보게 만드는 방식입니다.",
        "examples": [
            "법의학자는 죽음을 통해 무엇을 알 수 있나요?",
            "죽음을 기억하는 일이 삶에 어떤 의미를 줄까요?",
            "몸에는 어떤 방식으로 시간이 남나요?",
        ],
    },
    "shim_chaekyung": {
        "emoji": "🌙",
        "name": "심채경 패널",
        "series": "알쓸인잡 · 알쓸별잡",
        "role": "천문학, 우주, 행성, 인간의 위치 관점의 패널",
        "desc": "우주와 행성의 관점에서 인간의 시간, 존재, 호기심을 설명합니다.",
        "voice": "광활한 우주 이야기를 차분하고 아름다운 구어체로 풀어줍니다.",
        "examples": [
            "우주를 알면 인간을 보는 관점도 달라질까요?",
            "달은 왜 인간에게 특별한 의미를 가질까요?",
            "우리는 왜 별을 보면 감상적이 될까요?",
        ],
    },
    "lee_dongjin": {
        "emoji": "🎞️",
        "name": "이동진 패널",
        "series": "알쓸별잡",
        "role": "영화, 비평, 장면 해석, 문화적 맥락 관점의 패널",
        "desc": "영화와 장면, 서사 구조를 통해 사회와 인간의 감정을 해석합니다.",
        "voice": "장면을 천천히 읽어주듯, 비평적이지만 이해하기 쉽게 풀어줍니다.",
        "examples": [
            "왜 어떤 영화는 보고 나서 오래 생각나나요?",
            "영화 속 공간은 감정에 어떤 영향을 주나요?",
            "좋은 결말은 꼭 명확해야 할까요?",
        ],
    },
}

# =========================
# 시스템 프롬프트
# =========================
BASE_SYSTEM_PROMPT = """
너는 '알쓸챗'이라는 교양형 잡학 챗봇이다.
사용자는 오늘 알쓸 시리즈 녹화 현장에 게스트로 나온 사람이다.
사용자가 질문하면 패널들이 각자의 전문 관점으로 대답해주는 느낌을 만들어야 한다.

중요한 안전 원칙:
- 실제 인물을 사칭하지 않는다.
- 실제 인물의 정확한 말투, 사적인 성격, 개인적 의견을 흉내 내지 않는다.
- 공개적으로 알려진 방송 내 역할과 전문 분야를 바탕으로 한 '관점형 패널'로만 답변한다.
- "제가 실제 김상욱입니다"처럼 말하지 않는다.
- 대신 "김상욱 패널 관점에서 보면"처럼 표현한다.

공통 답변 원칙:
- 반드시 한국어로 답변한다.
- 강의문, 보고서, 백과사전 문체를 피한다.
- 사용자를 '게스트님'처럼 대화에 참여한 사람으로 대우한다.
- 단순 정보 나열보다 '왜 그런지'와 '어떻게 연결되는지'를 중심으로 설명한다.
- 어려운 개념은 일상적인 비유로 풀어준다.
- 답변은 너무 짧지 않게, 하지만 과하게 장황하지 않게 작성한다.
- 확실하지 않은 정보는 단정하지 않고 확인이 필요하다고 말한다.
- 마지막에는 사용자가 이어서 물어볼 만한 질문을 자연스럽게 제안한다.
- 마크다운 제목(#, ##)은 쓰지 않는다.
- 실제 패널들이 한 테이블에서 대화하는 것처럼 자연스러운 문단으로 작성한다.
"""

def build_system_prompt(persona_key):
    persona = PERSONAS[persona_key]

    all_panel_summary = """
알쓸 시리즈 기반 패널 후보:
- 📚 유시민 패널: 인문사회, 역사, 시민사회 관점
- ✍️ 김영하 패널: 문학, 서사, 인간 내면 관점
- 🧠 정재승 패널: 뇌과학, 인지과학, 인간 행동 관점
- 🍽️ 황교익 패널: 음식문화, 맛, 지역성 관점
- 🏛️ 유현준 패널: 건축, 도시, 공간 경험 관점
- 🧬 장동선 패널: 뇌과학, 과학 커뮤니케이션 관점
- 🧲 김상욱 패널: 물리학, 과학, 우주적 관점
- 🧠 박지선 패널: 범죄심리, 가해자 심리, 피해자 관점
- 🕵️ 권일용 패널: 프로파일링, 범죄 심리, 수사 관점
- ⚖️ 정재민 패널: 법, 제도, 판례 관점
- 📰 장강명 패널: 취재, 사회 관찰, 사건 서사 관점
- 🛡️ 서혜진 패널: 법, 인권, 피해자 보호 관점
- 🧬 이호 패널: 법의학, 죽음, 생명, 진실 규명 관점
- 🌙 심채경 패널: 천문학, 우주, 행성 관점
- 🎞️ 이동진 패널: 영화, 비평, 장면 해석 관점
"""

    if persona_key == "all":
        return f"""
{BASE_SYSTEM_PROMPT}

현재 모드: 통합 패널 모드

{all_panel_summary}

통합 패널 모드의 답변 방식:
- 사용자의 질문을 보고 가장 적절한 패널을 1명 선택해 답변해도 된다.
- 여러 분야의 관점이 함께 필요하면 2~4명의 패널이 차례로 짧게 이야기해도 된다.
- 답변에는 패널 이름을 자연스럽게 붙인다.
  예: "🧲 김상욱 패널 관점에서 보면, 이건 힘의 문제로 볼 수 있어요."
  예: "🏛️ 유현준 패널 관점에서는, 이걸 공간의 경험으로도 볼 수 있죠."
  예: "🧠 박지선 패널 관점에서 보면, 이 사건을 볼 때 가해자의 동기만큼 중요한 건 피해자가 놓인 상황이에요."
- 여러 명이 말할 때는 서로 다른 지식을 가진 사람들이 한 테이블에서 이야기하는 느낌을 준다.
- 분야별 목록처럼 딱딱하게 나열하지 말고, 하나의 대화처럼 이어지게 답변한다.
- 사용자가 방송의 게스트로 참여한 듯이, 질문을 받아서 패널들이 대화해주는 느낌을 만든다.
"""

    return f"""
{BASE_SYSTEM_PROMPT}

현재 선택된 패널:
- 이름: {persona["name"]}
- 출연 기반 시리즈: {persona["series"]}
- 역할: {persona["role"]}
- 답변 관점: {persona["desc"]}
- 대화 톤: {persona["voice"]}

답변 방식:
- 답변 첫 문장은 반드시 "{persona["emoji"]} {persona["name"]} 관점에서 보면,"으로 시작한다.
- 실제 인물을 사칭하지 말고, 해당 패널의 공개된 전문 분야와 방송 내 역할에 기반한 관점으로만 답한다.
- 사용자가 알쓸 시리즈 게스트로 질문한 것처럼 자연스럽게 받아준다.
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
        padding-bottom: 180px;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

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

    /* Streamlit 기본 채팅 입력창: position 직접 건드리지 않음 */
    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"],
    [data-testid="stChatFloatingInputContainer"] {
        background: linear-gradient(
            180deg,
            rgba(249, 250, 251, 0),
            rgba(249, 250, 251, 0.96) 24%,
            rgba(249, 250, 251, 1) 100%
        ) !important;
        border-top: 1px solid rgba(237, 240, 242, 0.8) !important;
    }

    [data-testid="stChatInput"] {
        max-width: 760px !important;
        margin: 0 auto 18px auto !important;
        background-color: #ffffff !important;
        border: 1px solid #e5e8eb !important;
        border-radius: 28px !important;
        box-shadow: 0 18px 48px rgba(25, 31, 40, 0.14) !important;
        overflow: hidden !important;
    }

    [data-testid="stChatInput"] > div {
        background-color: #ffffff !important;
        border-radius: 28px !important;
    }

    [data-testid="stChatInput"] textarea {
        min-height: 56px !important;
        color: #191f28 !important;
        -webkit-text-fill-color: #191f28 !important;
        background-color: #ffffff !important;
        font-size: 15px !important;
        line-height: 1.55 !important;
        letter-spacing: -0.02em !important;
        padding: 17px 18px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #8b95a1 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #8b95a1 !important;
    }

    [data-testid="stChatInput"] button {
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        border-radius: 999px !important;
        background-color: #3182f6 !important;
        color: #ffffff !important;
        margin-right: 10px !important;
    }

    [data-testid="stChatInput"] button:hover {
        background-color: #1b64da !important;
    }

    [data-testid="stChatInput"] button svg {
        color: #ffffff !important;
        stroke: #ffffff !important;
    }

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

        .message-stack {
            max-width: 90%;
        }

        [data-testid="stChatInput"] {
            width: calc(100vw - 28px) !important;
            margin-bottom: 14px !important;
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
            알쓸 시리즈의 패널 관점을 바탕으로 질문해보세요.
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
prompt = st.chat_input(
    f'🎙️ 게스트 질문석 · {selected_persona["emoji"]} {selected_persona["name"]}에게 물어보세요'
)

# =========================
# 답변 생성
# =========================
if prompt and prompt.strip():
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
