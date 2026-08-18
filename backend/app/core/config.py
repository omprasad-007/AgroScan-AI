import os
from pydantic_settings import BaseSettings
from typing import Optional

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Settings(BaseSettings):
    APP_NAME: str = "AgroScan AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    DEMO_MODE: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./agroscan.db"

    # JWT Security
    SECRET_KEY: str = "agroscan_ai_super_secret_jwt_key_2026_college_mini_project_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Security & CORS
    FRONTEND_URL: Optional[str] = None
    ALLOWED_ORIGINS: list[str] = [
        "https://agro-scan-ai-nine.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    MAX_UPLOAD_SIZE_MB: int = 10

    # External API Keys & AI Provider
    AI_PROVIDER: str = "openai"  # "openai" (OpenRouter/OpenAI) or "gemini"
    GEMINI_API_KEY: Optional[str] = None
    PLANT_ID_API_KEY: Optional[str] = None
    PERENUAL_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    WEATHER_API_KEY: Optional[str] = None

    # ML Config
    MODEL_TYPE: str = "demo"
    MODEL_PATH: str = "../ml/models/plant_disease_model_v1.h5"
    UPLOAD_DIR: str = "./uploads"

    model_config = {
        "env_file": [
            os.path.join(_BASE_DIR, ".env"),
            os.path.join(_BASE_DIR, "../.env"),
            ".env",
            "backend/.env"
        ],
        "extra": "ignore"
    }

settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
