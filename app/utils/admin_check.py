from fastapi import HTTPException
from app.config import settings

def ensure_admin(email: str):
    if email != settings.ADMIN_EMAIL:
        raise HTTPException(
            status_code=403,
            detail="You do not have admin permission for 11evnai."
        )
