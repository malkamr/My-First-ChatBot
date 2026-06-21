import streamlit as st
import requests

# 🔑 API KEY — Paste your OpenRouter API key here
# Get it from: https://openrouter.ai/keys
# It looks like: sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

import os
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# 🤖 MODEL — Choose any free model from OpenRouter.
# Browse free models at: https://openrouter.ai/models?q=free
# Some good free options:
#   "mistralai/mistral-7b-instruct:free"
#   "meta-llama/llama-3.1-8b-instruct:free"
#   "google/gemma-2-9b-it:free"
MODEL = "cohere/north-mini-code:free"

# SYSTEM PROMPT — Controls how the AI assistant behaves.
# Customize this to change the bot's personality or focus.
SYSTEM_PROMPT = """You are a smart study assistant named StudyMate. Your job is to help students with:
- Creating effective study schedules
- Planning for exams
- Managing time efficiently
- Providing useful study tips

Reply in the same language used in the user's latest message.
If the user writes in English, reply only in English.
If the user writes in Arabic, reply only in Arabic.

Never switch languages unless the user does, in a friendly and encouraging manner.
Provide practical and clear plans. Use emojis moderately to make the conversation more lively."""


def get_ai_response(messages: list) -> str:
    """
    Sends the conversation history to OpenRouter and returns the reply.

    Args:
        messages: List of {"role": "user"/"assistant", "content": "..."} dicts

    Returns:
        The assistant's reply as a plain string.
    """
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
                "max_tokens": 1024,
            },
            timeout=30,
        )



        # Check for HTTP errors (401 = bad key, 429 = rate limit, etc.)
        if response.status_code == 401:
            return "you have an invalid API key. Please check your OpenRouter API key."
        elif response.status_code == 429:
            return "you have exceeded your API rate limit. Please wait and try again later."
        elif response.status_code != 200:
            return f"⚠️ Server Error: {response.status_code} — {response.text}"

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "⚠️ Connection timeout. Please check your internet connection and try again."
    except Exception as e:
        return f"⚠️ An unexpected error occurred: {str(e)}"


# ──────────────────────────────────────────────
# Streamlit UI
# ──────────────────────────────────────────────

st.title("🎓 StudyMate AI")
st.caption("Your smart study assistant. Ask questions in Arabic or English!")

# Initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the full chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input box
user_input = st.chat_input("what's on your mind? Ask me anything about studying, exams, or time management!")

if user_input:
    # Show the user's message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # Append to history BEFORE calling the API so the model has full context
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenRouter with the full conversation history
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            reply = get_ai_response(st.session_state.messages)
        st.write(reply)

    # Save the assistant's reply to history
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Reset button
if st.button("🔄 Reset Conversation"):
    st.session_state.messages = []
    st.rerun()