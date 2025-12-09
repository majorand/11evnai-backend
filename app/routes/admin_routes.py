from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.admin_service import get_system_stats, get_recent_activity
from app.utils.supabase_jwt import get_current_user
from app.config import settings

router = APIRouter()

def ensure_admin(user_email: str):
    if user_email != settings.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Not authorized for 11evnai admin access")


@router.get("/admin/stats")
def admin_stats(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ensure_admin(user["email"])
    stats = get_system_stats(db)
    return {"brand": "11evnai", "stats": stats}


@router.get("/admin/activity")
def admin_activity(
    limit: int = 20,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ensure_admin(user["email"])
    logs = get_recent_activity(db, limit)
    return {"brand": "11evnai", "activity": logs}


@router.get("/admin/users")
def admin_users(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ensure_admin(user["email"])

    users = db.execute("SELECT id, email, created_at FROM users ORDER BY created_at DESC").fetchall()

    return {
        "brand": "11evnai",
        "users": [
            {
                "id": row.id,
                "email": row.email,
                "created_at": row.created_at.isoformat() if row.created_at else None
            }
            for row in users
        ]
    }
