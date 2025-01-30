from langchain_community.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParserLocal
import tempfile
import os
import streamlit as st
import shutil  # New import
import time

def download_youtube_video(url: str) -> str:
    """Handle YouTube audio download and transcription using Whisper"""
    try:
        status = st.empty()
        status.info("Processing the video...")
        
        # Create temporary directory
        save_dir = tempfile.mkdtemp()
        
        # Initialize loader with Whisper parser
        loader = GenericLoader(
            YoutubeAudioLoader([url], save_dir),
            OpenAIWhisperParserLocal()  # Local Whisper model
        )

        # Execute download and transcription
        with st.spinner("Downloading and transcribing audio..."):
            docs = loader.load()
            
        if not docs:
            status.error("Failed to process YouTube video")
            return None

        # Combine transcript text
        transcript = " ".join(doc.page_content for doc in docs)
        
        # Update status
        status.success("Video processed successfully!")
        return transcript

    except ModuleNotFoundError as e:
        status.error(f"Missing required package: {str(e)}. Please install it with pip install {e.name}")
        return None
    except Exception as e:
        status.error(f"Error processing YouTube video: {str(e)}")
        return None
    finally:
        # Clean up temporary directory and contents
        if 'save_dir' in locals():
            try:
                shutil.rmtree(save_dir)
            except Exception as e:
                print(f"Error cleaning up directory: {str(e)}")
        # Clear processing status after 3 seconds
        if 'status' in locals():
            time.sleep(3)
            status.empty() 