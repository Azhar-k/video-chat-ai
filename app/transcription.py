import whisper
import os

def transcribe_video(video_path: str) -> str:
    """
    Transcribe video using OpenAI's Whisper model
    
    Args:
        video_path (str): Path to the video file
        
    Returns:
        str: Transcribed text
    """
    try:
        model = whisper.load_model("base")
        result = model.transcribe(video_path)
        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        raise 