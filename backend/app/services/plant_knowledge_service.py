import logging
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger("agroscan")

class PlantKnowledgeService:
    """
    Service wrapper for Perenual Botanical Care & Cultivation API.
    Never causes primary disease diagnosis to crash if botanical API is unreachable.
    """
    SEARCH_URL = "https://perenual.com/api/species-list"

    @classmethod
    async def get_crop_care_info(cls, crop_name: str) -> Dict[str, Any]:
        api_key = settings.PERENUAL_API_KEY

        if not api_key:
            return cls._get_default_care_fallback(crop_name)

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    cls.SEARCH_URL,
                    params={"key": api_key, "q": crop_name}
                )

                if response.status_code == 200:
                    data = response.json()
                    results = data.get("data", [])
                    if results:
                        top = results[0]
                        return {
                            "crop": crop_name,
                            "scientific_name": top.get("scientific_name", [crop_name])[0],
                            "sunlight": ", ".join(top.get("sunlight", ["Full Sun"])),
                            "watering": top.get("watering", "Average"),
                            "status": "available"
                        }

                logger.warning(f"Perenual API HTTP {response.status_code}. Using fallback info.")
                return cls._get_default_care_fallback(crop_name)

        except Exception as e:
            logger.warn(f"PlantKnowledgeService exception for {crop_name}: {e}")
            return cls._get_default_care_fallback(crop_name)

    @staticmethod
    def _get_default_care_fallback(crop_name: str) -> Dict[str, Any]:
        return {
            "crop": crop_name,
            "scientific_name": f"{crop_name} (Solanum sp.)",
            "sunlight": "Full Sun (6-8 hours daily)",
            "watering": "Regular irrigation at soil level",
            "status": "partially_available",
            "notice": "Additional plant information is temporarily unavailable."
        }
