from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class VideoTask(Base):
    __tablename__ = "video_tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    prompt = Column(String)
    model = Column(String, default="gpt-4o-generative-video")
    status = Column(String, default="processing")
    video_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
