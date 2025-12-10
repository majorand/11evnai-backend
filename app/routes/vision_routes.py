from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.vision_service import analyze_image_with_openai

router = APIRouter()

@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = "Describe this image"
):
    try:
        image_bytes = await file.read()
        result = await analyze_image_with_openai(image_bytes, prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
