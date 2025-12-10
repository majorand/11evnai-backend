# app/services/three_d_text_service.py
from openai import OpenAI
import base64

client = OpenAI()

async def text_to_3d(prompt: str) -> bytes:
    response = client.chat.completions.create(
        model="gpt-4o-3d",
        messages=[{"role": "user", "content": prompt}]
    )

    model_b64 = response.choices[0].message["model"]
    return base64.b64decode(model_b64)
