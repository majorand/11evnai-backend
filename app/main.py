# ==========================================================
# 11EVNAI - Backend Main Application
# FastAPI + Supabase + OpenAI + Google + Video + 3D
# ==========================================================

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local imports
from app.database import init_db
from app.config import settings

# ROUTERS
from app.routes.auth_routes import router as auth_router
from app.routes.chat_routes import router as chat_router
from app.routes.vision_routes import router as vision_router  
from app.routes.images_routes import router as images_router
from app.routes.video_routes import router as video_router
from app.routes.audio_routes import router as audio_router
from app.routes.document_routes import router as document_router
from app.routes.three_d_routes import router as three_d_router
from app.routes.admin_routes import router as admin_router


# ==========================================================
# Initialize FastAPI App
# ==========================================================

app = FastAPI(
    title="11EVNAI Backend",
    description="Full multimodal AI backend for 11EVNAI (Chat, Vision, Video, 3D, Audio, Documents)",
    version="1.0.0"
)

# ==========================================================
# CORS (Frontend must be allowed)
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to Vercel URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Initialize Database
# ==========================================================

@app.on_event("startup")
def startup_event():
    print("Initializing database...")
    init_db()
    print("Database ready.")

# ==========================================================
# ROUTER REGISTRATION
# ==========================================================

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(vision_router, prefix="/vision", tags=["Vision"])
app.include_router(images_router, prefix="/images", tags=["Image Tools"])
app.include_router(video_router, prefix="/video", tags=["Video Tools"])
app.include_router(audio_router, prefix="/audio", tags=["Audio / Whisper"])
app.include_router(document_router, prefix="/documents", tags=["Document AI"])
app.include_router(three_d_router, prefix="/3d", tags=["3D Models"])
app.include_router(admin_router, prefix="/admin", tags=["Admin Tools"])



# ==========================================================
# ROOT ENDPOINT
# ==========================================================

@app.get("/")
def root():
    return {
        "status": "11EVNAI backend running",
        "version": "1.0.0",
        "services": [
            "chat",
            "vision",
            "images",
            "video",
            "audio",
            "documents",
            "3d",
            "admin"
        ]
    }

# ==========================================================
# DEVELOPMENT SERVER STARTER
# ==========================================================

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
