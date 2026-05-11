st.markdown(
    """
    <style>
    /* =========================
       Bottom Chat Area Fix
       ========================= */

    /* 하단 고정 영역의 검은 배경 제거 */
    [data-testid="stBottomBlockContainer"],
    [data-testid="stChatFloatingInputContainer"],
    .stChatFloatingInputContainer {
        background-color: #f9fafb !important;
        border-top: 1px solid #edf0f2 !important;
        box-shadow: 0 -8px 24px rgba(25, 31, 40, 0.04) !important;
        padding: 18px 0 24px 0 !important;
    }

    /* 하단 영역 내부 정렬 */
    [data-testid="stBottomBlockContainer"] > div,
    [data-testid="stChatFloatingInputContainer"] > div,
    .stChatFloatingInputContainer > div {
        max-width: 760px !important;
        margin: 0 auto !important;
        padding-left: 24px !important;
        padding-right: 24px !important;
        background: transparent !important;
    }

    /* 채팅 입력창 전체 */
    [data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e8eb !important;
        border-radius: 24px !important;
        box-shadow: 0 10px 28px rgba(25, 31, 40, 0.08) !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    /* 채팅 입력창 내부 래퍼 */
    [data-testid="stChatInput"] > div {
        background-color: #ffffff !important;
        border-radius: 24px !important;
    }

    /* 텍스트 입력 영역 */
    [data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #191f28 !important;
        font-size: 15px !important;
        letter-spacing: -0.02em !important;
        padding: 16px 18px !important;
        min-height: 52px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #8b95a1 !important;
    }

    /* 전송 버튼 */
    [data-testid="stChatInput"] button {
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
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
        fill: none !important;
        stroke: #ffffff !important;
    }

    /* focus 상태 */
    [data-testid="stChatInput"]:focus-within {
        border-color: #3182f6 !important;
        box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.12),
                    0 10px 28px rgba(25, 31, 40, 0.08) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
