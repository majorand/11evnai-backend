from sqlalchemy.orm import Session
from app.models import User, Chat, Message
from datetime import datetime

def get_system_stats(db: Session):
    total_users = db.query(User).count()
    total_chats = db.query(Chat).count()
    total_messages = db.query(Message).count()

    return {
        "total_users": total_users,
        "total_chats": total_chats,
        "total_messages": total_messages,
        "timestamp": datetime.utcnow().isoformat()
    }


def get_recent_activity(db: Session, limit: int = 20):
    messages = (
        db.query(Message)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "chat_id": msg.chat_id,
            "sender": msg.sender,
            "content": msg.content[:100] + ("..." if len(msg.content) > 100 else ""),
            "created_at": msg.created_at.isoformat()
        }
        for msg in messages
    ]
