# OpenAI TTS WebApp

OpenAI TTS WebApp is a FastAPI-based web application that converts text input to speech using the OpenAI API. The app features a simple and mobile-optimized interface with selectable natural language voice models that are provided by OpenAI.

## Features

- Convert text to speech using OpenAI's text-to-speech models.
- Choose from various voice models: Alloy, Echo, Fable, Onyx, Nova, and Shimmer.
- Download generated audio in mp3 format.
- Mobile-optimized UI with a clean and user-friendly design.

## Requirements

- Python 3.6+
- FastAPI
- Uvicorn
- Pydantic
- Python-dotenv
- Pydub
- OpenAI

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

4. Place your `logo.png` and `favicon.ico` in the `static` directory. I have included my basic logo and favicon curtosey of flaticon.com

## Running the Application

To start the application, run:
```bash
uvicorn app:app --host 0.0.0.0 --port 6996 --reload
```

Then open your browser and go to `http://127.0.0.1:6996`.

## Usage

1. Enter the text you want to convert to speech in the textarea.
2. Select the desired voice model from the dropdown.
3. Click the "Generate" button to create and download the audio file.

## Project Structure

```
OpenAI-TTS-WebApp/
├── app.py
├── requirements.txt
├── static/
│   ├── favicon.ico
│   ├── logo.png
│   └── styles.css
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

Contributions are welcome, there are some additional bells and whistles I would like to add such as a simple account authentication system, input form validations, voice model previews and a generated preview before just downloading. But this was just a quick n dirty proof of concept that I built for my wife.
