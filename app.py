import streamlit as st
import requests

st.set_page_config(page_title="WSP ChatBot", layout="wide", initial_sidebar_state="collapsed")

# Apply custom dark mode styling
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #FFFFFF;
        }
        .chat-container {
            max-height: 75vh;
            overflow-y: auto;
            padding: 1rem;
            border-radius: 10px;
            background-color: #1e1e1e;
            margin-bottom: 70px;
        }
        .message.user {
            color: #00FFB3;
            font-weight: bold;
        }
        .message.bot {
            color: #FFFFFF;
            background-color: #2a2a2a;
            padding: 0.5rem;
            border-radius: 10px;
        }
        .fixed-input {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #121212;
            padding: 1rem;
            border-top: 1px solid #333;
        }
        input[type="text"] {
            width: 80%;
            padding: 10px;
            border: none;
            border-radius: 10px;
        }
        button {
            padding: 10px 20px;
            background-color: #00FFB3;
            border: none;
            border-radius: 10px;
            color: black;
            font-weight: bold;
            margin-left: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:white;'>🤖 WSP ChatBot</h2>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(f"<div class='message {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input area fixed at the bottom
with st.container():
    st.markdown('<div class="fixed-input">', unsafe_allow_html=True)
    user_input = st.text_input("You:", value="", key="input", label_visibility="collapsed", placeholder="Type your message and hit Enter")
    st.markdown('</div>', unsafe_allow_html=True)

# Send request
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
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
                "messages": [{"role": "user", "content": user_input}],
            }
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            res_data = res.json()
            bot_reply = res_data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
        except Exception as e:
            bot_reply = f"Error: {e}"

        st.session_state.messages.append({"role": "bot", "content": bot_reply})
        st.experimental_rerun()
