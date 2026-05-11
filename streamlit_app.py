import streamlit as st
from openai import OpenAI

# 제목과 설명을 표시합니다.
st.title("💬 챗봇")
st.write(
    "이 앱은 OpenAI의 GPT-3.5 모델을 사용해 응답을 생성하는 간단한 챗봇입니다. "
    "앱을 사용하려면 OpenAI API 키를 입력해야 하며, API 키는 [여기](https://platform.openai.com/account/api-keys)에서 발급받을 수 있습니다. "
    "이 앱을 단계별로 만드는 방법은 [Streamlit 튜토리얼](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)에서 확인할 수 있습니다."
)

# `st.text_input`을 통해 사용자에게 OpenAI API 키를 입력받습니다.
# 또는 API 키를 `./.streamlit/secrets.toml`에 저장한 뒤
# `st.secrets`를 통해 불러올 수도 있습니다.
# 자세한 내용은 https://docs.streamlit.io/develop/concepts/connections/secrets-management 를 참고하세요.
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:

    # OpenAI 클라이언트를 생성합니다.
    client = OpenAI(api_key=openai_api_key)

    # 채팅 메시지를 저장할 세션 상태 변수를 생성합니다.
    # 이렇게 하면 앱이 다시 실행되어도 이전 메시지가 유지됩니다.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 채팅 메시지를 `st.chat_message`를 통해 표시합니다.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자가 메시지를 입력할 수 있는 채팅 입력창을 생성합니다.
    # 이 입력창은 화면 하단에 자동으로 표시됩니다.
    if prompt := st.chat_input("무엇을 도와드릴까요?"):

        # 현재 입력한 메시지를 저장하고 화면에 표시합니다.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API를 사용해 응답을 생성합니다.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # `st.write_stream`을 사용해 응답을 채팅창에 실시간으로 표시한 뒤,
        # 세션 상태에 저장합니다.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
