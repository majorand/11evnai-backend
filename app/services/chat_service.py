from sqlalchemy.orm import Session
from openai import OpenAI
from app.models import Chat, Message
from datetime import datetime

client = OpenAI()

def get_or_create_chat(db: Session, user_id: str, chat_id: int = None):
    if chat_id:
        chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id).first()
        if chat:
            return chat

    new_chat = Chat(user_id=user_id, title="New 11evnai Chat")
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


def add_message(db: Session, chat_id: int, sender: str, content: str):
    msg = Message(chat_id=chat_id, sender=sender, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_chat_history(db: Session, chat_id: int):
    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at)
        .all()
    )
    return [{"role": msg.sender, "content": msg.content} for msg in messages]


def generate_ai_response(model: str, messages: list, personality_prompt: str = None):
    if personality_prompt:
        messages = [
            {"role": "system", "content": personality_prompt},
            *messages
        ]

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )
    return completion.choices[0].message["content"]
