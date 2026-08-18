import urllib.request
import urllib.parse
import json
from typing import Optional
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.schemas import WeatherRiskRequest, WeatherRiskResponse
from app.services.weather_service import WeatherRiskService

router = APIRouter()

@router.get("/current")
def get_current_weather(
    city: str = "Pune",
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    lang: str = "en"
):
    api_key = getattr(settings, "WEATHER_API_KEY", None) or "58f50b7f998a3e7f90d73d87f6534183"
    
    if api_key and api_key != "your_openweather_api_key_here":
        try:
            weather_lang = "mr" if lang == "mr" else "en"
            if lat is not None and lon is not None:
                params = urllib.parse.urlencode({"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": weather_lang})
            else:
                safe_city = urllib.parse.quote(city.strip()) if city else "Pune"
                params = urllib.parse.urlencode({"q": safe_city, "appid": api_key, "units": "metric", "lang": weather_lang})

            url = f"https://api.openweathermap.org/data/2.5/weather?{params}"
            req = urllib.request.Request(url, headers={'User-Agent': 'AgroScanAI/1.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    main = data.get("main", {})
                    weather_list = data.get("weather", [{}])
                    wind = data.get("wind", {})
                    rain = data.get("rain", {})
                    
                    return {
                        "location": data.get("name", city),
                        "temperature_c": main.get("temp", 26.5),
                        "humidity_pct": main.get("humidity", 82.0),
                        "rainfall_mm": rain.get("1h", rain.get("3h", 0.0)),
                        "condition": weather_list[0].get("description", "Clear sky").title() if weather_list else "Clear sky",
                        "wind_speed_kmh": round(wind.get("speed", 4.0) * 3.6, 1),
                        "latitude": lat or data.get("coord", {}).get("lat"),
                        "longitude": lon or data.get("coord", {}).get("lon"),
                        "live_api": True
                    }
        except Exception as e:
            print(f"OpenWeatherMap API fetch warning for {city} ({lat},{lon}): {e}")

    # Fallback default values
    return {
        "location": city,
        "temperature_c": 26.5,
        "humidity_pct": 82.0,
        "rainfall_mm": 4.2,
        "condition": "हलका पाऊस / मध्यम आर्द्रता" if lang == "mr" else "Monsoon Light Rain",
        "wind_speed_kmh": 14.5,
        "latitude": lat,
        "longitude": lon,
        "live_api": False
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
