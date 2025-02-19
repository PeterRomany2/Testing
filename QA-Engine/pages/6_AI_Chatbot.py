import os
import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

# Streamlit page configuration
st.set_page_config(
    page_title="AI Chatbot",
    layout="centered"
)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("You need to log in to access this page.")
    st.stop()  # Stop further execution of the page
    
# Embed Lottie animation in Streamlit with top-right positioning
lottie_html = """
<div style="text-align: center; margin-bottom: 20px;">
<h1 style="color:#0FFF50; font-family: Arial, sans-serif;">AI Chatbot<br>Your Personal Assistant</h1>
</div>
<div style="position: fixed; top: 0; right: 0;">
<script src="https://unpkg.com/@lottiefiles/lottie-player@2.0.8/dist/lottie-player.js"></script>
<lottie-player src="https://lottie.host/3e8ec22e-eb1b-4a61-8b78-5550fe0b94b8/AK7Vjkbjxk.json" background="##FFFFFF" speed="1" style="width: 300px; height: 300px" loop autoplay direction="1" mode="normal"></lottie-player>
</div>
"""
components.html(lottie_html, height=250)

GROQ_API_KEY = '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'

# Save the API key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Initialize the chat history in Streamlit session state if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to render chat messages with inline CSS
def render_chat_history():
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(
                f"""
                <div style='display: flex; align-items: flex-start; margin-bottom: 10px;'>
                    <div style='font-size: 24px; margin-right: 10px;'>👨‍💼</div>
                    <div style='background-color: #f0f0f0; color: #000; padding: 10px; border-radius: 10px; max-width: 70%; line-height: 1.5;'>
                        {message['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style='display: flex; align-items: flex-start; margin-bottom: 10px; flex-direction: row-reverse;'>
                    <div style='font-size: 24px; margin-left: 10px;'>🤖</div>
                    <div style='background-color: #d9fdd3; color: #000; padding: 10px; border-radius: 10px; max-width: 70%; line-height: 1.5;'>
                        {message['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# Render the chat history with enhanced styling
render_chat_history()

# Create two columns for the input and button
col1, col2 = st.columns([4, 1])

with col1:
    # Input field for user's message
    user_prompt = st.chat_input("Ask Me...")

with col2:
    # Clear History Button
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.rerun()

if user_prompt:
    # Append user's message to the chat history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Send user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history,
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Re-render the chat history to include the new messages
    st.rerun()
