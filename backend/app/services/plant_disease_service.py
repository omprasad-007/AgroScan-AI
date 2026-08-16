import httpx
from typing import Dict, Any
from app.core.config import settings

class PlantDiseaseService:
    """
    Plant Identification & Disease Detection Service using Plant.id API.
    Normalizes responses and provides timeout/error handling.
    """
    PLANT_ID_URL = "https://api.plant.id/v2/identify"

    @classmethod
    def identify_and_diagnose(cls, image_bytes: bytes) -> Dict[str, Any]:
        """
        Sends image to Plant.id API or falls back cleanly if key is unconfigured or in DEMO_MODE.
        Returns normalized dictionary:
        {
            "crop": str,
            "scientific_name": str,
            "disease_name": str,
            "disease_code": str,
            "confidence": float,
            "is_demo": bool,
            "raw_response": dict
        }
        """
        if settings.DEMO_MODE or not settings.PLANT_ID_API_KEY:
            return cls._get_demo_fallback(image_bytes)

        try:
            import base64
            b64_img = base64.b64encode(image_bytes).decode('utf-8')
            headers = {
                "Content-Type": "application/json",
                "Api-Key": settings.PLANT_ID_API_KEY
            }
            payload = {
                "images": [f"data:image/jpeg;base64,{b64_img}"],
                "modifiers": ["crops_fast", "health_all"],
                "plant_language": "en",
                "plant_details": ["common_names", "url", "taxonomy"]
            }

            with httpx.Client(timeout=10.0) as client:
                response = client.post(cls.PLANT_ID_URL, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    return cls._normalize_api_response(data)
                else:
                    return cls._get_demo_fallback(image_bytes, note=f"Plant.id API HTTP {response.status_code}")
        except Exception as e:
            return cls._get_demo_fallback(image_bytes, note=f"Plant.id API error: {str(e)}")

    @classmethod
    def _normalize_api_response(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        suggestions = data.get("suggestions", [])
        health_assessment = data.get("health_assessment", {})

        crop = "Tomato"
        scientific_name = "Solanum lycopersicum"
        confidence = 0.92

        if suggestions:
            top = suggestions[0]
            crop = top.get("plant_name", crop)
            scientific_name = top.get("plant_details", {}).get("scientific_name", scientific_name)
            confidence = round(float(top.get("probability", confidence)), 4)

        disease_name = "Healthy Leaf (No Disease)"
        disease_code = "healthy_leaf"

        diseases = health_assessment.get("diseases", [])
        if diseases:
            top_dis = diseases[0]
            disease_name = top_dis.get("name", disease_name)
            disease_code = disease_name.lower().replace(" ", "_")

        return {
            "crop": crop,
            "scientific_name": scientific_name,
            "disease_name": disease_name,
            "disease_code": disease_code,
            "confidence": confidence,
            "is_demo": False,
            "raw_response": data
        }

    @classmethod
    def _get_demo_fallback(cls, image_bytes: bytes, note: str = "") -> Dict[str, Any]:
        from app.services.model_service import DemoPredictor
        predictor = DemoPredictor()
        res = predictor.predict(image_bytes)
        res["scientific_name"] = "Solanum lycopersicum" if res["crop"] == "Tomato" else "Solanum tuberosum"
        if note:
            res["note"] = note
        return res
