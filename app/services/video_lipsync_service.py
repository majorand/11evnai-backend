import requests
from io import BytesIO

WAV2LIP_API = "https://api.deepai.org/api/wav2lip"

def lipsync_video(video_bytes: bytes, audio_bytes: bytes):
    files = {
        "video": ("video.mp4", video_bytes, "video/mp4"),
        "audio": ("audio.wav", audio_bytes, "audio/wav"),
    }

    headers = { "api-key": "YOUR_DEEPAI_API_KEY" }

    response = requests.post(WAV2LIP_API, files=files, headers=headers).json()

    video_url = response["output_url"]
    output = requests.get(video_url).content

    return BytesIO(output)
