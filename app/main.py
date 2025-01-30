import streamlit as st
from transcription import transcribe_video
from chat import ChatBot
from youtube_handler import download_youtube_video
from file_handler import handle_uploaded_file
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
        # Input selection
        input_method = st.radio(
            "Select input method:",
            ["YouTube URL", "Upload Video"],
            index=0
        )

        # Clear history when switching input methods
        if 'last_input_method' in st.session_state and st.session_state.last_input_method != input_method:
            for key in ['transcript', 'messages', 'chatbot', 'previous_url']:
                st.session_state.pop(key, None)
        
        st.session_state.last_input_method = input_method

        # Process input based on selection
        video_processed = False
        if input_method == "Upload Video":
            video_path = handle_uploaded_file()
            if video_path:
                try:
                    if 'transcript' not in st.session_state:
                        with st.spinner("Transcribing video..."):
                            transcript = transcribe_video(video_path)
                            st.session_state['transcript'] = transcript
                            video_processed = True
                finally:
                    if os.path.exists(video_path):
                        os.unlink(video_path)
                        
        elif input_method == "YouTube URL":
            youtube_url = st.text_input("Enter YouTube URL:")
            if youtube_url:
                # Clear history if URL changes
                if 'previous_url' in st.session_state and st.session_state.previous_url != youtube_url:
                    for key in ['transcript', 'messages', 'chatbot']:
                        st.session_state.pop(key, None)
                
                st.session_state.previous_url = youtube_url
                
                if 'transcript' not in st.session_state:
                    transcript = download_youtube_video(youtube_url)
                    if transcript:
                        st.session_state['transcript'] = transcript
                        video_processed = True

        # Chat interface - Only show after processing
        if 'transcript' in st.session_state:
            # Initialize chat messages first
            if 'messages' not in st.session_state:
                st.session_state.messages = []
            
            # Display chat messages immediately
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # Show chat input immediately
            if prompt := st.chat_input("Ask something about the video"):
                # Check if chatbot is ready
                if 'chatbot' not in st.session_state:
                    st.error("Please wait while the chatbot finishes initializing...")
                else:
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.write(prompt)

                    with st.spinner("Generating response..."):
                        try:
                            response = st.session_state.chatbot.get_response(prompt)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            with st.chat_message("assistant"):
                                st.write(response)
                        except Exception as e:
                            st.error(f"Error generating response: {str(e)}")

            # Initialize chatbot after showing input
            if 'chatbot' not in st.session_state:
                with st.spinner("Finalizing setup..."):
                    st.session_state.chatbot = ChatBot(st.session_state['transcript'])

    except Exception as e:
        st.error("An unexpected error occurred. Please try again later.")
        logging.error(f"Main error: {str(e)}")
        # Clear state on critical errors
        for key in ['transcript', 'messages', 'chatbot']:
            st.session_state.pop(key, None)

if __name__ == "__main__":
    main() 