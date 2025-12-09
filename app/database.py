from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

Base = declarative_base()

# create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database (create tables)."""
    Base.metadata.create_all(bind=engine)
