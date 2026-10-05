import time
import httpx
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from app.core.config import settings
from app.services.providers.base_provider import (
    DiseaseDetectionProvider, ProviderDiagnosisResult, PredictionCandidate
)

logger = logging.getLogger("agroscan")

class PlantixProvider(DiseaseDetectionProvider):
    """
    Plantix Intelligence / Crop Health API Provider.
    Official Documentation: https://b2b.plantix.net/
    Specialized in Indian field agriculture, crop disease diagnosis, non-crop rejection, and nutrient deficiency detection.
    """
    API_URL = "https://api.plantix.net/v2/image_analysis"

    def __init__(self):
        super().__init__(name="plantix", display_name="Plantix Crop Health API")

    def is_available(self) -> bool:
        return bool(settings.PLANTIX_API_KEY) and not getattr(settings, "DEMO_MODE", False)

    async def diagnose(
        self,
        image_bytes: bytes,
        plant_name: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None,
        language: str = "en"
    ) -> ProviderDiagnosisResult:
        self.total_calls += 1
        t0 = time.time()

        if not self.is_available():
            return ProviderDiagnosisResult(
                provider=self.name,
                status="not_configured",
                plant="Unknown",
                disease="Unknown",
                disease_code="unconfigured_provider",
                confidence=0.0,
                error="Plantix API key (PLANTIX_API_KEY) is not configured in backend environment."
            )

        api_key = settings.PLANTIX_API_KEY
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        try:
            files = {"image": ("leaf.jpg", image_bytes, "image/jpeg")}
            data = {}
            if plant_name and plant_name != "Crop":
                data["crop"] = plant_name
            if location:
                if location.get("latitude"):
                    data["latitude"] = str(location["latitude"])
                if location.get("longitude"):
                    data["longitude"] = str(location["longitude"])

            async with httpx.AsyncClient(timeout=6.0) as client:
                res = await client.post(self.API_URL, headers=headers, files=files, data=data)
                latency = (time.time() - t0) * 1000.0
                self.last_latency_ms = latency

                if res.status_code == 200:
                    payload = res.json()
                    parsed = self._parse_response(payload, latency)
                    if parsed:
                        self.last_success_at = datetime.utcnow()
                        return parsed
                elif res.status_code == 400:
                    data = res.json()
                    err_msg = data.get("message") or "Plantix rejected image as non-crop or unreadable."
                    return ProviderDiagnosisResult(
                        provider=self.name,
                        status="non_leaf_detected",
                        plant="Non-Crop",
                        disease="Non-Crop",
                        disease_code="non_crop",
                        confidence=0.0,
                        latency_ms=round(latency, 1),
                        error=err_msg
                    )
                else:
                    self.failure_count += 1
                    return ProviderDiagnosisResult(
                        provider=self.name,
                        status="error",
                        plant="Unknown",
                        disease="Unknown",
                        disease_code="provider_error",
                        confidence=0.0,
                        latency_ms=round(latency, 1),
                        error=f"Plantix API returned HTTP {res.status_code}"
                    )

        except Exception as e:
            self.failure_count += 1
            latency = (time.time() - t0) * 1000.0
            self.last_latency_ms = latency
            logger.warning(f"Plantix provider error: {e}")
            return ProviderDiagnosisResult(
                provider=self.name,
                status="error",
                plant="Unknown",
                disease="Unknown",
                disease_code="provider_error",
                confidence=0.0,
                latency_ms=round(latency, 1),
                error=f"Plantix request failed: {e}"
            )

    def _parse_response(self, data: Dict[str, Any], latency: float) -> Optional[ProviderDiagnosisResult]:
        # Handle non-crop / image problems
        if not data.get("crop_detected", True):
            return ProviderDiagnosisResult(
                provider=self.name,
                status="non_leaf_detected",
                plant="Non-Crop",
                disease="Non-Crop",
                disease_code="non_crop",
                confidence=0.0,
                latency_ms=round(latency, 1),
                error="Plantix detected a non-crop or non-agricultural image."
            )

        crop = data.get("crop", "General Crop").title()
        diagnoses = data.get("predicted_diseases", []) or data.get("diagnoses", [])
        
        candidates = []
        for diag in diagnoses[:4]:
            d_name = diag.get("name", "Leaf Spot").title()
            conf = round(float(diag.get("probability", diag.get("confidence", 0.75))), 3)
            code = d_name.lower().replace(" ", "_").replace("-", "_")
            is_healthy = "healthy" in d_name.lower()
            candidates.append(PredictionCandidate(
                crop=crop,
                disease_name=d_name,
                disease_code=code,
                confidence=conf,
                is_healthy=is_healthy,
                scientific_name=diag.get("pathogen_scientific_name")
            ))

        if candidates:
            primary = candidates[0]
            return ProviderDiagnosisResult(
                provider=self.name,
                status="success",
                plant=crop,
                scientific_name=primary.scientific_name or "N/A",
                disease=primary.disease_name,
                disease_code=primary.disease_code,
                confidence=primary.confidence,
                is_healthy=primary.is_healthy,
                top_predictions=candidates,
                latency_ms=round(latency, 1)
            )
        else:
            return ProviderDiagnosisResult(
                provider=self.name,
                status="success",
                plant=crop,
                scientific_name="N/A",
                disease="Healthy Leaf (No Disease Detected)",
                disease_code="healthy_leaf",
                confidence=0.90,
                is_healthy=True,
                latency_ms=round(latency, 1)
            )
