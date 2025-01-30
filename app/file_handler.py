import tempfile
import streamlit as st

def handle_uploaded_file() -> str:
    """Handle file upload and return temporary file path"""
    video_file = st.file_uploader("Upload your video", type=['mp4', 'avi', 'mov'])
    if video_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(video_file.read())
            return tmp_file.name
    return None 