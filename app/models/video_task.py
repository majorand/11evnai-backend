from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class VideoTask(Base):
    __tablename__ = "video_tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    prompt = Column(String, nullable=False)
    model = Column(String, default="gpt-4.2-video")
    status = Column(String, default="processing")
    video_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
