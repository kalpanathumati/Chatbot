# chatbot.py

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env and set API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Initialize Gemini 1.5 Flash
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Streamlit config
st.set_page_config(page_title="Gemini Chatbot", layout="centered")

# CSS
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

# Message input workaround
input_key = "input_" + str(len(st.session_state.chat_history))  # unique key for each turn
user_input = st.text_input("You:", key=input_key)

# Process user input
if user_input:
    # Add user message
    st.session_state.chat_history.append(("user", user_input))

    # Generate response
    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    # Add bot message
    st.session_state.chat_history.append(("bot", reply))

    # Rerun to show latest chat and reset input
    st.experimental_rerun()

# Display chat history
for sender, message in st.session_state.chat_history:
    css_class = "user" if sender == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {css_class}">{message}</div>', unsafe_allow_html=True)
