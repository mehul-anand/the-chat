import streamlit as st
import google.generativeai as genai
import time
from streamlit.components.v1 import html

# --------------------------------------------------------
#styling start
# wide layout config
# st.set_page_config(
#     layout="wide",
# )

# footer styling
html("""
<script>
window.top.document.querySelectorAll('[href*="streamlit.io"]').forEach(e => e.setAttribute("style", "display: none;"));
</script>
""")

# main block padding
st.markdown(
    body="""
        <style>
            .block-container{
                    padding-top: 0px;
                }
        </style>
    """, 
    unsafe_allow_html=True
)

# fixing the header

header = st.container()
header.title("AI Chat")
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)
st.markdown(
    """
<style>
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
        position: sticky;
        top: 2.875rem;
        background-color: #111111;
        z-index: 999;
    }
    .fixed-header {
        border-bottom: 1px solid #846eee;
    }
</>
    """,
    unsafe_allow_html=True
)

# main block content and styling

with st.container():
    st.markdown("""
    <style>
    #main-div {
        top: 1.5rem;
        background-color:#111111;
    }

    @media (min-width: 768px) {
        #main-div {
            top: 4rem;
        }
    }
                
    h1{
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(90deg, #846eee, fuchsia);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;  
    }
    </style>
    <div id="main-div">
        <p class="desc">
            Your one stop app to discuss complex and fun topics with AI
        </p> 
        <p class="desc">
            More detailed and structured prompt = better outputs
        </p> 
        <p class="desc">
            Be responsible with your AI use and have fun exploring the wonders of technology 🤠
        </p> 
    </div>
""", unsafe_allow_html=True)
    
# styling end
# --------------------------------------------------------

# configure the google API
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '🤖'

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

    # --------------------------------------------------------
    # TODO : add this chat functionality
    # chat(st.session_state.messages.append(
    #     dict(role='user', content=prompt)
    # ),is_user=True)
    # --------------------------------------------------------

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
    # Clear Chat Button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.gemini_history = []
    st.session_state.chat = st.session_state.model.start_chat (history=[])
    st.rerun()  # Refresh the app
    st.session_state.gemini_history = st.session_state.chat.history
    

# --------------------------------------------------------
# custom footer start
    
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 12px;        
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 0.9rem;
        color: #888;
        z-index: 100;        
        font-size:1em;
        color:white;
    }
    .footer a {
        text-decoration:none;
        # background: linear-gradient(90deg, #846eee, fuchsia);
        # -webkit-background-clip: text;
        # -webkit-text-fill-color: transparent;
    }
    </style>

    <div class="footer">
        Made with ❤️ by <a href="https://mehul.xyz" target="_blank">Mehul Anand</a>

    </div>
    """,
    unsafe_allow_html=True,
)

# custom footer end
# --------------------------------------------------------