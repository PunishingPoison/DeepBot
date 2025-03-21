import streamlit as st
import requests
from markdown import markdown
from streamlit_chat import message

# ---------------- Streamlit Page Config ----------------
st.set_page_config(page_title="WSP ChatBot", layout="wide")
st.markdown("""
    <style>
        html, body {
            background-color: #121212;
            color: #FFFFFF;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 6rem;
        }
        .stTextInput > div > div > input {
            background-color: #1e1e1e;
            color: white;
        }
        .stTextInput > div {
            border: 1px solid #333;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #00FFB3;
            color: black;
            font-weight: bold;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:white;'>🤖 WSP ChatBot</h2>", unsafe_allow_html=True)

# ---------------- Session Setup ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Chat History ----------------
for msg in st.session_state.messages:
    message(msg["content"], is_user=(msg["role"] == "user"))

# ---------------- User Input ----------------
with st.form("chat_input", clear_on_submit=True):
    user_input = st.text_input("Type your message...", placeholder="Ask anything...", label_visibility="collapsed")
    submit = st.form_submit_button("Send")

# ---------------- Send & Respond ----------------
if submit and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display loading message
    with st.spinner("Thinking..."):
        try:
            headers = {
                "Authorization": "Bearer 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",
                "HTTP-Referer": "https://www.sitename.com",
                "X-Title": "SiteName",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "deepseek/deepseek-r1:free",
                "messages": st.session_state.messages,
            }

            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            res_data = res.json()
            bot_reply = res_data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")

        except Exception as e:
            bot_reply = f"Error: {str(e)}"

    # Add bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    message(bot_reply, is_user=False)
