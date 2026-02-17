

from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables from .env into process env
load_dotenv()

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "rag-intern-poc")
    env: str = os.getenv("ENV", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()