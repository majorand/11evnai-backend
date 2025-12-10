
from app.database import get_db
from app.models import VideoTask
from sqlalchemy.orm import Session
from openai import OpenAI
import time

client = OpenAI()

class VideoService:

    @staticmethod
    def create_task(user_id: str, prompt: str, model: str):
        db: Session = next(get_db())
        task = VideoTask(user_id=user_id, prompt=prompt)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task.id

    @staticmethod
    def generate_video(task_id: int):
        db: Session = next(get_db())
        task = db.query(VideoTask).get(task_id)

        response = client.responses.create(
            model="gpt-4.2-video",
            input=task.prompt
        )

        time.sleep(3)

        task.video_url = f"https://cdn.11evn.ai/output/{task_id}.mp4"
        task.status = "complete"
        db.commit()

    @staticmethod
    def get_status(task_id: int):
        db: Session = next(get_db())
        return db.query(VideoTask).get(task_id)

    @staticmethod
    def get_all_tasks(user_id: str):
        db: Session = next(get_db())
        return db.query(VideoTask).filter(VideoTask.user_id == user_id).all()
