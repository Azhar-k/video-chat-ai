# VidChat AI

VidChat AI is an application that allows users to have interactive conversations about video content. Users can upload videos and ask questions about their content, receiving contextual answers based on the video's transcript.

## Features

- Video upload support
- Automatic video transcription
- Interactive Q&A based on video content
- Context-aware responses

## Setup

1. Clone the repository

2. Create and activate virtual environment:
   
   For Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   For macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the project root directory
   - Add your OpenAI API key:
     ```bash
     OPENAI_API_KEY=your_actual_api_key_here
     ```
   - You can get your API key from: https://platform.openai.com/api-keys

5. Run the application:
   ```bash
   streamlit run app/main.py
   ```