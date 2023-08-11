from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

st.set_page_config(page_title="Your custom assistant", page_icon="🤖")

st.subheader("Your custom chat")

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    with st.form(key="update_system_message"):
        system_message = st.text_area(label="System role")
        set_button = st.form_submit_button(label="Set")
    with st.form(key="chat", clear_on_submit=True):
        user_prompt = st.text_input(label="Send a message")
        chat_button = st.form_submit_button(label="Chat")
    if set_button and system_message:  # Reset the chat when system message changed
        st.session_state.messages = []
        st.session_state.messages.append(SystemMessage(content=system_message))
    if chat_button and user_prompt:
        st.session_state.messages.append(HumanMessage(content=user_prompt))

        with st.spinner("Working on your request"):
            # sending all the messages to the API
            response = chat(st.session_state.messages)
        # appending the response
        st.session_state.messages.append(AIMessage(content=response.content))

# st.session_state.messages
# message("this is chatgpt", is_user=False)
# message("this is me", is_user=True)

if len(st.session_state.messages) >= 1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(
            0, SystemMessage(content="You are a helpful assistant")
        )
if set_button:
    st.write("System message reset!")

for i, msg in enumerate(st.session_state.messages[1:]):
    if isinstance(msg, HumanMessage):
        message(msg.content, is_user=True, key=f"{i} + 🧔")
    else:
        message(msg.content, is_user=False, key=f"{i} + 🦾")
