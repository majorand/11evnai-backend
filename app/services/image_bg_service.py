# ======================================================
# 11EVNAI - OpenAI-Based Background Removal (No rembg)
# ======================================================

import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI

from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# ------------------------------------------------------
# Helper: Convert image bytes → Base64 string
# ------------------------------------------------------
def to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

# ------------------------------------------------------
# MAIN FUNCTION: Remove background using OpenAI Vision
# ------------------------------------------------------
async def remove_background(image_bytes: bytes):
    """
    Removes background using:
      1. GPT-4o Vision to generate segmentation mask
      2. OpenAI Image Editor to erase background

    Returns: transparent PNG bytes
    """

    b64_image = to_base64(image_bytes)

    # ----------------------------------------------
    # PART 1 → Ask GPT-4o to create segmentation mask
    # ----------------------------------------------
    mask_response = client.images.generate(
        model="gpt-image-1",
        prompt=(
            "Create a black & white segmentation mask. "
            "WHITE = subject, BLACK = background. "
            "Keep edges clean. Output mask only."
        ),
        image=b64_image,
        size="1024x1024"
    )

    mask_b64 = mask_response.data[0].b64_json
    mask_bytes = base64.b64decode(mask_b64)

    # ----------------------------------------------
    # PART 2 → Use OpenAI Image Editor to apply mask
    # ----------------------------------------------
    edited = client.images.edit(
        model="gpt-image-1",
        image=b64_image,
        mask=base64.b64encode(mask_bytes).decode("utf-8"),
        prompt="Remove background and output subject on a transparent background.",
        size="1024x1024"
    )

    output_b64 = edited.data[0].b64_json
    output_bytes = base64.b64decode(output_b64)

    return output_bytes
