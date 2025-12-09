import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "11evnai Backend"
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

settings = Settings()
