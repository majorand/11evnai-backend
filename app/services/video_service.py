from app.database import SessionLocal
from app.models.video_task import VideoTask
from app.services.openai_client import openai_client

class VideoService:

    @staticmethod
    def create_task(user_id: str, prompt: str, model: str = "gpt-4.2-video"):
        db = SessionLocal()
        task = VideoTask(
            user_id=user_id,
            prompt=prompt,
            model=model,
            status="processing"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        db.close()
        return task.id

    @staticmethod
    def generate_video(task_id: int):
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

        db.commit()
        db.close()

    @staticmethod
    def get_status(task_id: int):
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
