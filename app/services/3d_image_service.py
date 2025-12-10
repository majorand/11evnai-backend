# app/services/three_d_image_service.py
from openai import OpenAI
import base64

client = OpenAI()

async def image_to_3d(image_bytes: bytes) -> bytes:
    b64_image = base64.b64encode(image_bytes).decode()

    response = client.chat.completions.create(
        model="gpt-4o-3d",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Generate a 3D model from this image."},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{b64_image}"
                    }
                ]
            }
        ]
    )

    model_b64 = response.choices[0].message["model"]
    return base64.b64decode(model_b64)
