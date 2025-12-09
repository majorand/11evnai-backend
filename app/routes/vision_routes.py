from fastapi import APIRouter, File, UploadFile, Depends
from app.services.vision_service import (
    generate_caption,
    extract_text,
    analyze_document
)
from app.utils.supabase_jwt import get_current_user

router = APIRouter()

@router.post("/vision/caption")
async def caption_image(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    img_bytes = await file.read()
    caption = generate_caption(img_bytes)
    return {"caption": caption, "brand": "11evnai"}


@router.post("/vision/ocr")
async def ocr_image(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    img_bytes = await file.read()
    text = extract_text(img_bytes)
    return {"text": text, "brand": "11evnai"}


@router.post("/vision/document")
async def document_analysis(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    img_bytes = await file.read()
    analysis = analyze_document(img_bytes)
    return {"analysis": analysis, "brand": "11evnai"}
