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

class TajiriVisionProvider(DiseaseDetectionProvider):
    """
    Tajiri Vision Plant Diagnosis API Integration.
    Official Documentation: https://docs.tajiri.farm/
    Specialized in crop growth stage, tropical/subtropical crop pathology, and visual symptom analysis.
    """
    API_URL = "https://api.tajiri.farm/v1/vision/diagnose"

    def __init__(self):
        super().__init__(name="tajiri", display_name="Tajiri Vision API")

    def is_available(self) -> bool:
        return bool(settings.TAJIRI_API_KEY) and not getattr(settings, "DEMO_MODE", False)

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
                error="Tajiri API key (TAJIRI_API_KEY) is not configured in backend environment."
            )

        api_key = settings.TAJIRI_API_KEY
        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            files = {"image": ("leaf.jpg", image_bytes, "image/jpeg")}
            data = {"region": "south_asia", "language": language}
            if plant_name and plant_name != "Crop":
                data["crop_type"] = plant_name

            async with httpx.AsyncClient(timeout=14.0) as client:
                res = await client.post(self.API_URL, headers=headers, files=files, data=data)
                latency = (time.time() - t0) * 1000.0
                self.last_latency_ms = latency

                if res.status_code == 200:
                    payload = res.json()
                    parsed = self._parse_response(payload, latency)
                    if parsed:
                        self.last_success_at = datetime.utcnow()
                        return parsed
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
                        error=f"Tajiri API responded with HTTP {res.status_code}"
                    )

        except Exception as e:
            self.failure_count += 1
            latency = (time.time() - t0) * 1000.0
            self.last_latency_ms = latency
            logger.warning(f"Tajiri Vision provider error: {e}")
            return ProviderDiagnosisResult(
                provider=self.name,
                status="error",
                plant="Unknown",
                disease="Unknown",
                disease_code="provider_error",
                confidence=0.0,
                latency_ms=round(latency, 1),
                error=f"Tajiri request failed: {e}"
            )

    def _parse_response(self, data: Dict[str, Any], latency: float) -> Optional[ProviderDiagnosisResult]:
        crop = data.get("crop", "General Crop").title()
        diagnoses = data.get("diagnoses", []) or data.get("results", [])

        candidates = []
        for d in diagnoses[:4]:
            d_name = d.get("condition", d.get("name", "Leaf Spot")).title()
            conf = round(float(d.get("confidence", 0.70)), 3)
            code = d_name.lower().replace(" ", "_").replace("-", "_")
            is_healthy = "healthy" in d_name.lower()
            candidates.append(PredictionCandidate(
                crop=crop,
                disease_name=d_name,
                disease_code=code,
                confidence=conf,
                is_healthy=is_healthy
            ))

        if candidates:
            primary = candidates[0]
            return ProviderDiagnosisResult(
                provider=self.name,
                status="success",
                plant=crop,
                scientific_name="N/A",
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
                confidence=0.91,
                is_healthy=True,
                latency_ms=round(latency, 1)
            )
