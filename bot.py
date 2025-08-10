# chatbot.py

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Page config
st.set_page_config(page_title="Gemini Chatbot", layout="centered")

# CSS for message bubbles
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

# Title
st.title("💬 Gemini AI Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize submitted flag
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submitted = st.form_submit_button("Send")

if submitted:
    st.session_state.submitted = True
    st.session_state.last_input = user_input

# Handle submission
if st.session_state.get("submitted", False):
    user_input = st.session_state.get("last_input", "")
    if user_input:
        # Add user message
        st.session_state.chat_history.append(("user", user_input))

        try:
            # Generate bot response
            response = model.generate_content(user_input)
            reply = response.text
        except Exception as e:
            reply = f"❌ Error: {str(e)}"

        # Add bot message
        st.session_state.chat_history.append(("bot", reply))

    # Reset the flag
    st.session_state.submitted = False

# Display chat history
for sender, message in st.session_state.chat_history:
    css_class = "user" if sender == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {css_class}">{message}</div>', unsafe_allow_html=True)
