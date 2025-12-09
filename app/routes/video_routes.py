from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse
from app.utils.supabase_jwt import get_current_user

from app.services.video_edit_service import trim_video, resize_video
from app.services.video_effects_service import apply_effect
from app.services.video_lipsync_service import lipsync_video
from app.services.video_generation_openai import generate_video_openai
from app.services.video_generation_gemini import generate_video_veo

router = APIRouter()

@router.post("/video/trim")
async def trim(
    start: float = Form(...),
    end: float = Form(...),
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    output = trim_video(await file.read(), start, end)
    return StreamingResponse(output, media_type="video/mp4")


@router.post("/video/effect")
async def effect(
    effect: str = Form(...),
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    output = apply_effect(await file.read(), effect)
    return StreamingResponse(output, media_type="video/mp4")


@router.post("/video/lipsync")
async def lipsync(
    video: UploadFile = File(...),
    audio: UploadFile = File(...),
    user=Depends(get_current_user)
):
    output = lipsync_video(await video.read(), await audio.read())
    return StreamingResponse(output, media_type="video/mp4")


@router.post("/video/generate/openai")
async def generate_openai(
    prompt: str = Form(...),
    duration: int = Form(5),
    user=Depends(get_current_user)
):
    output = generate_video_openai(prompt, duration)
    return StreamingResponse(output, media_type="video/mp4")


@router.post("/video/generate/veo")
async def generate_veo(
    prompt: str = Form(...),
    duration: int = Form(5),
    user=Depends(get_current_user)
):
    output = generate_video_veo(prompt, duration)
    return StreamingResponse(output, media_type="video/mp4")
