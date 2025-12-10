# app/services/video_service.py
from openai import OpenAI
from app.database import SessionLocal
from app.models.video_model import VideoTask
import time

client = OpenAI()

class VideoService:

    @staticmethod
    def create_task(user_id: str, prompt: str, model: str):
        db = SessionLocal()
        task = VideoTask(
            user_id=user_id,
            prompt=prompt,
            status="processing",
            video_url=None,
            model=model
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task.id

    @staticmethod
    def generate_video(task_id: int):
        db = SessionLocal()
        task = db.query(VideoTask).filter(VideoTask.id == task_id).first()

        try:
            job = client.videos.generate(
                model=task.model,
                prompt=task.prompt
            )

            while True:
                status = client.videos.status(job.id)
                if status.status == "completed":
                    break
                time.sleep(2)

            task.status = "completed"
            task.video_url = status.output_url

        except:
            task.status = "failed"

        db.commit()

    @staticmethod
    def get_status(task_id):
        db = SessionLocal()
        return db.query(VideoTask).filter(VideoTask.id == task_id).first()

    @staticmethod
    def get_all_tasks(user_id):
        db = SessionLocal()
        return db.query(VideoTask).filter(VideoTask.user_id == user_id).all()
