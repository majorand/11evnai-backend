from datetime import datetime
from app.models.video_task import VideoTask
from app.database import SessionLocal
from app.openai_client import client
import os


class VideoService:

    @staticmethod
    def create_task(user_id: str, prompt: str, model: str = "gpt-4.2-video"):
        """Create a new video-generation task."""
        db = SessionLocal()
        try:
            task = VideoTask(
                user_id=user_id,
                prompt=prompt,
                model=model,
                status="pending",
                created_at=datetime.utcnow(),
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            return task.id
        finally:
            db.close()

    @staticmethod
    def get_status(task_id: int):
        """Retrieve task from DB."""
        db = SessionLocal()
        try:
            return db.query(VideoTask).filter(VideoTask.id == task_id).first()
        finally:
            db.close()

    @staticmethod
    def get_all_tasks(user_id: str):
        """Return all video tasks created by a user."""
        db = SessionLocal()
        try:
            return db.query(VideoTask).filter(VideoTask.user_id == user_id).order_by(VideoTask.id.desc()).all()
        finally:
            db.close()

    @staticmethod
    def generate_video(task_id: int):
        """Background job that actually generates the video."""
        db = SessionLocal()
        try:
            task = db.query(VideoTask).filter(VideoTask.id == task_id).first()
            if not task:
                return

            task.status = "processing"
            db.commit()

            # Call OpenAI video API
            response = client.videos.generate(
                model=task.model,
                prompt=task.prompt,
            )

            # Save output file
            output_path = f"videos/task_{task.id}.mp4"
            os.makedirs("videos", exist_ok=True)

            with open(output_path, "wb") as f:
                f.write(response)

            task.video_url = f"/static/videos/task_{task.id}.mp4"
            task.status = "completed"
            task.completed_at = datetime.utcnow()

            db.commit()

        except Exception as e:
            if task:
                task.status = "failed"
                task.error_message = str(e)
                db.commit()

        finally:
            db.close()
