import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🎭 시 짓기 챗봇")
st.write(
    "이 챗봇은 OpenAI의 GPT-3.5 모델을 사용하여 아름다운 시를 창작합니다. "
    "주제나 감정, 키워드를 입력하시면 맞춤형 시를 지어드려요! "
    "OpenAI API 키가 필요하며, [여기](https://platform.openai.com/account/api-keys)에서 받으실 수 있습니다."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("OpenAI API 키를 입력해주세요! 🗝️", icon="🔑")
else:
    # Create an OpenAI client.
    try:
        client = OpenAI(api_key=openai_api_key)
        
        # Create a session state variable to store the chat messages.
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display the existing chat messages via `st.chat_message`.
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Create a chat input field with poetry-specific placeholder
        if prompt := st.chat_input("어떤 시를 지어드릴까요? (예: 봄날의 사랑, 외로운 밤, 희망 등)"):
            # Store and display the current prompt.
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate a response using the OpenAI API with poetry-specific system prompt
            try:
                stream = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": """당신은 전문적인 시인입니다. 사용자의 요청에 따라 아름답고 감동적인 한국어 시를 창작해주세요. 
                        다음 규칙을 따라주세요:
                        1. 시는 자연스럽고 아름다운 한국어로 작성
                        2. 사용자가 제시한 주제나 감정을 중심으로 창작
                        3. 운율이나 리듬감을 고려하여 작성
                        4. 4-8줄 정도의 적당한 길이
                        5. 시 제목도 함께 제공
                        6. 시 아래에 간단한 설명이나 영감을 덧붙일 수 있음"""},
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                    temperature=0.8,  # 창의성을 위해 온도 조정
                )
                
                # Stream the response to the chat using `st.write_stream`
                with st.chat_message("assistant"):
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {str(e)}")
                st.info("API 키가 올바른지 확인해주세요. 또는 잠시 후 다시 시도해주세요.")
                
    except Exception as e:
        st.error(f"OpenAI 클라이언트 초기화 중 오류가 발생했습니다: {str(e)}")
        st.info("API 키가 올바른지 확인해주세요.")

# 사이드바에 사용 팁 추가
with st.sidebar:
    st.header("💡 시 창작 팁")
    st.markdown("""
    **좋은 시를 위한 입력 예시:**
    - "봄날의 첫사랑"
    - "비 오는 날의 그리움"
    - "고향에 대한 그리움"
    - "희망과 용기"
    - "어머니의 사랑"
    
    **더 구체적으로 요청하세요:**
    - "자유시로 써주세요"
    - "7언 절구로 써주세요"
    - "슬픈 감정의 시"
    - "희망적인 메시지가 담긴 시"
    """)
    
    st.header("🎨 최근 인기 주제")
    popular_topics = ["계절", "사랑", "이별", "가족", "꿈", "자연", "우정", "성장"]
    for topic in popular_topics:
        if st.button(topic, key=f"topic_{topic}"):
            st.session_state.suggested_topic = topic
