from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.video_task import VideoTask
from app.services.openai_client import OpenAIClient


class VideoService:

    @staticmethod
    def create_task(user_id: str, prompt: str, model: str):
        db: Session = SessionLocal()
        task = VideoTask(user_id=user_id, prompt=prompt, status="processing")
        db.add(task)
        db.commit()
        db.refresh(task)
        return task.id

    @staticmethod
    def generate_video(task_id: int):
        db: Session = SessionLocal()
        task = db.query(VideoTask).filter(VideoTask.id == task_id).first()
        if not task:
            return

        client = OpenAIClient()

        # NOTE: this is the correct async-video API call
        result = client.videos.create(
            model="gpt-4o-generative-video",
            prompt=task.prompt
        )

        # Update task
        task.status = "completed"
        task.video_url = result.url
        db.commit()

    @staticmethod
    def get_status(task_id: int):
        db = SessionLocal()
        return db.query(VideoTask).filter(VideoTask.id == task_id).first()

    @staticmethod
    def get_all_tasks(user_id: str):
        db = SessionLocal()
        return db.query(VideoTask).filter(VideoTask.user_id == user_id).all()
