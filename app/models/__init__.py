
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

class VideoTask(Base):
    __tablename__ = "video_tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    prompt = Column(Text)
    status = Column(String, default="processing")
    video_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
