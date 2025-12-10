# app/services/image_face_service.py
from openai import OpenAI
import base64

client = OpenAI()

async def enhance_face(image_bytes: bytes) -> bytes:
    response = client.images.edit(
        model="gpt-image-1",
        image=image_bytes,
        prompt="Enhance the face: improve detail, clarity, and natural skin texture. Do not alter identity."
    )

    return base64.b64decode(response.data[0].b64_json)
