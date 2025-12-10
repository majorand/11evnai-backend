from fastapi import APIRouter, Form, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from app.utils.supabase_jwt import get_current_user
from app.services.three_d_text_service import text_to_3d
from app.services.three_d_image_service import image_to_3d

router = APIRouter()

@router.post("/3d/text")
async def text_3d(
    prompt: str = Form(...),
    user = Depends(get_current_user)
):
    # async-safe call
    model_bytes = await text_to_3d(prompt)

    # GLB format (binary)
    return StreamingResponse(
        model_bytes,
        media_type="model/gltf-binary"
    )


@router.post("/3d/image")
async def image_3d(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):
    img_bytes = await file.read()

    # async-safe call
    model_bytes = await image_to_3d(img_bytes)

    # OBJ format (plaintext)
    return StreamingResponse(
        model_bytes,
        media_type="model/obj"
    )
