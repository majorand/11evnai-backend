import jwt
from fastapi import HTTPException, Header
from app.config import settings

# PEM key from Supabase Project Settings → API → JWT Secret
SUPABASE_JWT_SECRET = settings.SUPABASE_KEY

def decode_supabase_jwt(token: str):
    try:
        decoded = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Supabase token")

async def get_current_user(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.replace("Bearer ", "")

    decoded = decode_supabase_jwt(token)

    email = decoded.get("email")
    user_id = decoded.get("sub")

    if not email or not user_id:
        raise HTTPException(status_code=401, detail="Invalid user payload")

    return {"email": email, "id": user_id}
