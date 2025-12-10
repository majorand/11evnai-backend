# app/services/image_img2img_service.py
from openai import OpenAI
import base64

client = OpenAI()

async def image_to_image(prompt: str, image_bytes: bytes, strength: float) -> bytes:
    response = client.images.edit(
        model="gpt-image-1",
        image=image_bytes,
        prompt=prompt
    )

    return base64.b64decode(response.data[0].b64_json)
