from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Base class for models
Base = declarative_base()

# Create the SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database initializer
def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
