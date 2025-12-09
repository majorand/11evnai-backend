from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# ==========================================================
# Fix database URL to work with psycopg (Python 3.13 compatible)
# ==========================================================

# Supabase/Render usually provides:  postgresql://...
# SQLAlchemy + psycopg requires:     postgresql+psycopg://...
db_url = settings.DATABASE_URL.replace(
    "postgresql://",
    "postgresql+psycopg://"
)

# ==========================================================
# SQLAlchemy Base Model
# ==========================================================

Base = declarative_base()

# ==========================================================
# Engine (psycopg3 + SQLAlchemy 2.0)
# ==========================================================

engine = create_engine(
    db_url,
    pool_pre_ping=True,     # Prevent stale connection crashes
)

# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ==========================================================
# Initialize DB (creates tables at startup)
# ==========================================================

def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

# ==========================================================
# FastAPI Dependency
# ==========================================================

def get_db():
    """Yield a database session for API routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
