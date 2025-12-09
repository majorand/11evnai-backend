import requests
from io import BytesIO
from app.config import settings

GEMINI_API_KEY = settings.GEMINI_API_KEY

def generate_video_veo(prompt: str, duration: int = 5):
    url = "https://generativelanguage.googleapis.com/v1beta/models/veo-1:generateVideo"

    payload = {
        "prompt": prompt,
        "videoConfig": {
            "durationSeconds": duration
        }
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    video_url = data["video"]["uri"]

    video_bytes = requests.get(video_url).content
    return BytesIO(video_bytes)
