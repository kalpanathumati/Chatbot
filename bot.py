# chatbot.py

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model (use gemini-1.5-flash)
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.set_page_config(page_title="Gemini Chatbot", layout="centered")

# Apply custom CSS
st.markdown("""
    <style>
    .chat-bubble {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        display: inline-block;
        word-wrap: break-word;
    }
    .user {
        background-color: #007bff;
        color: white;
        text-align: right;
        margin-left: auto;
    }
    .bot {
        background-color: #e5e5e5;
        color: black;
        text-align: left;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💬 Gemini AI Chatbot")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("You:", key="input")

# Display chat history
for sender, message in st.session_state.chat_history:
    css_class = "user" if sender == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {css_class}">{message}</div>', unsafe_allow_html=True)

# On new input
if user_input:
    st.session_state.chat_history.append(("user", user_input))

    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    st.session_state.chat_history.append(("bot", reply))
    st.experimental_rerun()
