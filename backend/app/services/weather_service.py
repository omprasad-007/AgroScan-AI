import logging
import httpx
from typing import Dict, Any
from app.core.config import settings

logger = logging.getLogger("agroscan")

class WeatherRiskService:
    """
    Scientific Microclimate Disease Outbreak Risk Engine.
    Executes a 7-stage risk evaluation pipeline:
    Input Validation -> Crop/Pathogen Parameters -> Factor Calculation -> Combination -> Risk Scoring -> Category -> Explain WHY.
    """
    WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

    # Crop & Pathogen Germination Parameter Profiles
    PATHOGEN_PROFILES = {
        "Tomato": {
            "pathogen": "Phytophthora infestans (Late Blight)",
            "temp_opt": (18.0, 24.0),
            "temp_range": (10.0, 28.0),
            "humidity_crit": 80.0,
            "humidity_mod": 65.0,
            "rain_sensitive": True
        },
        "Potato": {
            "pathogen": "Phytophthora infestans (Late Blight)",
            "temp_opt": (16.0, 22.0),
            "temp_range": (8.0, 26.0),
            "humidity_crit": 85.0,
            "humidity_mod": 70.0,
            "rain_sensitive": True
        },
        "Rice": {
            "pathogen": "Magnaporthe oryzae (Rice Blast)",
            "temp_opt": (24.0, 28.0),
            "temp_range": (20.0, 32.0),
            "humidity_crit": 88.0,
            "humidity_mod": 75.0,
            "rain_sensitive": True
        },
        "Wheat": {
            "pathogen": "Puccinia striiformis (Stripe Rust)",
            "temp_opt": (12.0, 18.0),
            "temp_range": (5.0, 22.0),
            "humidity_crit": 75.0,
            "humidity_mod": 60.0,
            "rain_sensitive": False
        },
        "Cotton": {
            "pathogen": "Xanthomonas citri (Bacterial Blight)",
            "temp_opt": (28.0, 34.0),
            "temp_range": (22.0, 38.0),
            "humidity_crit": 75.0,
            "humidity_mod": 60.0,
            "rain_sensitive": True
        },
        "Soybean": {
            "pathogen": "Phakopsora pachyrhizi (Asian Rust)",
            "temp_opt": (20.0, 26.0),
            "temp_range": (15.0, 30.0),
            "humidity_crit": 80.0,
            "humidity_mod": 65.0,
            "rain_sensitive": True
        },
        "Maize": {
            "pathogen": "Puccinia sorghi (Common Rust)",
            "temp_opt": (16.0, 25.0),
            "temp_range": (12.0, 29.0),
            "humidity_crit": 85.0,
            "humidity_mod": 70.0,
            "rain_sensitive": False
        },
        "Chilli": {
            "pathogen": "Colletotrichum capsici (Anthracnose)",
            "temp_opt": (25.0, 30.0),
            "temp_range": (20.0, 35.0),
            "humidity_crit": 80.0,
            "humidity_mod": 65.0,
            "rain_sensitive": True
        },
        "Onion": {
            "pathogen": "Alternaria porri (Purple Blotch)",
            "temp_opt": (22.0, 27.0),
            "temp_range": (15.0, 32.0),
            "humidity_crit": 85.0,
            "humidity_mod": 70.0,
            "rain_sensitive": True
        },
        "Sugarcane": {
            "pathogen": "Colletotrichum falcatum (Red Rot)",
            "temp_opt": (27.0, 32.0),
            "temp_range": (20.0, 36.0),
            "humidity_crit": 80.0,
            "humidity_mod": 65.0,
            "rain_sensitive": True
        }
    }

    @classmethod
    def calculate_risk(
        cls, 
        temp_c: float, 
        humidity_pct: float, 
        rainfall_mm: float, 
        crop: str = "Tomato", 
        disease: str = ""
    ) -> Dict[str, Any]:
        """
        Calculates disease risk score (0-100), risk category, and scientific "Explain WHY" breakdown.
        """
        # 1. Validate Inputs
        temp_c = max(-20.0, min(60.0, float(temp_c)))
        humidity_pct = max(0.0, min(100.0, float(humidity_pct)))
        rainfall_mm = max(0.0, min(500.0, float(rainfall_mm)))
        
        # 2. Load Crop/Pathogen Parameters
        profile = cls.PATHOGEN_PROFILES.get(crop, cls.PATHOGEN_PROFILES["Tomato"])
        target_pathogen = disease if disease else profile["pathogen"]
        opt_low, opt_high = profile["temp_opt"]
        rng_low, rng_high = profile["temp_range"]

        # Base initial score
        base_score = 10.0
        thermal_pts = 0.0
        humidity_pts = 0.0
        rainfall_pts = 0.0
        factors = []

        # 3. Calculate Thermal Risk Factor
        if opt_low <= temp_c <= opt_high:
            thermal_pts = 35.0
            factors.append(
                f"Temperature ({temp_c:.1f}°C) matches optimal germination window ({opt_low}°C–{opt_high}°C) for {target_pathogen} (+35 pts)."
            )
        elif rng_low <= temp_c <= rng_high:
            thermal_pts = 20.0
            factors.append(
                f"Temperature ({temp_c:.1f}°C) lies within secondary germination range ({rng_low}°C–{rng_high}°C) for {target_pathogen} (+20 pts)."
            )
        else:
            thermal_pts = 5.0
            factors.append(
                f"Temperature ({temp_c:.1f}°C) is outside optimal spore germination bounds ({opt_low}°C–{opt_high}°C) (+5 pts)."
            )

        # 4. Calculate Relative Humidity Risk Factor
        if humidity_pct >= profile["humidity_crit"]:
            humidity_pts = 40.0
            factors.append(
                f"Relative humidity ({humidity_pct:.1f}%) exceeds critical leaf wetness threshold (≥{profile['humidity_crit']}%) (+40 pts)."
            )
        elif humidity_pct >= profile["humidity_mod"]:
            humidity_pts = 25.0
            factors.append(
                f"Relative humidity ({humidity_pct:.1f}%) is in moderate spore production range (≥{profile['humidity_mod']}%) (+25 pts)."
            )
        else:
            humidity_pts = 5.0
            factors.append(
                f"Relative humidity ({humidity_pct:.1f}%) is low, keeping foliage dry and slowing spore germination (+5 pts)."
            )

        # 5. Calculate Rainfall Risk Factor
        if rainfall_mm > 10.0:
            rainfall_pts = 15.0
            factors.append(
                f"Heavy rainfall ({rainfall_mm:.1f}mm) accelerates rain-splash spore dispersal across neighboring crops (+15 pts)."
            )
        elif rainfall_mm > 0.0:
            rainfall_pts = 10.0
            factors.append(
                f"Light/moderate rainfall ({rainfall_mm:.1f}mm) creates leaf moisture conducive for spore attachment (+10 pts)."
            )
        else:
            rainfall_pts = 0.0
            factors.append(
                "No active rainfall recorded (0.0mm); rain-splash transmission risk is minimal (+0 pts)."
            )

        # 6. Combine Factors & Compute Risk Index Score
        total_score = min(100.0, round(base_score + thermal_pts + humidity_pts + rainfall_pts, 1))

        # 7. Determine Risk Category & Actionable Advice
        if total_score >= 70.0:
            level = "High"
            advice = f"HIGH RISK: Microclimate conditions strongly favor rapid {target_pathogen} outbreak. Apply preventive organic copper or bio-fungicide sprays within 48 hours and monitor leaf underside."
        elif total_score >= 45.0:
            level = "Medium"
            advice = f"MEDIUM RISK: Moderate transmission threat for {crop} crops. Improve canopy airflow through pruning and avoid overhead evening irrigation."
        else:
            level = "Low"
            advice = f"LOW RISK: Ambient conditions are dry and non-conducive for {target_pathogen}. Maintain routine weekly crop health checks."

        return {
            "crop": crop,
            "pathogen": target_pathogen,
            "risk_score": total_score,
            "risk_level": level,
            "factor_breakdown": {
                "base_score": base_score,
                "thermal_points": thermal_pts,
                "humidity_points": humidity_pts,
                "rainfall_points": rainfall_pts
            },
            "contributing_factors": factors,
            "advice": advice
        }

    @classmethod
    async def fetch_live_weather(cls, city: str = "Pune", lat: Optional[float] = None, lon: Optional[float] = None, lang: str = "en") -> Dict[str, Any]:
        api_key = settings.WEATHER_API_KEY
        if not api_key:
            return cls._get_weather_fallback(city, lang=lang)

        params = {"appid": api_key, "units": "metric", "lang": "mr" if lang == "mr" else "en"}
        if lat is not None and lon is not None:
            params["lat"] = str(lat)
            params["lon"] = str(lon)
        else:
            params["q"] = city

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(cls.WEATHER_URL, params=params)
                if res.status_code == 200:
                    data = res.json()
                    main = data.get("main", {})
                    weather_list = data.get("weather", [{}])
                    rain = data.get("rain", {}).get("1h", 0.0)
                    condition_text = weather_list[0].get("description", "Clear").title() if weather_list else "Clear"
                    return {
                        "city": data.get("name", city),
                        "temp_c": main.get("temp", 26.5),
                        "humidity_pct": main.get("humidity", 82.0),
                        "rainfall_mm": rain,
                        "condition": condition_text,
                        "status": "available"
                    }

                logger.warning(f"OpenWeatherMap HTTP {res.status_code}. Returning controlled fallback.")
                return cls._get_weather_fallback(city, lang=lang)
        except Exception as e:
            logger.warning(f"WeatherRiskService exception: {e}")
            return cls._get_weather_fallback(city, lang=lang)

    @classmethod
    def fetch_weather_sync(cls, city: str = "Pune", lat: Optional[float] = None, lon: Optional[float] = None, lang: str = "en") -> Dict[str, Any]:
        api_key = settings.WEATHER_API_KEY
        if not api_key:
            return cls._get_weather_fallback(city, lang=lang)

        params = {"appid": api_key, "units": "metric", "lang": "mr" if lang == "mr" else "en"}
        if lat is not None and lon is not None:
            params["lat"] = str(lat)
            params["lon"] = str(lon)
        else:
            params["q"] = city

        try:
            with httpx.Client(timeout=4.0) as client:
                res = client.get(cls.WEATHER_URL, params=params)
                if res.status_code == 200:
                    data = res.json()
                    main = data.get("main", {})
                    weather_list = data.get("weather", [{}])
                    rain = data.get("rain", {}).get("1h", 0.0)
                    condition_text = weather_list[0].get("description", "Clear").title() if weather_list else "Clear"
                    return {
                        "city": data.get("name", city),
                        "temp_c": main.get("temp", 26.5),
                        "humidity_pct": main.get("humidity", 82.0),
                        "rainfall_mm": rain,
                        "condition": condition_text,
                        "status": "available"
                    }
        except Exception as e:
            logger.warning(f"WeatherRiskService sync fetch error: {e}")

        return cls._get_weather_fallback(city, lang=lang)

    @staticmethod
    def _get_weather_fallback(city: str, lang: str = "en") -> Dict[str, Any]:
        if lang == "mr":
            return {
                "city": city,
                "temp_c": 26.5,
                "humidity_pct": 82.0,
                "rainfall_mm": 5.0,
                "condition": "हलका पाऊस / मध्यम आर्द्रता",
                "status": "partially_available",
                "notice": "थेट हवामान माहिती तात्पुरती अनुपलब्ध आहे."
            }
        return {
            "city": city,
            "temp_c": 26.5,
            "humidity_pct": 82.0,
            "rainfall_mm": 5.0,
            "condition": "Pleasant / Mild Humidity",
            "status": "partially_available",
            "notice": "Live weather information temporarily unavailable."
        }
