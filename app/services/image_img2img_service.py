from PIL import Image
from io import BytesIO
import torch
from realesrgan import RealESRGAN

def upscale_image(image_bytes: bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGB")

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = RealESRGAN(device, scale=4)
    model.load_weights('weights/RealESRGAN_x4.pth')

    upscaled = model.predict(img)

    buffer = BytesIO()
    upscaled.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
