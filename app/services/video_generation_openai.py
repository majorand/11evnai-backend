from openai import OpenAI
import requests
from io import BytesIO

client = OpenAI()

def generate_video_openai(prompt: str, duration: int = 5):
    result = client.videos.generate(
        model="gpt-video-1",
        prompt=prompt,
        duration=duration
    )

    video_url = result.data[0].url
    video_bytes = requests.get(video_url).content
    return BytesIO(video_bytes)
