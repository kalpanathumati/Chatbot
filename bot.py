# chatbot.py

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

# Initialize Gemini 1.5 Flash model
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Streamlit page config
st.set_page_config(page_title="Gemini Chatbot", layout="centered")

# Custom CSS styling
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

# App title
st.title("💬 Gemini AI Chatbot")

# Chat history state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text input (not inside a form now)
user_input = st.text_input("You:", key="user_input")

# Process and generate response
if user_input:
    # Append user message
    st.session_state.chat_history.append(("user", user_input))

    # Generate response from Gemini
    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    # Append bot reply
    st.session_state.chat_history.append(("bot", reply))

    # Clear the input manually
    st.session_state.user_input = ""

    # Rerun to refresh UI
    st.experimental_rerun()

# Display chat history
for sender, message in st.session_state.chat_history:
    css_class = "user" if sender == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {css_class}">{message}</div>', unsafe_allow_html=True)
