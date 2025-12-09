from openai import OpenAI
from PIL import Image
import pytesseract
from io import BytesIO

client = OpenAI()

def generate_caption(image_bytes: bytes):
    """
    Uses OpenAI GPT-4.1 Vision to describe image.
    """
    result = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Describe this image in detail."},
                    {"type": "input_image", "image": image_bytes}
                ]
            }
        ]
    )

    return result.choices[0].message["content"]


def extract_text(image_bytes: bytes):
    """
    OCR using Tesseract + fallback to OpenAI OCR.
    """
    try:
        img = Image.open(BytesIO(image_bytes))
        text = pytesseract.image_to_string(img)
        if text.strip():
            return text
    except:
        pass

    # Fallback to OpenAI OCR
    result = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract text from this image."},
                    {"type": "input_image", "image": image_bytes}
                ]
            }
        ]
    )

    return result.choices[0].message["content"]


def analyze_document(image_bytes: bytes):
    """
    GPT-4.1 Vision document understanding.
    """
    result = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Analyze the document, extract key data, summarize it, and structure it."},
                    {"type": "input_image", "image": image_bytes}
                ]
            }
        ]
    )

    return result.choices[0].message["content"]
