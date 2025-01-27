import streamlit as st
from transcription import transcribe_video
from chat import ChatBot
import tempfile
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify API key is set
if not os.getenv("OPENAI_API_KEY"):
    st.error("Please set your OpenAI API key in the .env file")
    st.stop()

st.set_page_config(page_title="VidChat AI", page_icon="🎥")

def main():
    st.title("VidChat AI 🎥💬")
    st.write("Chat with your video content!")

    # File uploader
    video_file = st.file_uploader("Upload your video", type=['mp4', 'avi', 'mov'])

    if video_file:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(video_file.read())
            video_path = tmp_file.name

        # Transcribe video
        with st.spinner("Transcribing video..."):
            transcript = transcribe_video(video_path)
            st.session_state['transcript'] = transcript

        # Initialize chat interface
        if 'messages' not in st.session_state:
            st.session_state['messages'] = []

        # Display chat interface
        chatbot = ChatBot(transcript)
        
        # Display chat history
        for message in st.session_state['messages']:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask something about the video"):
            # Add user message to chat history
            st.session_state['messages'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Generate and display assistant response
            with st.chat_message("assistant"):
                response = chatbot.get_response(prompt)
                st.session_state['messages'].append({"role": "assistant", "content": response})
                st.write(response)

        # Cleanup temporary file
        os.unlink(video_path)

if __name__ == "__main__":
    main() 