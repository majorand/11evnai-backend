
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_routes import router as auth_router
from app.routes.chat_routes import router as chat_router
from app.routes.vision_routes import router as vision_router
from app.routes.images_routes import router as images_router
from app.routes.video_routes import router as video_router
from app.routes.document_routes import router as document_router
from app.routes.three_d_routes import router as three_d_router

app = FastAPI(title="11EVN AI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "running"}

app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/chat")
app.include_router(vision_router, prefix="/vision")
app.include_router(images_router, prefix="/images")
app.include_router(video_router, prefix="/video")
app.include_router(document_router, prefix="/documents")
app.include_router(three_d_router, prefix="/3d")
