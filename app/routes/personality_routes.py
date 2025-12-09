from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.personality_service import (
    create_personality,
    get_all_personalities
)
from app.utils.supabase_jwt import get_current_user
from app.config import settings

router = APIRouter()

def ensure_admin(email: str):
    if email != settings.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Admin only for 11evnai.")


@router.post("/personalities/create")
def create_persona(
    name: str = Form(...),
    description: str = Form(...),
    system_prompt: str = Form(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ensure_admin(user["email"])

    persona = create_personality(
        db, name, description, system_prompt, creator=user["email"]
    )

    return {"status": "created", "personality": persona.id, "brand": "11evnai"}


@router.get("/personalities/list")
def list_personas(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    personas = get_all_personalities(db)
    return {
        "brand": "11evnai",
        "count": len(personas),
        "personalities": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "created_by": p.created_by,
                "created_at": p.created_at
            }
            for p in personas
        ]
    }
