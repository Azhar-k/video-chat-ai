import whisper
from pathlib import Path

def transcribe_video(video_path: str) -> str:
    """
    Transcribe video using OpenAI's Whisper model directly.
    
    Args:
        video_path (str): Path to the video file
        
    Returns:
        str: Transcribed text
    """
    try:
        # Load the Whisper model
        model = whisper.load_model("base")  # You can choose "small", "medium", "large", etc.
        
        # Transcribe the audio from the video file
        result = model.transcribe(video_path)
        
        # Return the transcribed text
        return result["text"]
        
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        raise 