from fastapi import APIRouter, HTTPException, BackgroundTasks, Body
from app.services.video_service import VideoService
import asyncio

router = APIRouter()

@router.post("/create")
async def create_video(
    background_tasks: BackgroundTasks,
    user_id: str = Body(...),
    prompt: str = Body(...),
    model: str = Body("openai-video")   # cleaned model name
):
    """
    Creates a new async video generation task.
    """
    task_id = await VideoService.create_task(user_id, prompt, model)

    # queue async generator properly
    background_tasks.add_task(
        lambda: asyncio.create_task(VideoService.generate_video(task_id))
    )

    return {"task_id": task_id, "status": "processing"}


@router.get("/status/{task_id}")
async def check_status(task_id: int):
    task = await VideoService.get_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "task_id": task.id,
        "status": task.status,
        "video_url": task.video_url
    }


@router.get("/list/{user_id}")
async def list_tasks(user_id: str):
    tasks = await VideoService.get_all_tasks(user_id)
    return [
        {
            "task_id": t.id,
            "prompt": t.prompt,
            "status": t.status,
            "video_url": t.video_url,
            "created_at": t.created_at,
        }
        for t in tasks
    ]
