from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.config import settings
from app.utils.supabase_jwt import get_current_user

router = APIRouter()

@router.post("/auth/sync")
def sync_user(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = user["id"]
    email = user["email"]

    # Check if user exists
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        new_user = User(id=user_id, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db_user = new_user

    return {
        "status": "ok",
        "user_id": db_user.id,
        "email": db_user.email,
        "is_admin": email == settings.ADMIN_EMAIL,
        "brand": "11evnai"
    }


@router.get("/auth/me")
def get_me(user=Depends(get_current_user)):
    return {
        "user_id": user["id"],
        "email": user["email"],
        "is_admin": user["email"] == settings.ADMIN_EMAIL,
        "platform": "11evnai"
    }
