
from fastapi import APIRouter, BackgroundTasks
from app.services.video_service import VideoService

router = APIRouter()

@router.post("/create")
def create_video(background_tasks: BackgroundTasks, user_id: str, prompt: str, model: str = "gpt-4.2-video"):
    task_id = VideoService.create_task(user_id, prompt, model)
    background_tasks.add_task(VideoService.generate_video, task_id)
    return {"task_id": task_id, "status": "processing"}

@router.get("/status/{task_id}")
def status(task_id: int):
    return VideoService.get_status(task_id)

@router.get("/list/{user_id}")
def list_videos(user_id: str):
    return VideoService.get_all_tasks(user_id)
