from fastapi import APIRouter, Depends
from app.schemas.schemas import WeatherRiskRequest, WeatherRiskResponse
from app.services.weather_service import WeatherRiskService

router = APIRouter()

@router.get("/current")
def get_current_weather(city: str = "Pune"):
    return {
        "location": city,
        "temperature_c": 26.5,
        "humidity_pct": 82.0,
        "rainfall_mm": 4.2,
        "condition": "Monsoon Light Rain",
        "wind_speed_kmh": 14.5
    }

@router.post("/risk", response_model=WeatherRiskResponse)
def compute_weather_risk(req: WeatherRiskRequest):
    res = WeatherRiskService.calculate_risk(
        temp_c=req.temperature_c,
        humidity_pct=req.humidity_pct,
        rainfall_mm=req.rainfall_mm,
        crop=req.crop,
        disease=req.disease or "Late Blight"
    )
    return WeatherRiskResponse(
        risk_score=res["risk_score"],
        risk_level=res["risk_level"],
        contributing_factors=res["contributing_factors"],
        advice=res["advice"]
    )
