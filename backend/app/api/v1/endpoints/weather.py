import urllib.request
import urllib.parse
import json
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, Request, Query
from app.core.config import settings
from app.schemas.schemas import WeatherRiskRequest, WeatherRiskResponse
from app.services.weather_service import WeatherRiskService
from app.services.geocoding_service import GeocodingService

router = APIRouter()
logger = logging.getLogger("agroscan.weather")

WEATHER_DESC_MR = {
    "clear sky": "निरभ्र आकाश (Clear Sky)",
    "few clouds": "कमी ढगाळ (Few Clouds)",
    "scattered clouds": "विखुरलेले ढग (Scattered Clouds)",
    "broken clouds": "ढगाळ वातावरण (Broken Clouds)",
    "overcast clouds": "पूर्ण ढगाळ (Overcast)",
    "light rain": "हलका पाऊस (Light Rain)",
    "moderate rain": "मध्यम पाऊस (Moderate Rain)",
    "heavy intensity rain": "मुसळधार पाऊस (Heavy Rain)",
    "very heavy rain": "अति मुसळधार पाऊस (Very Heavy Rain)",
    "thunderstorm": "वादळी पाऊस (Thunderstorm)",
    "thunderstorm with light rain": "विजांसह हलका पाऊस",
    "haze": "धुकट वातावरण (Haze)",
    "mist": "धुके (Mist)",
    "smoke": "धूर / धुके (Smoke)",
    "fog": "दाट धुके (Fog)"
}


def _detect_location_from_ip(client_ip: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Detects real geographic location (city, state, lat, lon) via IP geolocation.
    If client IP is local or private, queries external public exit IP.
    """
    try:
        # If no client IP or private IP, query local exit IP
        is_private = not client_ip or client_ip in ["127.0.0.1", "::1", "localhost"] or client_ip.startswith("192.168.") or client_ip.startswith("10.") or client_ip.startswith("172.16.")
        url = "http://ip-api.com/json/" if is_private else f"http://ip-api.com/json/{client_ip}"
        
        req = urllib.request.Request(url, headers={"User-Agent": "AgroScanAI/1.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "success":
                return {
                    "city": data.get("city"),
                    "region": data.get("regionName"),
                    "country": data.get("country"),
                    "latitude": float(data.get("lat")),
                    "longitude": float(data.get("lon"))
                }
    except Exception as e:
        logger.warning(f"IP Geolocation resolution failed: {e}")
    return None


@router.get("/current")
def get_current_weather(
    request: Request,
    city: Optional[str] = Query(None, description="City or district name"),
    lat: Optional[float] = Query(None, description="GPS Latitude"),
    lon: Optional[float] = Query(None, description="GPS Longitude"),
    lang: str = Query("en", description="Language code (en or mr)")
) -> Dict[str, Any]:
    """
    Retrieves real-time live weather based on:
    1. Device GPS coordinates (highest priority)
    2. Explicit city / district search
    3. Automatic IP Geolocation (falls back to farmer's real local region, e.g. Kolhapur)
    """
    api_key = getattr(settings, "WEATHER_API_KEY", None) or "58f50b7f998a3e7f90d73d87f6534183"
    
    detection_method = "manual_search"
    resolved_lat = lat
    resolved_lon = lon
    resolved_city = (city.strip() if city else "")

    # Clean auto/placeholder tokens
    if resolved_city.lower() in ["auto", "none", "null", "undefined"]:
        resolved_city = ""

    # 1. Determine location source
    if resolved_lat is not None and resolved_lon is not None:
        detection_method = "device_gps"
    elif resolved_city:
        detection_method = "city_query"
    else:
        # Auto-detect real location via client IP
        client_ip = request.headers.get("x-forwarded-for", "").split(",")[0].strip() or (request.client.host if request.client else None)
        ip_loc = _detect_location_from_ip(client_ip)
        if ip_loc:
            resolved_lat = ip_loc["latitude"]
            resolved_lon = ip_loc["longitude"]
            resolved_city = ip_loc["city"]
            detection_method = "auto_ip"
        else:
            # Fallback to Kolhapur agro-climatic region if all lookups fail
            resolved_city = "Kolhapur"
            detection_method = "regional_default"

    # 2. Query Live OpenWeatherMap API
    if api_key and api_key != "your_openweather_api_key_here":
        try:
            weather_lang = "mr" if lang == "mr" else "en"
            
            if resolved_lat is not None and resolved_lon is not None:
                params = urllib.parse.urlencode({
                    "lat": resolved_lat,
                    "lon": resolved_lon,
                    "appid": api_key,
                    "units": "metric",
                    "lang": weather_lang
                })
            else:
                params = urllib.parse.urlencode({
                    "q": resolved_city,
                    "appid": api_key,
                    "units": "metric",
                    "lang": weather_lang
                })

            url = f"https://api.openweathermap.org/data/2.5/weather?{params}"
            req = urllib.request.Request(url, headers={"User-Agent": "AgroScanAI/1.0"})
            
            with urllib.request.urlopen(req, timeout=6) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    main = data.get("main", {})
                    weather_list = data.get("weather", [{}])
                    wind = data.get("wind", {})
                    rain = data.get("rain", {})
                    coord = data.get("coord", {})
                    
                    loc_name = data.get("name") or resolved_city or "Local Farm"
                    raw_desc = (weather_list[0].get("description", "Clear sky") if weather_list else "Clear sky").lower()
                    
                    if lang == "mr":
                        cond_display = WEATHER_DESC_MR.get(raw_desc, raw_desc.title())
                    else:
                        cond_display = raw_desc.title()

                    final_lat = float(resolved_lat if resolved_lat is not None else coord.get("lat", 16.69))
                    final_lon = float(resolved_lon if resolved_lon is not None else coord.get("lon", 74.24))

                    return {
                        "location": loc_name,
                        "temperature_c": round(float(main.get("temp", 26.5)), 1),
                        "humidity_pct": round(float(main.get("humidity", 65.0)), 1),
                        "rainfall_mm": round(float(rain.get("1h", rain.get("3h", 0.0))), 1),
                        "condition": cond_display,
                        "wind_speed_kmh": round(float(wind.get("speed", 3.0)) * 3.6, 1),
                        "latitude": final_lat,
                        "longitude": final_lon,
                        "is_gps": detection_method == "device_gps",
                        "detection_method": detection_method,
                        "live_api": True
                    }
        except Exception as e:
            logger.warning(f"OpenWeatherMap API warning for {resolved_city} ({resolved_lat},{resolved_lon}): {e}")

    # Fallback to local reverse geocoded coordinates
    final_city = resolved_city or "Kolhapur"
    return {
        "location": final_city,
        "temperature_c": 28.0,
        "humidity_pct": 45.0,
        "rainfall_mm": 0.0,
        "condition": "कमी ढगाळ (Few Clouds)" if lang == "mr" else "Partly Cloudy",
        "wind_speed_kmh": 12.0,
        "latitude": resolved_lat or 16.69,
        "longitude": resolved_lon or 74.24,
        "is_gps": detection_method == "device_gps",
        "detection_method": detection_method,
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
