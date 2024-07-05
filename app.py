from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from pydub import AudioSegment
import os
import openai
import datetime
from pathlib import Path

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class TextToSpeechRequest(BaseModel):
    text: str
    voice: str = "alloy"

@app.post("/text-to-speech/")
async def text_to_speech(text: str = Form(...), voice: str = Form("alloy")):
    client = openai.OpenAI()

    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )

    first_words = "_".join(text.split()[:5])
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_path_mp3 = Path(f"{first_words}_{voice}_{timestamp}.mp3")

    response.stream_to_file(audio_path_mp3)

    return FileResponse(audio_path_mp3, media_type='audio/mpeg', filename=audio_path_mp3.name)

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/static/styles.css">
        <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
        <title>Text to Speech</title>
    </head>
    <body>
        <div class="container">
            <img src="/static/logo.png" alt="Logo" class="logo">
            <h1>Text to Speech Generator</h1>
            <form action="/text-to-speech/" method="post">
                <textarea id="text" name="text" rows="4" cols="50" placeholder="Enter your text here..."></textarea>
                <div class="controls">
                    <label for="voice">Voice:</label>
                    <select id="voice" name="voice">
                        <option value="alloy" selected>Alloy</option>
                        <option value="echo">Echo</option>
                        <option value="fable">Fable</option>
                        <option value="onyx">Onyx</option>
                        <option value="nova">Nova</option>
                        <option value="shimmer">Shimmer</option>
                    </select>
                    <button type="submit" class="generate-btn">Generate</button>
                </div>
            </form>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)