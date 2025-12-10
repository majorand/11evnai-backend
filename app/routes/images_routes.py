from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse, Response
from app.utils.supabase_jwt import get_current_user
from app.services.image_bg_service import remove_background
from app.services.image_face_service import enhance_face
from app.services.image_upscale_service import upscale_image
from app.services.image_img2img_service import image_to_image
from app.services.image_inpaint_service import inpaint_image

router = APIRouter()


@router.post("/images/remove-bg")
async def remove_bg(file: UploadFile = File(...), user=Depends(get_current_user)):
    img_bytes = await file.read()
    output = remove_background(img_bytes)
    return StreamingResponse(output, media_type="image/png")


@router.post("/images/face-enhance")
async def face_enhance(file: UploadFile = File(...), user=Depends(get_current_user)):
    img_bytes = await file.read()
    output = enhance_face(img_bytes)
    return StreamingResponse(output, media_type="image/png")


@router.post("/images/upscale")
async def upscale(file: UploadFile = File(...), user=Depends(get_current_user)):
    img_bytes = await file.read()
    result = await upscale_image(img_bytes)
    return Response(content=result, media_type="image/png")


@router.post("/images/img2img")
async def img2img(
    prompt: str = Form(...),
    strength: float = Form(0.8),
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    img_bytes = await file.read()
    output = await image_to_image(prompt, img_bytes, strength)
    return StreamingResponse(output, media_type="image/png")


@router.post("/images/inpaint")
async def inpaint(
    prompt: str = Form(...),
    file: UploadFile = File(...),
    mask: UploadFile = File(...),
    user=Depends(get_current_user)
):
    img_bytes = await file.read()
    mask_bytes = await mask.read()
    output = await inpaint_image(prompt, img_bytes, mask_bytes)
    return StreamingResponse(output, media_type="image/png")
