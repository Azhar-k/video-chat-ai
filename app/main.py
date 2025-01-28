import streamlit as st
from transcription import transcribe_video
from chat import ChatBot
import tempfile
import os
from dotenv import load_dotenv

# Must set page config before any other st commands
st.set_page_config(page_title="VidChat AI", page_icon="🎥")

# Load environment variables from .env file
load_dotenv()

# Verify API key exists
if not os.getenv("GOOGLE_API_KEY"):
    st.error("No Google API key found in .env file")
    st.stop()

def main():
    st.title("VidChat AI 🎥💬")
    st.write("Chat with your video content!")

    try:
        # File uploader
        video_file = st.file_uploader("Upload your video", type=['mp4', 'avi', 'mov'])

        if video_file:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(video_file.read())
                video_path = tmp_file.name

            try:
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

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                # Cleanup temporary file
                if os.path.exists(video_path):
                    os.unlink(video_path)

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main() 