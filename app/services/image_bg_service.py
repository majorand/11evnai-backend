from rembg import remove
from io import BytesIO
from PIL import Image

def remove_background(image_bytes: bytes):
    output = remove(image_bytes)
    return BytesIO(output)
