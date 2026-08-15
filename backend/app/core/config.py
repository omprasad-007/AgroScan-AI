import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "AgroScan AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    DEMO_MODE: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./agroscan.db"

    # JWT Security
    SECRET_KEY: str = "agroscan_ai_super_secret_jwt_key_2026_college_mini_project_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Gemini AI API Key
    GEMINI_API_KEY: Optional[str] = None

    # ML Config
    MODEL_TYPE: str = "demo"
    MODEL_PATH: str = "../ml/models/plant_disease_model_v1.h5"
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
