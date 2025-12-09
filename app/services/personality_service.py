from sqlalchemy.orm import Session
from app.models import Personality

def create_personality(db: Session, name: str, description: str, prompt: str, creator: str):
    persona = Personality(
        name=name,
        description=description,
        system_prompt=prompt,
        created_by=creator
    )
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona


def get_personality(db: Session, persona_id: int):
    return db.query(Personality).filter(Personality.id == persona_id).first()


def get_all_personalities(db: Session):
    return db.query(Personality).order_by(Personality.created_at.desc()).all()


def apply_personality(persona_prompt: str, history: list):
    """
    Insert the personality system message before the conversation history.
    """
    return [
        {"role": "system", "content": persona_prompt},
        *history
    ]
