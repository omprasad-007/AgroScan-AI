import httpx
from typing import Dict, Any
from app.core.config import settings
from app.services.disease_knowledge_base import get_crop_cultivation_info

class PlantKnowledgeService:
    """
    Plant Knowledge & Care Service using Perenual Plant API
    combined with AgroScan's local Crop Knowledge System.
    """
    PERENUAL_BASE_URL = "https://perenual.com/api/species-list"

    @classmethod
    def get_plant_details(cls, crop_name: str) -> Dict[str, Any]:
        """
        Fetches botanical & cultivation details for a crop.
        Combines external API data with AgroScan's internal database.
        """
        local_info = get_crop_cultivation_info(crop_name)
        perenual_info = {}

        if settings.PERENUAL_API_KEY and not settings.DEMO_MODE:
            try:
                params = {
                    "key": settings.PERENUAL_API_KEY,
                    "q": crop_name
                }
                with httpx.Client(timeout=8.0) as client:
                    resp = client.get(cls.PERENUAL_BASE_URL, params=params)
                    if resp.status_code == 200:
                        data = resp.json()
                        data_list = data.get("data", [])
                        if data_list:
                            first = data_list[0]
                            perenual_info = {
                                "perenual_id": first.get("id"),
                                "scientific_name": first.get("scientific_name", [local_info.get("scientific_name")])[0],
                                "watering": first.get("watering"),
                                "sunlight": first.get("sunlight", []),
                                "cycle": first.get("cycle")
                            }
            except Exception as e:
                print(f"Perenual API warning: {e}")

        # Merge local AgroScan knowledge base with API metadata
        return {
            "crop": crop_name,
            "scientific_name": perenual_info.get("scientific_name") or local_info.get("scientific_name", "Solanum species"),
            "sunlight": perenual_info.get("sunlight") or [local_info.get("sunlight", "Full Sun")],
            "watering": perenual_info.get("watering") or local_info.get("irrigation_schedule", "Regular moist soil"),
            "soil": local_info.get("soil_type", "Well-drained fertile loam"),
            "sowing_period": local_info.get("sowing_period", "June - July / Oct - Nov"),
            "spacing": local_info.get("spacing", "60cm x 45cm"),
            "fertilization": local_info.get("fertilization", "NPK 120:60:60 kg/ha"),
            "harvest_indicators": local_info.get("harvest_indicators", "Fruit turns firm and uniform red"),
            "harvest_period": local_info.get("harvest_period", "75-90 days after transplanting")
        }
