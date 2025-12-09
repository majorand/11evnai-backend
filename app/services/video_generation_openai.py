from openai import OpenAI
from app.config import settings
from app.database import SessionLocal
from app.models import VideoTask
import time

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class VideoService:

    @staticmethod
    def create_task(user_id: str, prompt: str, model: str = "gpt-4o-generative-video"):
        """
        Create a video generation job.
        """
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
        """
        Polls the OpenAI API for video generation and updates DB.
        """
        db = SessionLocal()
        task = db.query(VideoTask).filter(VideoTask.id == task_id).first()
        if not task:
            db.close()
            return

        try:
            # Start job with OpenAI
            response = client.videos.generate(
                model=task.model,
                prompt=task.prompt
            )

            video_id = response.id

            # Poll until ready
            while True:
                status = client.videos.check(id=video_id)
                if status.status == "completed":
                    task.video_url = status.video.url
                    task.status = "completed"
                    db.commit()
                    break
                elif status.status == "failed":
                    task.status = "failed"
                    db.commit()
                    break
                time.sleep(2)

        except Exception as e:
            task.status = "failed"
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
