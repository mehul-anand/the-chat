import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'gemini_history' not in st.session_state:
    st.session_state.gemini_history = []

# Initialize Gemini model and chat
if 'model' not in st.session_state:
    st.session_state.model = genai.GenerativeModel('gemini-2.0-flash')
    st.session_state.chat = st.session_state.model.start_chat(
        history=st.session_state.gemini_history
    )

st.title('Temporary Chat')

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar')
    ):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('Your message here...'):
    # Display user message
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to session state
    st.session_state.messages.append(
        dict(role='user', content=prompt)
    )

    # Send message to AI
    response = st.session_state.chat.send_message(
        prompt,
        stream=True
    )

    # Display assistant response
    with st.chat_message(
        name=MODEL_ROLE,
        avatar=AI_AVATAR_ICON
    ):
        message_placeholder = st.empty()
        full_response = ''
        for chunk in response:
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                message_placeholder.write(full_response + '▌')
        message_placeholder.markdown(full_response)

    # Add assistant response to session state
    st.session_state.messages.append(
        dict(
            role=MODEL_ROLE,
            content=st.session_state.chat.history[-1].parts[0].text,
            avatar=AI_AVATAR_ICON
        )
    )
    st.session_state.gemini_history = st.session_state.chat.history