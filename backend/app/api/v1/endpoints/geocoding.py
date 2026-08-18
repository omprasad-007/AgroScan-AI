from fastapi import APIRouter, Query
from typing import List, Dict, Any
from app.services.geocoding_service import GeocodingService

router = APIRouter()

@router.get("/search", response_model=List[Dict[str, Any]])
def search_location(
    q: str = Query("", description="Query for searching village, town, district, or state"),
    lang: str = Query("en", description="Language code e.g. mr or en")
):
    return GeocodingService.search_location(q, lang=lang)

@router.get("/reverse", response_model=Dict[str, Any])
def reverse_geocode(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    lang: str = Query("en", description="Language code e.g. mr or en")
):
    return GeocodingService.reverse_geocode(lat, lon, lang=lang)
