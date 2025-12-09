from diffusers import StableDiffusionInpaintPipeline
from io import BytesIO
from PIL import Image
import torch

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def inpaint_image(prompt: str, image_bytes: bytes, mask_bytes: bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    mask = Image.open(BytesIO(mask_bytes)).convert("RGB")

    result = pipe(prompt=prompt, image=image, mask_image=mask).images[0]

    buffer = BytesIO()
    result.save(buffer, "PNG")
    buffer.seek(0)
    return buffer
