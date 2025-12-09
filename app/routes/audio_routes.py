from fastapi import APIRouter, UploadFile, File, Depends
from app.services.audio_service import transcribe_audio
from app.utils.supabase_jwt import get_current_user

router = APIRouter()

@router.post("/audio/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    audio_bytes = await file.read()
    text = transcribe_audio(audio_bytes)

    return {
        "transcription": text,
        "brand": "11evnai"
    }
