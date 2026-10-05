import time
import base64
import httpx
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from app.core.config import settings
from app.services.providers.base_provider import (
    DiseaseDetectionProvider, ProviderDiagnosisResult, PredictionCandidate, ProviderHealthStatus
)

logger = logging.getLogger("agroscan")

class KindwisePlantIdProvider(DiseaseDetectionProvider):
    """
    Kindwise / Plant.id AI Provider Integration.
    Supports official v3 identification & v2 health/disease diagnosis.
    """
    V3_API_URL = "https://api.plant.id/v3/identification"
    V2_API_URL = "https://api.plant.id/v2/identify"

    def __init__(self):
        super().__init__(name="kindwise", display_name="Kindwise / Plant.id AI")

    def is_available(self) -> bool:
        return bool(settings.PLANT_ID_API_KEY) and not getattr(settings, "DEMO_MODE", False)

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
                error="Kindwise API key is not configured or DEMO_MODE is active."
            )

        api_key = settings.PLANT_ID_API_KEY
        b64_img = base64.b64encode(image_bytes).decode('utf-8')
        headers = {"Api-Key": api_key, "Content-Type": "application/json"}

        lat = (location.get("latitude") or 16.58) if location else 16.58
        lon = (location.get("longitude") or 74.31) if location else 74.31

        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                # 1. Try Plant.id v3 API
                payload_v3 = {
                    "images": [f"data:image/jpeg;base64,{b64_img}"],
                    "latitude": lat,
                    "longitude": lon,
                    "health": "all",
                    "similar_images": False
                }
                res = await client.post(self.V3_API_URL, headers=headers, json=payload_v3)
                latency = (time.time() - t0) * 1000.0
                self.last_latency_ms = latency

                if res.status_code == 200:
                    data = res.json()
                    parsed = self._parse_v3(data, latency)
                    if parsed:
                        self.last_success_at = datetime.utcnow()
                        return parsed

                # 2. Fallback to v2 if v3 had non-200
                v2_payload = {
                    "images": [b64_img],
                    "modifiers": ["crops_fast", "disease_fast", "health_all"],
                    "plant_details": ["common_names", "taxonomy"]
                }
                res_v2 = await client.post(self.V2_API_URL, headers={"Api-Key": api_key}, json=v2_payload)
                latency_v2 = (time.time() - t0) * 1000.0
                self.last_latency_ms = latency_v2

                if res_v2.status_code == 200:
                    data_v2 = res_v2.json()
                    parsed_v2 = self._parse_v2(data_v2, latency_v2)
                    if parsed_v2:
                        self.last_success_at = datetime.utcnow()
                        return parsed_v2

                self.failure_count += 1
                return ProviderDiagnosisResult(
                    provider=self.name,
                    status="error",
                    plant="Unknown",
                    disease="Unknown",
                    disease_code="provider_error",
                    confidence=0.0,
                    latency_ms=round(latency, 1),
                    error=f"Kindwise API returned HTTP {res.status_code} / {res_v2.status_code}"
                )

        except Exception as e:
            self.failure_count += 1
            latency = (time.time() - t0) * 1000.0
            self.last_latency_ms = latency
            logger.warning(f"Kindwise provider error: {e}")
            return ProviderDiagnosisResult(
                provider=self.name,
                status="error",
                plant="Unknown",
                disease="Unknown",
                disease_code="provider_error",
                confidence=0.0,
                latency_ms=round(latency, 1),
                error=f"Kindwise request failed: {e}"
            )

    def _parse_v3(self, data: Dict[str, Any], latency: float) -> Optional[ProviderDiagnosisResult]:
        res_obj = data.get("result", {})
        
        # Plant check
        is_plant_info = res_obj.get("is_plant", {})
        is_plant_prob = float(is_plant_info.get("probability", 1.0))
        if is_plant_prob < 0.40 or is_plant_info.get("binary") is False:
            return ProviderDiagnosisResult(
                provider=self.name,
                status="non_leaf_detected",
                plant="Non-Plant",
                disease="Non-Plant",
                disease_code="non_plant",
                confidence=0.0,
                latency_ms=round(latency, 1),
                error="Kindwise classifier determined the image does not contain a plant."
            )

        classification = res_obj.get("classification", {})
        suggestions = classification.get("suggestions", [])
        top_crop = "General Crop"
        sci_name = "N/A"
        if suggestions:
            top_sug = suggestions[0]
            sci_name = top_sug.get("name", "N/A")
            common = top_sug.get("details", {}).get("common_names", [])
            top_crop = common[0].title() if common else sci_name.title()

        # Health Assessment
        health_obj = res_obj.get("disease", {}) or res_obj.get("health_assessment", {})
        disease_sugs = health_obj.get("suggestions", [])
        is_healthy = health_obj.get("is_healthy", {}).get("binary", True)

        top_candidates = []
        if disease_sugs and not is_healthy:
            for s in disease_sugs[:4]:
                d_name = s.get("name", "Leaf Spot").title()
                prob = round(float(s.get("probability", 0.70)), 3)
                code = d_name.lower().replace(" ", "_").replace("-", "_")
                top_candidates.append(PredictionCandidate(
                    crop=top_crop,
                    disease_name=d_name,
                    disease_code=code,
                    confidence=prob,
                    is_healthy=False
                ))

        if top_candidates and not is_healthy:
            primary = top_candidates[0]
            return ProviderDiagnosisResult(
                provider=self.name,
                status="success",
                plant=top_crop,
                scientific_name=sci_name,
                disease=primary.disease_name,
                disease_code=primary.disease_code,
                confidence=primary.confidence,
                is_healthy=False,
                top_predictions=top_candidates,
                latency_ms=round(latency, 1)
            )
        else:
            return ProviderDiagnosisResult(
                provider=self.name,
                status="success",
                plant=top_crop,
                scientific_name=sci_name,
                disease="Healthy Leaf (No Disease Detected)",
                disease_code="healthy_leaf",
                confidence=0.95,
                is_healthy=True,
                top_predictions=[PredictionCandidate(
                    crop=top_crop,
                    disease_name="Healthy Leaf (No Disease Detected)",
                    disease_code="healthy_leaf",
                    confidence=0.95,
                    is_healthy=True
                )],
                latency_ms=round(latency, 1)
            )

    def _parse_v2(self, data: Dict[str, Any], latency: float) -> Optional[ProviderDiagnosisResult]:
        suggestions = data.get("suggestions", [])
        if not suggestions:
            return None

        top = suggestions[0]
        plant_name = top.get("plant_name", "General Crop").capitalize()
        details = top.get("plant_details", {})
        scientific = details.get("scientific_name", plant_name)
        diseases = top.get("diseases", [])

        top_candidates = []
        if diseases:
            for d in diseases[:4]:
                d_name = d.get("name", "Leaf Spot").title()
                d_conf = round(float(d.get("probability", 0.70)), 3)
                d_code = d_name.lower().replace(" ", "_")
                top_candidates.append(PredictionCandidate(
                    crop=plant_name,
                    disease_name=d_name,
                    disease_code=d_code,
                    confidence=d_conf,
                    is_healthy=False
                ))

        if top_candidates:
            primary = top_candidates[0]
            return ProviderDiagnosisResult(
                provider=self.name,
                status="success",
                plant=plant_name,
                scientific_name=scientific,
                disease=primary.disease_name,
                disease_code=primary.disease_code,
                confidence=primary.confidence,
                is_healthy=False,
                top_predictions=top_candidates,
                latency_ms=round(latency, 1)
            )
        else:
            return ProviderDiagnosisResult(
                provider=self.name,
                status="success",
                plant=plant_name,
                scientific_name=scientific,
                disease="Healthy Leaf (No Disease Detected)",
                disease_code="healthy_leaf",
                confidence=0.95,
                is_healthy=True,
                latency_ms=round(latency, 1)
            )
