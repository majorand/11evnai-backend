# app/services/image_inpaint_service.py
from openai import OpenAI
import base64

client = OpenAI()

async def inpaint_image(prompt: str, image_bytes: bytes, mask_bytes: bytes) -> bytes:
    response = client.images.edit(
        model="gpt-image-1",
        image=image_bytes,
        mask=mask_bytes,
        prompt=prompt
    )

    return base64.b64decode(response.data[0].b64_json)
