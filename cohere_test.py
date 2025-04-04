import streamlit as st
import cohere
import os

COHERE_API_KEY = os.getenv("COHERE_API_KEY") or "7c39Dgzhn9mVBheHP54ThEMdU2bN3TW9qYSc5E2O"
co = cohere.Client(COHERE_API_KEY)

st.set_page_config(page_title="Cohere Chat", layout="centered")
st.title("💬 Cohere LLM Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

prompt = st.text_input("You:", "")

def format_chat_history(history):
    mapped = []
    for role, msg in history:
        if role == "You":
            mapped.append({"role": "USER", "message": msg})
        elif role == "Bot":
            mapped.append({"role": "CHATBOT", "message": msg})
    return mapped

if st.button("Send") and prompt:
    st.session_state.chat_history.append(("You", prompt))

    response = co.chat(
        model="command-r",
        message=prompt,
        chat_history=format_chat_history(st.session_state.chat_history[:-1])
    )

    bot_reply = response.text.strip()
    st.session_state.chat_history.append(("Bot", bot_reply))

st.markdown("### Conversation:")
for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:** {msg}")
