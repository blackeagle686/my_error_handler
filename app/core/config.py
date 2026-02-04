
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My Coder Error Handler"
    VERSION: str = "1.0.0"
    
    # LLM Settings
    USE_MOCK_LLM: bool = os.getenv("USE_MOCK_LLM", "False").lower() == "true"
    MODEL_PATH: str = os.getenv("MODEL_PATH", "Qwen/Qwen2.5-Coder-1.5B-Instruct")
    
    # Vector DB
    CHROMA_DB_DIR: str = os.path.join(os.getcwd(), "chroma_db")
    
    class Config:
        env_file = ".env"

settings = Settings()
