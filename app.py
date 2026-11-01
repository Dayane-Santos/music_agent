import streamlit as st
from dotenv import load_dotenv
from src.agent import agent_executor

load_dotenv()

st.set_page_config(page_title="Music Store Assistant", page_icon="🎵")
st.title("🎵 Music Store Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt_input := st.chat_input("Ask me anything about our music store!"):
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    with st.chat_message("user"):
        st.markdown(prompt_input)

    with st.chat_message("assistant"):
        formatted_history = [
            (msg["role"], msg["content"]) for msg in st.session_state.messages[:-1]
        ]
        response = agent_executor.invoke({
            "input": prompt_input,
            "chat_history": formatted_history
        })
        st.markdown(response["output"])
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
    