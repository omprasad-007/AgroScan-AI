from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    farm,
    scan,
    weather,
    recommendations,
    chat,
    analytics,
    admin,
    health,
    crop_guides,
    plants,
    geocoding
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(auth.router, prefix="/user", tags=["User Profile"])
api_router.include_router(farm.router, prefix="/farms", tags=["Farms"])
api_router.include_router(geocoding.router, prefix="/geocoding", tags=["Geocoding & GPS"])
api_router.include_router(plants.router, prefix="/plants", tags=["Plants"])
api_router.include_router(scan.router, prefix="/predictions", tags=["Predictions & Scans"])
api_router.include_router(weather.router, prefix="/weather", tags=["Weather"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI Chatbot"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(crop_guides.router, prefix="/crop-guides", tags=["Crop Cultivation Guides"])
