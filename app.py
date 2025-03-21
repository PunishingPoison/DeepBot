import streamlit as st
import requests

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="WSP ChatBot", layout="wide", page_icon="🤖")
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #FFFFFF;
    }
    .stApp {
        background-color: #1e1e1e;
        color: #FFFFFF;
    }

    /* Chat Styling */
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }
    .chat-message {
        display: flex;
        align-items: flex-start;
        margin: 10px 0;
    }
    .chat-message.user {
        justify-content: flex-end;
        text-align: right;
    }
    .chat-message.ai {
        justify-content: flex-start;
        text-align: left;
    }
    .message-bubble {
        max-width: 70%;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
    .message-bubble.user {
        background-color: #0d47a1;
        color: white;
        border: 1px solid #1565c0;
    }
    .message-bubble.ai {
        background-color: #2e2e2e;
        color: #f1f1f1;
        border: 1px solid #444;
    }
    .message-name {
        font-size: 12px;
        color: #aaa;
        margin-bottom: 3px;
    }

    /* Textarea + Label */
    textarea {
        background-color: #2b2b2b !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    label, .stTextArea label {
        color: white !important;
    }
    textarea::placeholder {
        color: #cccccc !important;
    }

    /* Button Styling */
    button[kind="primary"] {
        background-color: #333333 !important;
        color: black !important;
        border: none !important;
    }
    button[kind="primary"]:hover {
        background-color: #444444 !important;
        color: black !important;
    }

    /* --- Dark Code Block Styling --- */
    pre, code {
        background-color: #000000 !important;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 12px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 14px;
        overflow-x: auto;
    }

    /* Optional scrollbar styling for code blocks */
    pre::-webkit-scrollbar {
        height: 6px;
    }
    pre::-webkit-scrollbar-thumb {
        background: #444;
        border-radius: 4px;
    }
    button[title="Copy to clipboard"] {
    filter: invert(1); /* makes it white */
    background-color: transparent !important;
    border: none !important;
    }
    button[title="Copy to clipboard"]:hover {
    filter: invert(1) brightness(1.2);
    cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Session Setup ----------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown('<div class="header"><h2>🤖 WSP ChatBot (OpenRouter)</h2></div>', unsafe_allow_html=True)

# ---------------- Chat Container ----------------
chat_container = st.container()
with chat_container:
    for msg in st.session_state["messages"]:
        role = msg["role"]
        content = msg["content"]
        name = "Me" if role == "user" else "WSP Bot"
        align = "user" if role == "user" else "ai"
        st.markdown(
            f"""
            <div class="chat-message {align}">
                <div>
                    <div class="message-name">{name}</div>
                    <div class="message-bubble {align}">{content}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------- User Input ----------------
with st.form("user_input_form", clear_on_submit=True):
    user_input = st.text_area("Your message:", key="user_input", placeholder="Type your message here...", height=100)
    submit_button = st.form_submit_button("Send")

# ---------------- OpenRouter API ----------------
if submit_button and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Show user's message + placeholder for bot response
    with chat_container:
        st.markdown(
            f"""
            <div class="chat-message user">
                <div>
                    <div class="message-name">Me</div>
                    <div class="message-bubble user">{user_input}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        placeholder = st.empty()
        placeholder.markdown(
            """
            <div class="chat-message ai">
                <div>
                    <div class="message-name">WSP Bot</div>
                    <div class="message-bubble ai">WSP Bot is typing...</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "HTTP-Referer": "https://www.sitename.com",
                "X-Title": "SiteName",
                "Content-Type": "application/json",
            },
            json={
                "model": "nvidia/llama-3.1-nemotron-70b-instruct:free",
                "messages": st.session_state["messages"]
            },
        )
        data = response.json()
        bot_message = data["choices"][0]["message"]["content"]
    except Exception as e:
        bot_message = f"Error: {str(e)}"

    # Show actual bot response
    placeholder.empty()
    with chat_container:
        st.markdown(
            f"""
            <div class="chat-message ai">
                <div>
                    <div class="message-name">WSP Bot</div>
                    <div class="message-bubble ai">{bot_message}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Save bot reply
    st.session_state["messages"].append({"role": "assistant", "content": bot_message})
