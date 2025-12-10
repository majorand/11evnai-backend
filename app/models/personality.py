from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Personality(Base):
    __tablename__ = "personalities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
