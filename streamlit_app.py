import streamlit as st
from app.agent import ask_agent
import requests
from helpers.helper_functions import escape_dollars

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="SupportPilot AI", page_icon="🤖")
st.title("🤖 SupportPilot AI")
st.caption("AI-powered customer support — ask about orders, products, or policies")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(escape_dollars(msg["content"]))

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask_agent(user_input)
            st.write(escape_dollars(result["response"]))
            # try:
            #     payload = {"message":user_input}
            #     response =requests.post(f"{API_URL}/chat",json=payload)

            #     if response.status_code == 200:
            #         answer = response.json()["response"]
            #         st.write(escape_dollars(answer))

            #         st.session_state.messages.append({
            #                     "role": "assistant",
            #                     "content": answer,
            #                     "handoff": response.json()["handoff"]
            #                 })
            #     else:
            #         st.error(response.json().get("detail","Something went wrong."))

            # except requests.exceptions.ConnectionError:
            #     st.error("Could not connect to the FastAPI server.")
        
        st.session_state.messages.append({
        "role": "assistant",
        "content": result["response"],
        "handoff": result["handoff"]
        })



        