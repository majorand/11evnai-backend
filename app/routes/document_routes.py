from fastapi import APIRouter

router = APIRouter()

@router.get("/documents/ping")
def ping_docs():
    return {"message": "Documents API is working"}
