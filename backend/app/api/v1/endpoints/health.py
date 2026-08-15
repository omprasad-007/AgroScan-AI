from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "demo_mode": settings.DEMO_MODE,
        "model_type": settings.MODEL_TYPE
    }
