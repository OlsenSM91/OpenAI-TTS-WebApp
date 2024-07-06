# OpenAI TTS WebApp

OpenAI TTS WebApp is a FastAPI-based web application that converts text input to speech using the OpenAI API. The app also allows users to upload a video, generate audio from text, and combine the generated audio with the uploaded video. The user interface is simple, mobile-optimized, and features selectable natural language voice models provided by OpenAI.

![Screenshot 2024-07-05 212610](https://github.com/OlsenSM91/OpenAI-TTS-WebApp/assets/130707762/355a478a-bdca-4ef7-861b-cf5674db5471)

## Features

- Convert text to speech using OpenAI's text-to-speech models.
- Upload a video file to be used with the generated audio.
- Combine the generated audio with the uploaded video.
- Choose from various voice models: Alloy, Echo, Fable, Onyx, Nova, and Shimmer.
- Mobile-optimized UI with a clean and user-friendly design.

## Requirements

- Python 3.6+
- FastAPI
- Uvicorn
- Pydantic
- Python-dotenv
- Pydub
- OpenAI
- aiofiles

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/OlsenSM91/OpenAI-TTS-WebApp.git
    cd OpenAI-TTS-WebApp
    ```

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Edit the `.env` file in the project root and add your OpenAI API key (Ensure you have a balance on your OpenAI API account):
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

4. Place your `logo.png` and `favicon.ico` in the `static` directory. I have included my basic logo and favicon courtesy of flaticon.com

## Running the Application

To start the application, run:
```bash
uvicorn app:app --host 0.0.0.0 --port 6996 --reload
```

Then open your browser and go to `http://127.0.0.1:6996`.

## Usage

1. Upload the video file you want to use.
2. Enter the text you want to convert to speech in the textarea.
3. Select the desired voice model from the dropdown.
4. Click the "Generate Audio" button to create the audio file.
5. Click the "Combine Audio and Video" button to combine the generated audio with the uploaded video.
6. Preview the combined video.

## Project Structure

```
OpenAI-TTS-WebApp/
├── app.py
├── requirements.txt
├── static/
│   ├── favicon.ico
│   ├── logo.png
│   └── styles.css
├── videos/
├── .env
└── README.md
```

## Acknowledgements

- [OpenAI](https://www.openai.com/) for providing the text-to-speech API.
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework.
- [Uvicorn](https://www.uvicorn.org/) for the ASGI server.
- [Pydub](https://pydub.com/) for audio manipulation.
- [Flaticon](https://flaticon.com/) for Logo/Favicon Image.

## Contributions

Contributions are welcome, there are some additional bells and whistles I would like to add such as a simple account authentication system, input form validations, voice model previews, and a generated preview before just downloading. But this was just a quick and dirty proof of concept that I built for my wife.
