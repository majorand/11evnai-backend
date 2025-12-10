# app/services/image_bg_service.py
from openai import OpenAI
import base64
from PIL import Image
import io

client = OpenAI()

def remove_background(image_bytes: bytes) -> bytes:
    """
    Remove background using OpenAI by passing a mask and instruction.
    """

    # Create a full-white mask (meaning: edit whole image)
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    mask = Image.new("L", img.size, 255)

    buf_mask = io.BytesIO()
    mask.save(buf_mask, format="PNG")
    mask_bytes = buf_mask.getvalue()

    response = client.images.edit(
        model="gpt-image-1",
        image=image_bytes,
        mask=mask_bytes,
        prompt="Remove the background and produce a transparent PNG of the subject."
    )

    return base64.b64decode(response.data[0].b64_json)
