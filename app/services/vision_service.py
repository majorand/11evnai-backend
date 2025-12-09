import base64
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_image_with_openai(image_bytes: bytes, prompt: str = "Describe this image"):
    """
    Sends an image + text prompt to OpenAI Vision (gpt-4o-mini).
    """

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded_image}"}
                ]
            }
        ]
    )

    return response.choices[0].message["content"]
