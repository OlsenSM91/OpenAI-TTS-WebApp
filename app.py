from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydub import AudioSegment
import os
import datetime
from pathlib import Path
import aiofiles
import uvicorn
import logging
import subprocess
import openai
from pydantic import BaseModel
import traceback

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise EnvironmentError("OPENAI_API_KEY is not set in the environment variables")

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Change to DEBUG for more verbosity
logger = logging.getLogger(__name__)

@app.post("/upload-video/")
async def upload_video(video: UploadFile = File(...)):
    try:
        logger.debug("Starting video upload")
        video_dir = Path("videos")
        video_dir.mkdir(exist_ok=True)
        original_video_path = video_dir / f"uploaded_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        async with aiofiles.open(original_video_path, 'wb') as out_file:
            content = await video.read()
            await out_file.write(content)

        cropped_video_path = original_video_path
        if not is_proper_aspect_ratio(original_video_path):
            cropped_video_path = video_dir / f"cropped_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            crop_video(original_video_path, cropped_video_path)

        logger.info(f"Video uploaded and cropped successfully: {cropped_video_path}")
        return {"video_path": str(cropped_video_path)}
    except Exception as e:
        logger.error(f"Error uploading video: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error uploading video")

@app.post("/generate-audio/")
async def generate_audio(text: str = Form(...), voice: str = Form("alloy")):
    logger.debug(f"Received text-to-speech request with text: {text} and voice: {voice}")
    try:
        client = openai.OpenAI()
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        first_words = "_".join(text.split()[:5])
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path_mp3 = Path(f"videos/{first_words}_{voice}_{timestamp}.mp3")
        logger.debug(f"Generated speech file path: {audio_path_mp3}")

        response.stream_to_file(str(audio_path_mp3))

        logger.info(f"Audio generated successfully: {audio_path_mp3}")
        return {"audio_path": str(audio_path_mp3)}
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")

@app.post("/combine-audio-video/")
async def combine_audio_video(
    video_path: str = Form(...),
    audio_path: str = Form(...),
    start_time: float = Form(0.0)
):
    try:
        logger.debug(f"Combining audio {audio_path} with video {video_path}")
        combined_video_path = Path(f"videos/combined_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        audio = AudioSegment.from_file(audio_path)
        audio_duration = len(audio) / 1000  # duration in seconds
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-t', str(audio_duration),
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            '-y', str(combined_video_path)
        ]
        subprocess.run(cmd, check=True)
        
        logger.info(f"Combined video and audio successfully: {combined_video_path}")

        return {"combined_video_path": str(combined_video_path)}
    except Exception as e:
        logger.error(f"Error combining video and audio: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error combining video and audio")

def crop_video(input_path, output_path):
    cmd = [
        'ffmpeg',
        '-i', str(input_path),
        '-vf', 'crop=ih*9/16:ih',
        '-c:a', 'copy',
        '-y', str(output_path)
    ]
    subprocess.run(cmd, check=True)

def is_proper_aspect_ratio(video_path):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=s=x:p=0',
        str(video_path)
    ]
    output = subprocess.check_output(cmd).decode('utf-8').strip()
    width, height = map(int, output.split('x'))
    return abs(width / height - 9 / 16) < 0.01

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
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item active" aria-current="page">Upload Video</li>
                    <li class="breadcrumb-item">Generate Audio</li>
                    <li class="breadcrumb-item">Combine Audio and Video</li>
                </ol>
            </nav>
            <div id="upload-section" class="section">
                <form id="upload-form" enctype="multipart/form-data">
                    <label for="video">Upload Video:</label>
                    <input type="file" id="video" name="video" accept="video/*" required>
                    <button type="submit" class="upload-btn">Upload</button>
                </form>
                <progress id="upload-progress" value="0" max="100" style="width: 100%; display:none;"></progress>
                <video id="video-preview" controls style="display:none;"></video>
            </div>
            <div id="audio-section" class="section hidden">
                <form id="audio-form">
                    <textarea id="text" name="text" rows="4" cols="50" placeholder="Enter your text here..." required></textarea>
                    <label for="voice">Voice:</label>
                    <select id="voice" name="voice">
                        <option value="alloy" selected>Alloy</option>
                        <option value="echo">Echo</option>
                        <option value="fable">Fable</option>
                        <option value="onyx">Onyx</option>
                        <option value="nova">Nova</option>
                        <option value="shimmer">Shimmer</option>
                    </select>
                    <button type="submit" class="generate-btn">Generate Audio</button>
                </form>
                <audio id="audio-preview" controls style="display:none;"></audio>
            </div>
            <div id="combine-section" class="section hidden">
                <form id="combine-form">
                    <input type="hidden" id="video_path" name="video_path">
                    <input type="hidden" id="audio_path" name="audio_path">
                    <button type="submit" class="combine-btn">Combine Audio and Video</button>
                </form>
                <video id="combined-video-preview" controls style="display:none;"></video>
            </div>
        </div>
        <script>
            document.getElementById('upload-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const xhr = new XMLHttpRequest();
                xhr.open('POST', '/upload-video/', true);

                xhr.upload.onprogress = function(event) {
                    if (event.lengthComputable) {
                        const percentComplete = (event.loaded / event.total) * 100;
                        document.getElementById('upload-progress').value = percentComplete;
                        document.getElementById('upload-progress').style.display = 'block';
                    }
                };

                xhr.onload = function() {
                    if (xhr.status === 200) {
                        const response = JSON.parse(xhr.responseText);
                        document.getElementById('video_path').value = response.video_path;
                        document.getElementById('video-preview').src = response.video_path;
                        document.getElementById('video-preview').style.display = 'block';
                        document.getElementById('audio-section').classList.remove('hidden');
                        document.querySelector('.breadcrumb-item.active').classList.remove('active');
                        document.querySelector('.breadcrumb-item:nth-child(2)').classList.add('active');
                    }
                };

                xhr.send(formData);
            });

            document.getElementById('audio-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const xhr = new XMLHttpRequest();
                xhr.open('POST', '/generate-audio/', true);

                xhr.onload = function() {
                    if (xhr.status === 200) {
                        const response = JSON.parse(xhr.responseText);
                        document.getElementById('audio_path').value = response.audio_path;
                        document.getElementById('audio-preview').src = response.audio_path;
                        document.getElementById('audio-preview').style.display = 'block';
                        document.getElementById('combine-section').classList.remove('hidden');
                        document.querySelector('.breadcrumb-item.active').classList.remove('active');
                        document.querySelector('.breadcrumb-item:nth-child(3)').classList.add('active');
                    } else {
                        console.error('Error generating audio:', xhr.responseText);
                    }
                };

                xhr.onerror = function() {
                    console.error('Request failed');
                };

                xhr.send(formData);
            });

            document.getElementById('combine-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const xhr = new XMLHttpRequest();
                xhr.open('POST', '/combine-audio-video/', true);

                xhr.onload = function() {
                    if (xhr.status === 200) {
                        const response = JSON.parse(xhr.responseText);
                        document.getElementById('combined-video-preview').src = response.combined_video_path;
                        document.getElementById('combined-video-preview').style.display = 'block';
                    } else {
                        console.error('Error combining audio and video:', xhr.responseText);
                    }
                };

                xhr.onerror = function() {
                    console.error('Request failed');
                };

                xhr.send(formData);
            });
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6996, reload=True)