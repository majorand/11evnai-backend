import requests
from io import BytesIO

HF_ZERO123_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-zero123"
HF_API_KEY = "YOUR_HUGGINGFACE_API_KEY"

def image_to_3d(image_bytes: bytes):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(HF_ZERO123_URL, headers=headers, data=image_bytes)

    return BytesIO(response.content)
