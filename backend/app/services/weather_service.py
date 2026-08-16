import logging
import httpx
from typing import Dict, Any
from app.core.config import settings

logger = logging.getLogger("agroscan")

class WeatherRiskService:
    """
    Service wrapper for OpenWeatherMap API and microclimate disease risk assessment.
    Calculates fungal/bacterial transmission probability based on thermal & relative humidity thresholds.
    """
    WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

    @classmethod
    def calculate_risk(
        cls, 
        temp_c: float, 
        humidity_pct: float, 
        rainfall_mm: float, 
        crop: str = "Crop", 
        disease: str = "Disease"
    ) -> Dict[str, Any]:
        """
        Evaluates disease transmission risk matrix.
        High relative humidity (>75%) + warm thermal range (20°C - 30°C) elevates fungal spore germination.
        """
        score = 15.0
        factors = []

        if 18.0 <= temp_c <= 29.0:
            score += 35.0
            factors.append(f"Optimal thermal range ({temp_c:.1f}°C) for pathogen germination")
        elif temp_c > 29.0:
            score += 15.0
            factors.append(f"Warm conditions ({temp_c:.1f}°C) accelerate bacterial spread")

        if humidity_pct >= 80.0:
            score += 40.0
            factors.append(f"Critical relative humidity ({humidity_pct:.1f}%) creating high leaf wetness")
        elif humidity_pct >= 65.0:
            score += 20.0
            factors.append(f"Moderate relative humidity ({humidity_pct:.1f}%) favorable for spore production")

        if rainfall_mm > 0.0:
            score += 10.0
            factors.append(f"Active rainfall ({rainfall_mm:.1f}mm) aiding splash dispersal of spores")

        score = min(100.0, score)

        if score >= 75.0:
            level = "High"
            advice = "High risk of rapid transmission. Apply preventive organic or copper-based sprays every 5-7 days."
        elif score >= 50.0:
            level = "Medium"
            advice = "Moderate transmission risk. Ensure proper plant spacing and avoid overhead evening irrigation."
        else:
            level = "Low"
            advice = "Low outbreak risk. Maintain routine weekly crop health monitoring."

        if not factors:
            factors.append("Current ambient conditions are dry and non-conducive for rapid pathogen spread.")

        return {
            "risk_score": round(score, 1),
            "risk_level": level,
            "contributing_factors": factors,
            "advice": advice
        }

    @classmethod
    async def fetch_live_weather(cls, city: str = "Pune") -> Dict[str, Any]:
        api_key = settings.WEATHER_API_KEY
        if not api_key:
            return cls._get_weather_fallback(city)

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(
                    cls.WEATHER_URL,
                    params={"q": city, "appid": api_key, "units": "metric"}
                )
                if res.status_code == 200:
                    data = res.json()
                    main = data.get("main", {})
                    rain = data.get("rain", {}).get("1h", 0.0)
                    return {
                        "city": city,
                        "temp_c": main.get("temp", 26.5),
                        "humidity_pct": main.get("humidity", 82.0),
                        "rainfall_mm": rain,
                        "status": "available"
                    }

                logger.warning(f"OpenWeatherMap HTTP {res.status_code}. Returning controlled fallback.")
                return cls._get_weather_fallback(city)
        except Exception as e:
            logger.warn(f"WeatherRiskService exception: {e}")
            return cls._get_weather_fallback(city)

    @staticmethod
    def _get_weather_fallback(city: str) -> Dict[str, Any]:
        return {
            "city": city,
            "temp_c": 26.5,
            "humidity_pct": 82.0,
            "rainfall_mm": 5.0,
            "status": "partially_available",
            "notice": "Live weather information temporarily unavailable."
        }
