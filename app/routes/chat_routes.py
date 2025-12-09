from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat_service import (
    get_or_create_chat,
    add_message,
    get_chat_history,
    generate_ai_response,
)
from app.utils.supabase_jwt import get_current_user
from app.services.personality_service import get_personality

router = APIRouter()

@router.post("/chat/send")
def send_message(
    message: str,
    chat_id: int = None,
    model: str = "gpt-4.1",
    personality_id: int = None,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    chat = get_or_create_chat(db, user_id=user["id"], chat_id=chat_id)

    add_message(db, chat_id=chat.id, sender="user", content=message)

    history = get_chat_history(db, chat.id)

    persona_prompt = None
    if personality_id:
        persona = get_personality(db, personality_id)
        if persona:
            persona_prompt = persona.system_prompt

    ai_reply = generate_ai_response(
        model=model,
        messages=history,
        personality_prompt=persona_prompt
    )

    add_message(db, chat_id=chat.id, sender="ai", content=ai_reply)

    return {
        "chat_id": chat.id,
        "reply": ai_reply,
        "model_used": model,
        "brand": "11evnai"
    }


@router.get("/chat/history")
def history(chat_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user["id"]).first()
    if not chat:
        return {"error": "Chat not found"}

    messages = get_chat_history(db, chat_id)
    return {"chat_id": chat_id, "messages": messages}
