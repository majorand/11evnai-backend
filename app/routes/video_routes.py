from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.video_service import VideoService

router = APIRouter()

@router.post("/create")
def create_video(background_tasks: BackgroundTasks, user_id: str, prompt: str, model: str = "gpt-4o-generative-video"):
    """
    Creates a new Async Video Task.
    """
    task_id = VideoService.create_task(user_id, prompt, model)
    background_tasks.add_task(VideoService.generate_video, task_id)
    return {"task_id": task_id, "status": "processing"}

@router.get("/status/{task_id}")
def check_status(task_id: int):
    task = VideoService.get_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "task_id": task.id,
        "status": task.status,
        "video_url": task.video_url
    }

@router.get("/list/{user_id}")
def list_tasks(user_id: str):
    tasks = VideoService.get_all_tasks(user_id)
    return [
        {
            "task_id": t.id,
            "prompt": t.prompt,
            "status": t.status,
            "video_url": t.video_url,
            "created_at": t.created_at
        }
        for t in tasks
    ]
