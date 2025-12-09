import requests
from io import BytesIO
from app.config import settings

LUMA_API_KEY = settings.LUMA_API_KEY

def text_to_3d(prompt: str):
    url = "https://api.lumalabs.ai/v1/generate/3d"

    payload = {
        "prompt": prompt,
        "output_format": "glb"
    }

    headers = {
        "Authorization": f"Bearer {LUMA_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers).json()

    model_url = response["model"]["url"]
    model_bytes = requests.get(model_url).content

    return BytesIO(model_bytes)
