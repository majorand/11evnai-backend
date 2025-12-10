# app/services/image_upscale_service.py
from openai import OpenAI
import base64

client = OpenAI()

async def upscale_image(image_bytes: bytes) -> bytes:
    response = client.images.edit(
        model="gpt-image-1",
        image=image_bytes,
        prompt="Upscale this image to higher resolution with improved clarity."
    )

    return base64.b64decode(response.data[0].b64_json)
