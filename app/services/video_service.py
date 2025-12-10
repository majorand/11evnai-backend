<<<<<<< HEAD
from app.database import SessionLocal
from app.models.video_task import VideoTask
from app.services.openai_client import openai_client
=======

from app.database import get_db
from app.models import VideoTask
from sqlalchemy.orm import Session
from openai import OpenAI
import time

client = OpenAI()
>>>>>>> efdaf38d3cfbdfee6be2ae4448fa8893f1f02c60

class VideoService:

    @staticmethod
<<<<<<< HEAD
    def create_task(user_id: str, prompt: str, model: str = "gpt-4.2-video"):
        db = SessionLocal()
        task = VideoTask(
            user_id=user_id,
            prompt=prompt,
            model=model,
            status="processing"
        )
=======
    def create_task(user_id: str, prompt: str, model: str):
        db: Session = next(get_db())
        task = VideoTask(user_id=user_id, prompt=prompt)
>>>>>>> efdaf38d3cfbdfee6be2ae4448fa8893f1f02c60
        db.add(task)
        db.commit()
        db.refresh(task)
        db.close()
        return task.id

    @staticmethod
    def generate_video(task_id: int):
<<<<<<< HEAD
        db = SessionLocal()
        task = db.query(VideoTask).filter(VideoTask.id == task_id).first()
        if not task:
            db.close()
            return

        result = openai_client.video.generate(
            model=task.model,
            prompt=task.prompt,
        )

        task.video_url = result.url
        task.status = "completed"

=======
        db: Session = next(get_db())
        task = db.query(VideoTask).get(task_id)

        response = client.responses.create(
            model="gpt-4.2-video",
            input=task.prompt
        )

        time.sleep(3)

        task.video_url = f"https://cdn.11evn.ai/output/{task_id}.mp4"
        task.status = "complete"
>>>>>>> efdaf38d3cfbdfee6be2ae4448fa8893f1f02c60
        db.commit()
        db.close()

    @staticmethod
    def get_status(task_id: int):
<<<<<<< HEAD
        db = SessionLocal()
        task = db.query(VideoTask).filter(VideoTask.id == task_id).first()
        db.close()
        return task

    @staticmethod
    def get_all_tasks(user_id: str):
        db = SessionLocal()
        tasks = db.query(VideoTask).filter(VideoTask.user_id == user_id).all()
        db.close()
        return tasks
=======
        db: Session = next(get_db())
        return db.query(VideoTask).get(task_id)

    @staticmethod
    def get_all_tasks(user_id: str):
        db: Session = next(get_db())
        return db.query(VideoTask).filter(VideoTask.user_id == user_id).all()
>>>>>>> efdaf38d3cfbdfee6be2ae4448fa8893f1f02c60
