import urllib.request
import urllib.parse
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
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

DAY_NAME_MR = {
    "Monday": "सोमवार",
    "Tuesday": "मंगळवार",
    "Wednesday": "बुधवार",
    "Thursday": "गुरुवार",
    "Friday": "शुक्रवार",
    "Saturday": "शनिवार",
    "Sunday": "रविवार"
}

# Major agricultural districts and hubs in Maharashtra (bilingual support)
MAHARASHTRA_DISTRICTS = {
    "kolhapur": {"name_en": "Kolhapur", "name_mr": "कोल्हापूर", "lat": 16.7050, "lon": 74.2433},
    "कोल्हापूर": {"name_en": "Kolhapur", "name_mr": "कोल्हापूर", "lat": 16.7050, "lon": 74.2433},
    "pune": {"name_en": "Pune", "name_mr": "पुणे", "lat": 18.5204, "lon": 73.8567},
    "पुणे": {"name_en": "Pune", "name_mr": "पुणे", "lat": 18.5204, "lon": 73.8567},
    "sangli": {"name_en": "Sangli", "name_mr": "सांगली", "lat": 16.8524, "lon": 74.5815},
    "सांगली": {"name_en": "Sangli", "name_mr": "सांगली", "lat": 16.8524, "lon": 74.5815},
    "satara": {"name_en": "Satara", "name_mr": "सातारा", "lat": 17.6805, "lon": 74.0183},
    "सातारा": {"name_en": "Satara", "name_mr": "सातारा", "lat": 17.6805, "lon": 74.0183},
    "solapur": {"name_en": "Solapur", "name_mr": "सोलापूर", "lat": 17.6599, "lon": 75.9064},
    "सोलापूर": {"name_en": "Solapur", "name_mr": "सोलापूर", "lat": 17.6599, "lon": 75.9064},
    "nashik": {"name_en": "Nashik", "name_mr": "नाशिक", "lat": 19.9975, "lon": 73.7898},
    "नाशिक": {"name_en": "Nashik", "name_mr": "नाशिक", "lat": 19.9975, "lon": 73.7898},
    "ahmednagar": {"name_en": "Ahmednagar", "name_mr": "अहमदनगर", "lat": 19.0952, "lon": 74.7496},
    "अहमदनगर": {"name_en": "Ahmednagar", "name_mr": "अहमदनगर", "lat": 19.0952, "lon": 74.7496},
    "ahilyanagar": {"name_en": "Ahmednagar", "name_mr": "अहिल्यानगर", "lat": 19.0952, "lon": 74.7496},
    "jalgaon": {"name_en": "Jalgaon", "name_mr": "जळगाव", "lat": 21.0077, "lon": 75.5626},
    "जळगाव": {"name_en": "Jalgaon", "name_mr": "जळगाव", "lat": 21.0077, "lon": 75.5626},
    "aurangabad": {"name_en": "Chhatrapati Sambhajinagar", "name_mr": "छत्रपती संभाजीनगर", "lat": 19.8762, "lon": 75.3433},
    "औरंगाबाद": {"name_en": "Chhatrapati Sambhajinagar", "name_mr": "छत्रपती संभाजीनगर", "lat": 19.8762, "lon": 75.3433},
    "chhatrapati sambhajinagar": {"name_en": "Chhatrapati Sambhajinagar", "name_mr": "छत्रपती संभाजीनगर", "lat": 19.8762, "lon": 75.3433},
    "छत्रपती संभाजीनगर": {"name_en": "Chhatrapati Sambhajinagar", "name_mr": "छत्रपती संभाजीनगर", "lat": 19.8762, "lon": 75.3433},
    "nagpur": {"name_en": "Nagpur", "name_mr": "नागपूर", "lat": 21.1458, "lon": 79.0882},
    "नागपूर": {"name_en": "Nagpur", "name_mr": "नागपूर", "lat": 21.1458, "lon": 79.0882},
    "amravati": {"name_en": "Amravati", "name_mr": "अमरावती", "lat": 20.9374, "lon": 77.7796},
    "अमरावती": {"name_en": "Amravati", "name_mr": "अमरावती", "lat": 20.9374, "lon": 77.7796},
    "nanded": {"name_en": "Nanded", "name_mr": "नांदेड", "lat": 19.1383, "lon": 77.3210},
    "नांदेड": {"name_en": "Nanded", "name_mr": "नांदेड", "lat": 19.1383, "lon": 77.3210},
    "latur": {"name_en": "Latur", "name_mr": "लातूर", "lat": 18.4088, "lon": 76.5604},
    "लातूर": {"name_en": "Latur", "name_mr": "लातूर", "lat": 18.4088, "lon": 76.5604},
    "dhule": {"name_en": "Dhule", "name_mr": "धुळे", "lat": 20.9042, "lon": 74.7749},
    "धुळे": {"name_en": "Dhule", "name_mr": "धुळे", "lat": 20.9042, "lon": 74.7749},
    "ratnagiri": {"name_en": "Ratnagiri", "name_mr": "रत्नागिरी", "lat": 16.9902, "lon": 73.3120},
    "रत्नागिरी": {"name_en": "Ratnagiri", "name_mr": "रत्नागिरी", "lat": 16.9902, "lon": 73.3120},
    "sindhudurg": {"name_en": "Sindhudurg", "name_mr": "सिंधुदुर्ग", "lat": 16.1158, "lon": 73.6934},
    "सिंधुदुर्ग": {"name_en": "Sindhudurg", "name_mr": "सिंधुदुर्ग", "lat": 16.1158, "lon": 73.6934},
    "baramati": {"name_en": "Baramati", "name_mr": "बारामती", "lat": 18.1517, "lon": 74.5772},
    "बारामती": {"name_en": "Baramati", "name_mr": "बारामती", "lat": 18.1517, "lon": 74.5772},
    "kagal": {"name_en": "Kagal", "name_mr": "कागल", "lat": 16.5889, "lon": 74.3150},
    "कागल": {"name_en": "Kagal", "name_mr": "कागल", "lat": 16.5889, "lon": 74.3150},
    "karad": {"name_en": "Karad", "name_mr": "कराड", "lat": 17.2858, "lon": 74.1818},
    "कराड": {"name_en": "Karad", "name_mr": "कराड", "lat": 17.2858, "lon": 74.1818},
    "pandharpur": {"name_en": "Pandharpur", "name_mr": "पंढरपूर", "lat": 17.6775, "lon": 75.3278},
    "पंढरपूर": {"name_en": "Pandharpur", "name_mr": "पंढरपूर", "lat": 17.6775, "lon": 75.3278},
    "beed": {"name_en": "Beed", "name_mr": "बीड", "lat": 18.9891, "lon": 75.7601},
    "बीड": {"name_en": "Beed", "name_mr": "बीड", "lat": 18.9891, "lon": 75.7601},
    "parbhani": {"name_en": "Parbhani", "name_mr": "परभणी", "lat": 19.2686, "lon": 76.7708},
    "परभणी": {"name_en": "Parbhani", "name_mr": "परभणी", "lat": 19.2686, "lon": 76.7708},
    "jalna": {"name_en": "Jalna", "name_mr": "जालना", "lat": 19.8347, "lon": 75.8800},
    "जालना": {"name_en": "Jalna", "name_mr": "जालना", "lat": 19.8347, "lon": 75.8800},
    "dharashiv": {"name_en": "Dharashiv", "name_mr": "धाराशिव", "lat": 18.1861, "lon": 76.0419},
    "धाराशिव": {"name_en": "Dharashiv", "name_mr": "धाराशिव", "lat": 18.1861, "lon": 76.0419},
    "osmanabad": {"name_en": "Dharashiv", "name_mr": "उस्मानाबाद", "lat": 18.1861, "lon": 76.0419},
    "उस्मानाबाद": {"name_en": "Dharashiv", "name_mr": "उस्मानाबाद", "lat": 18.1861, "lon": 76.0419},
    "buldhana": {"name_en": "Buldhana", "name_mr": "बुलढाणा", "lat": 20.5311, "lon": 76.1844},
    "बुलढाणा": {"name_en": "Buldhana", "name_mr": "बुलढाणा", "lat": 20.5311, "lon": 76.1844},
    "akola": {"name_en": "Akola", "name_mr": "अकोला", "lat": 20.7002, "lon": 77.0082},
    "अकोला": {"name_en": "Akola", "name_mr": "अकोला", "lat": 20.7002, "lon": 77.0082},
    "yavatmal": {"name_en": "Yavatmal", "name_mr": "यवतमाळ", "lat": 20.3888, "lon": 78.1204},
    "यवतमाळ": {"name_en": "Yavatmal", "name_mr": "यवतमाळ", "lat": 20.3888, "lon": 78.1204},
    "washim": {"name_en": "Washim", "name_mr": "वाशीम", "lat": 20.1111, "lon": 77.1350},
    "वाशीम": {"name_en": "Washim", "name_mr": "वाशीम", "lat": 20.1111, "lon": 77.1350},
    "wardha": {"name_en": "Wardha", "name_mr": "वर्धा", "lat": 20.7453, "lon": 78.6022},
    "वर्धा": {"name_en": "Wardha", "name_mr": "वर्धा", "lat": 20.7453, "lon": 78.6022},
    "chandrapur": {"name_en": "Chandrapur", "name_mr": "चंद्रपूर", "lat": 19.9615, "lon": 79.2961},
    "चंद्रपूर": {"name_en": "Chandrapur", "name_mr": "चंद्रपूर", "lat": 19.9615, "lon": 79.2961},
    "gadchiroli": {"name_en": "Gadchiroli", "name_mr": "गडचिरोली", "lat": 20.1809, "lon": 80.0034},
    "गडचिरोली": {"name_en": "Gadchiroli", "name_mr": "गडचिरोली", "lat": 20.1809, "lon": 80.0034},
    "gondia": {"name_en": "Gondia", "name_mr": "गोंदिया", "lat": 21.4624, "lon": 80.1961},
    "गोंदिया": {"name_en": "Gondia", "name_mr": "गोंदिया", "lat": 21.4624, "lon": 80.1961},
    "bhandara": {"name_en": "Bhandara", "name_mr": "भंडारा", "lat": 21.1714, "lon": 79.6547},
    "भंडारा": {"name_en": "Bhandara", "name_mr": "भंडारा", "lat": 21.1714, "lon": 79.6547},
    "thane": {"name_en": "Thane", "name_mr": "ठाणे", "lat": 19.2183, "lon": 72.9781},
    "ठाणे": {"name_en": "Thane", "name_mr": "ठाणे", "lat": 19.2183, "lon": 72.9781},
    "palghar": {"name_en": "Palghar", "name_mr": "पालघर", "lat": 19.6967, "lon": 72.7699},
    "पालघर": {"name_en": "Palghar", "name_mr": "पालघर", "lat": 19.6967, "lon": 72.7699},
    "raigad": {"name_en": "Raigad", "name_mr": "रायगड", "lat": 18.6414, "lon": 72.8722},
    "रायगड": {"name_en": "Raigad", "name_mr": "रायगड", "lat": 18.6414, "lon": 72.8722},
    "mumbai": {"name_en": "Mumbai", "name_mr": "मुंबई", "lat": 19.0760, "lon": 72.8777},
    "मुंबई": {"name_en": "Mumbai", "name_mr": "मुंबई", "lat": 19.0760, "lon": 72.8777},
}


def _calculate_spray_advisory(temp: float, humidity: float, wind_kmh: float, rain_mm: float, lang: str = "en") -> Dict[str, str]:
    """Generates real-world practical agronomic spraying advisory for farmers."""
    if rain_mm > 1.0:
        return {
            "status": "AVOID",
            "headline": "पाऊस सुरू / अपेक्षित — फवारणी टाळा" if lang == "mr" else "Rain Ongoing/Expected — Avoid Spraying",
            "reason": "पावसामुळे औषध धुऊन जाईल. किमान २४ तास कोरड्या हवामानाची वाट पहा." if lang == "mr" else "Rainfall will wash away chemical/organic sprays. Wait for a dry window."
        }
    if wind_kmh > 15.0:
        return {
            "status": "AVOID",
            "headline": "जोरदार वारा — फवारणी करू नका" if lang == "mr" else "High Wind Speed — High Drift Risk",
            "reason": f"वाऱ्याचा वेग {wind_kmh} किमी/तास आहे. औषध हवेत उडून वाया जाईल आणि इतर पिकांवर पडू शकते." if lang == "mr" else f"Wind speed ({wind_kmh} km/h) exceeds safe spraying threshold (15 km/h)."
        }
    if humidity > 85.0:
        return {
            "status": "CAUTION",
            "headline": "अति आर्द्रता — बुरशीनाशक फवारणीस प्राधान्य" if lang == "mr" else "High Humidity — Prioritize Fungicides",
            "reason": "हवेत जास्त आर्द्रता असल्याने पानांवर बुरशी वेगाने वाढू शकते. प्रतिबंधात्मक बुरशीनाशक वापरा." if lang == "mr" else "High ambient humidity (>85%) favors fungal spore germination. Apply protective fungicide."
        }
    if temp > 34.0:
        return {
            "status": "CAUTION",
            "headline": "जास्त तापमान — सकाळी किंवा संध्याकाळी फवारणी करा" if lang == "mr" else "High Temperature — Spray in Early Morning",
            "reason": "दुपारच्या उन्हात फवारणी केल्यास पानांवर डाग पडू शकतात (Scorching). सकाळी १० पूर्वी किंवा संध्याकाळी फवारा." if lang == "mr" else "High daytime heat can cause leaf scorch. Spray before 10 AM or after 4 PM."
        }
    return {
        "status": "SAFE",
        "headline": "फवारणीसाठी उत्तम व अनुकूल वेळ" if lang == "mr" else "Optimal Crop Spraying Window",
        "reason": "तापमान, आर्द्रता आणि वारा नियंत्रणात आहेत. बुरशीनाशक किंवा खतांची फवारणी करण्यास उत्तम वेळ." if lang == "mr" else "Temperature, humidity, and wind velocity are all within optimal spraying parameters."
    }


def _detect_location_from_ip(client_ip: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Detects geographic location (city, state, lat, lon) via IP geolocation."""
    try:
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


def _resolve_location_params(
    city: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    lang: str = "en",
    request: Optional[Request] = None
) -> Dict[str, Any]:
    """
    Robust location resolver:
    1. Direct GPS coordinates (lat, lon)
    2. Maharashtra district dictionary (English and Marathi)
    3. Geospatial Nominatim query for any Indian village/taluka
    4. Client IP resolution (fallback)
    """
    clean_city = (city or "").strip()
    if clean_city.lower() in ["auto", "none", "null", "undefined"]:
        clean_city = ""

    # 1. Direct GPS
    if lat is not None and lon is not None:
        loc_name = f"GPS ({lat:.2f}°, {lon:.2f}°)"
        try:
            rev = GeocodingService.reverse_geocode(lat, lon, lang)
            if rev and rev.get("village"):
                loc_name = rev["village"]
                if rev.get("district") and rev["district"] != rev["village"]:
                    loc_name += f", {rev['district']}"
        except Exception:
            pass
        return {
            "lat": lat,
            "lon": lon,
            "location_name": loc_name,
            "method": "device_gps"
        }

    # 2. Known District dictionary (English & Marathi)
    if clean_city:
        matched = MAHARASHTRA_DISTRICTS.get(clean_city.lower()) or MAHARASHTRA_DISTRICTS.get(clean_city)
        if matched:
            loc_name = matched["name_mr"] if lang == "mr" else matched["name_en"]
            return {
                "lat": matched["lat"],
                "lon": matched["lon"],
                "location_name": loc_name,
                "method": "district_select"
            }

        # 3. Geocoding search (OpenStreetMap Nominatim for any Indian village or town)
        try:
            geo_results = GeocodingService.search_location(clean_city, lang)
            if geo_results and len(geo_results) > 0:
                top = geo_results[0]
                loc_name = top.get("village") or top.get("district") or clean_city
                return {
                    "lat": float(top["latitude"]),
                    "lon": float(top["longitude"]),
                    "location_name": loc_name,
                    "method": "geocoded_search"
                }
        except Exception as e:
            logger.warning(f"Geocoding search failed for {clean_city}: {e}")

    # 4. Client IP Geolocation fallback
    client_ip = None
    if request:
        client_ip = request.headers.get("x-forwarded-for", "").split(",")[0].strip() or (request.client.host if request.client else None)
    ip_loc = _detect_location_from_ip(client_ip)
    if ip_loc:
        return {
            "lat": ip_loc["latitude"],
            "lon": ip_loc["longitude"],
            "location_name": ip_loc["city"],
            "method": "auto_ip"
        }

    # 5. Default regional agro-hub (Kolhapur)
    default_name = "कोल्हापूर" if lang == "mr" else "Kolhapur"
    return {
        "lat": 16.7050,
        "lon": 74.2433,
        "location_name": default_name,
        "method": "regional_default"
    }


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
    1. Device GPS coordinates (highest accuracy)
    2. Explicit city / district / taluka selection
    3. Automatic IP Geolocation (falls back to farmer's regional center)
    """
    api_key = getattr(settings, "WEATHER_API_KEY", None) or "58f50b7f998a3e7f90d73d87f6534183"
    loc = _resolve_location_params(city=city, lat=lat, lon=lon, lang=lang, request=request)
    
    resolved_lat = loc["lat"]
    resolved_lon = loc["lon"]
    loc_name = loc["location_name"]
    detection_method = loc["method"]

    if api_key and api_key != "your_openweather_api_key_here":
        try:
            weather_lang = "mr" if lang == "mr" else "en"
            params = urllib.parse.urlencode({
                "lat": resolved_lat,
                "lon": resolved_lon,
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
                    
                    raw_desc = (weather_list[0].get("description", "Clear sky") if weather_list else "Clear sky").lower()
                    cond_display = WEATHER_DESC_MR.get(raw_desc, raw_desc.title()) if lang == "mr" else raw_desc.title()

                    temp_val = round(float(main.get("temp", 26.5)), 1)
                    humidity_val = round(float(main.get("humidity", 65.0)), 1)
                    rain_val = round(float(rain.get("1h", rain.get("3h", 0.0))), 1)
                    wind_val = round(float(wind.get("speed", 3.0)) * 3.6, 1)

                    advisory = _calculate_spray_advisory(temp_val, humidity_val, wind_val, rain_val, lang)

                    return {
                        "location": loc_name,
                        "temperature_c": temp_val,
                        "humidity_pct": humidity_val,
                        "rainfall_mm": rain_val,
                        "condition": cond_display,
                        "wind_speed_kmh": wind_val,
                        "latitude": float(resolved_lat),
                        "longitude": float(resolved_lon),
                        "is_gps": detection_method == "device_gps",
                        "detection_method": detection_method,
                        "spraying_advisory": advisory,
                        "live_api": True
                    }
        except Exception as e:
            logger.warning(f"OpenWeatherMap API warning for {loc_name} ({resolved_lat},{resolved_lon}): {e}")

    # Fallback response
    temp_val = 26.5
    humidity_val = 45.0
    rain_val = 0.0
    wind_val = 8.0
    advisory = _calculate_spray_advisory(temp_val, humidity_val, wind_val, rain_val, lang)

    return {
        "location": loc_name,
        "temperature_c": temp_val,
        "humidity_pct": humidity_val,
        "rainfall_mm": rain_val,
        "condition": "निरभ्र आकाश (Clear Sky)" if lang == "mr" else "Clear Sky",
        "wind_speed_kmh": wind_val,
        "latitude": float(resolved_lat),
        "longitude": float(resolved_lon),
        "is_gps": detection_method == "device_gps",
        "detection_method": detection_method,
        "spraying_advisory": advisory,
        "live_api": False
    }


@router.get("/forecast")
def get_weather_forecast(
    request: Request,
    city: Optional[str] = Query(None, description="City or district name"),
    lat: Optional[float] = Query(None, description="GPS Latitude"),
    lon: Optional[float] = Query(None, description="GPS Longitude"),
    lang: str = Query("en", description="Language code (en or mr)")
) -> Dict[str, Any]:
    """
    Returns a 5-day daily agricultural forecast including:
    - Min/Max temperature
    - Humidity
    - Rain probability & expected precipitation
    - Agricultural foliar spraying advisory for each day
    """
    api_key = getattr(settings, "WEATHER_API_KEY", None) or "58f50b7f998a3e7f90d73d87f6534183"
    loc = _resolve_location_params(city=city, lat=lat, lon=lon, lang=lang, request=request)
    
    resolved_lat = loc["lat"]
    resolved_lon = loc["lon"]
    loc_name = loc["location_name"]

    daily_forecasts: List[Dict[str, Any]] = []

    if api_key and api_key != "your_openweather_api_key_here":
        try:
            weather_lang = "mr" if lang == "mr" else "en"
            params = urllib.parse.urlencode({
                "lat": resolved_lat,
                "lon": resolved_lon,
                "appid": api_key,
                "units": "metric",
                "lang": weather_lang
            })

            url = f"https://api.openweathermap.org/data/2.5/forecast?{params}"
            req = urllib.request.Request(url, headers={"User-Agent": "AgroScanAI/1.0"})

            with urllib.request.urlopen(req, timeout=6) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    grouped: Dict[str, List[Any]] = {}
                    for item in data.get("list", []):
                        d_str = item.get("dt_txt", "").split(" ")[0]
                        if d_str:
                            grouped.setdefault(d_str, []).append(item)

                    for d_str, items in list(grouped.items())[:5]:
                        temps = [it["main"]["temp"] for it in items if "main" in it]
                        humidities = [it["main"]["humidity"] for it in items if "main" in it]
                        winds = [it.get("wind", {}).get("speed", 0.0) * 3.6 for it in items]
                        pops = [it.get("pop", 0.0) for it in items]
                        rain_vals = [it.get("rain", {}).get("3h", 0.0) for it in items]

                        max_t = round(max(temps), 1) if temps else 28.0
                        min_t = round(min(temps), 1) if temps else 18.0
                        avg_h = round(sum(humidities) / len(humidities), 1) if humidities else 50.0
                        max_w = round(max(winds), 1) if winds else 10.0
                        max_pop = round(max(pops) * 100) if pops else 0
                        tot_rain = round(sum(rain_vals), 1)

                        mid_item = items[len(items) // 2]
                        raw_desc = (mid_item.get("weather", [{}])[0].get("description", "Clear sky")).lower()
                        cond_display = WEATHER_DESC_MR.get(raw_desc, raw_desc.title()) if lang == "mr" else raw_desc.title()

                        try:
                            dt_obj = datetime.strptime(d_str, "%Y-%m-%d")
                            raw_day = dt_obj.strftime("%A")
                            day_name = DAY_NAME_MR.get(raw_day, raw_day) if lang == "mr" else raw_day
                            date_display = dt_obj.strftime("%d %b")
                        except Exception:
                            day_name = d_str
                            date_display = d_str

                        spray = _calculate_spray_advisory(max_t, avg_h, max_w, tot_rain, lang)

                        daily_forecasts.append({
                            "date": d_str,
                            "date_display": date_display,
                            "day_name": day_name,
                            "temp_max": max_t,
                            "temp_min": min_t,
                            "humidity_pct": avg_h,
                            "wind_speed_kmh": max_w,
                            "rain_probability_pct": max_pop,
                            "rainfall_mm": tot_rain,
                            "condition": cond_display,
                            "spraying_advisory": spray
                        })
        except Exception as e:
            logger.warning(f"OpenWeatherMap forecast API warning: {e}")

    return {
        "location": loc_name,
        "latitude": resolved_lat,
        "longitude": resolved_lon,
        "forecast": daily_forecasts
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
