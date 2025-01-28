import streamlit as st
from transcription import transcribe_video
from chat import ChatBot
import tempfile
import os
from dotenv import load_dotenv
import logging

# Set up logging to print detailed error messages to the console
logging.basicConfig(level=logging.ERROR)

# Must set page config before any other st commands
st.set_page_config(page_title="VidChat AI", page_icon="🎥")

# Load environment variables from .env file
load_dotenv()

# Verify API key exists
if not os.getenv("GOOGLE_API_KEY"):
    st.error("Google API key is missing. Please check your configuration.")
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
                # Check if transcription is already done
                if 'transcript' not in st.session_state:
                    with st.spinner("Transcribing video..."):
                        transcript = transcribe_video(video_path)
                        st.session_state['transcript'] = transcript  # Store the transcript in session state

                # Initialize chat interface
                if 'messages' not in st.session_state:
                    st.session_state['messages'] = []

                # Display chat interface
                chatbot = ChatBot(st.session_state['transcript'])  # Use the stored transcript
                
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

                    # Show spinner while waiting for the response
                    with st.spinner("Generating..."):
                        # Generate and display assistant response
                        response = chatbot.get_response(prompt)
                        st.session_state['messages'].append({"role": "assistant", "content": response})
                        with st.chat_message("assistant"):
                            st.write(response)

            except Exception as e:
                st.error("An error occurred while processing your request. Please try again.")
                logging.error(f"Error during processing: {str(e)}")  # Log detailed error
            finally:
                # Cleanup temporary file
                if os.path.exists(video_path):
                    os.unlink(video_path)

    except Exception as e:
        st.error("An unexpected error occurred. Please try again later.")
        logging.error(f"Unexpected error: {str(e)}")  # Log detailed error

if __name__ == "__main__":
    main() 