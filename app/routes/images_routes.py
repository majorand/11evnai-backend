from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse, Response
from app.utils.supabase_jwt import get_current_user
from app.services.openai_image_service import (
    openai_remove_bg,
    openai_face_enhance,
    openai_upscale,
    openai_img2img,
    openai_inpaint
)

router = APIRouter()

@router.post("/images/remove-bg")
async def remove_bg(file: UploadFile = File(...), user=Depends(get_current_user)):
    img_bytes = await file.read()
    output = await openai_remove_bg(img_bytes)
    return StreamingResponse(output, media_type="image/png")

@router.post("/images/face-enhance")
async def face_enhance(file: UploadFile = File(...), user=Depends(get_current_user)):
    img_bytes = await file.read()
    output = await openai_face_enhance(img_bytes)
    return StreamingResponse(output, media_type="image/png")

@router.post("/upscale")
async def upscale(file: UploadFile = File(...)):
    img_bytes = await file.read()
    output = await openai_upscale(img_bytes)
    return Response(content=output, media_type="image/png")

@router.post("/images/img2img")
async def img2img(
    prompt: str = Form(...),
    strength: float = Form(0.8),
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    img_bytes = await file.read()
    output = await openai_img2img(prompt, img_bytes, strength)
    return StreamingResponse(output, media_type="image/png")

@router.post("/images/inpaint")
async def inpaint(
    prompt: str = Form(...),
    file: UploadFile = File(...),
    mask: UploadFile = File(...),
    user=Depends(get_current_user)
):
