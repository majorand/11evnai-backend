# app/services/vision_service.py
from openai import OpenAI
import base64

client = OpenAI()

def analyze_image_with_openai(image_bytes: bytes, prompt: str):
    base64_img = base64.b64encode(image_bytes).decode()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url", 
                    "image_url": f"data:image/png;base64,{base64_img}"
                }
            ]}
        ]
    )

    return response.choices[0].message["content"]
