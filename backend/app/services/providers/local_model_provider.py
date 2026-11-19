"""
AgroScan AI — Local Model Provider
Executes local neural network evaluation using Hugging Face MobileNetV2 (PlantVillage v1.1).
Augmented with Botanical Morphology classifier for explicit non-MobileNetV2 crop coverage.
"""

import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from app.core.config import settings
from app.services.disease_knowledge_base import get_disease_by_code
from app.services.crop_registry import (
    get_crop_support,
    is_crop_supported_by_local_model,
    CropSupportStatus
)
from app.services.plant_species_classifier import PlantSpeciesClassifier
from app.services.plant_disease_model import (
    local_model_service,
    ModelPredictionResult,
    PredictionCandidate as ModelCandidate
)
from app.services.providers.base_provider import (
    DiseaseDetectionProvider,
    ProviderDiagnosisResult,
    PredictionCandidate,
    ProviderHealthStatus
)

logger = logging.getLogger("agroscan.providers.local")


class AgroScanLocalModelProvider(DiseaseDetectionProvider):
    """
    AgroScan Local Model Provider.
    Primary: Hugging Face MobileNetV2 (PlantVillage v1.1, Safetensors weights, 38 classes).
    Secondary: Botanical Species & Pathology Classifier for non-PlantVillage crops.
    """

    def __init__(self):
        super().__init__(name="agroscan_local", display_name="AgroScan Local Vision Engine")
        self.model_service = local_model_service

    def is_available(self) -> bool:
        # Local model is available if weights are present locally or already loaded
        return self.model_service.has_weights() or self.model_service.is_loaded

    def get_health_status(self) -> ProviderHealthStatus:
        base = super().get_health_status()
        meta = self.model_service.get_model_metadata()
        model_name = meta.get("model_name", "Vision Transformer")
        base.display_name = f"AgroScan Local Vision Engine ({model_name})"
        base.notes = (
            f"{model_name} ({meta.get('revision', 'latest')[:10]}) - "
            f"Loaded: {meta.get('is_loaded')}, Classes: {meta.get('num_classes', 38)}, "
            f"Device: {meta.get('device', 'cpu')}"
        )
        base.supported_crops = [
            "apple", "blueberry", "cherry", "corn", "grape", "orange",
            "peach", "pepper", "potato", "raspberry", "soybean",
            "squash", "strawberry", "tomato"
        ]
        return base

    async def diagnose(
        self,
        image_bytes: bytes,
        plant_name: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None,
        language: str = "en"
    ) -> ProviderDiagnosisResult:
        self.total_calls += 1
        t0 = time.time()

        # Lazy load weights on first inference request if available
        if self.model_service.has_weights() and not self.model_service.is_loaded:
            try:
                self.model_service.load_model()
            except Exception as e:
                logger.warning(f"Lazy load of MobileNetV2 failed: {e}")

        # Step 1: Check target crop support status
        is_target_specified = bool(plant_name and plant_name.lower() != "auto")
        is_target_mobilenet_supported = is_crop_supported_by_local_model(plant_name) if is_target_specified else True

        # Path 1: Execute Genuine MobileNetV2 Neural Network Inference
        if not is_target_specified or is_target_mobilenet_supported:
            try:
                res: ModelPredictionResult = self.model_service.predict_disease(
                    image_bytes,
                    target_crop=plant_name if is_target_specified else None
                )

                latency = (time.time() - t0) * 1000.0
                self.last_latency_ms = latency
                self.last_success_at = datetime.now(timezone.utc)

                kb_info = get_disease_by_code(res.disease_code)
                sci_name = kb_info.get("scientific_name") or res.top_prediction.scientific_name or "N/A"

                top_candidates: List[PredictionCandidate] = []
                for c in res.top_predictions:
                    top_candidates.append(
                        PredictionCandidate(
                            crop=c.crop,
                            disease_name=c.disease_name,
                            disease_code=c.canonical_disease_code,
                            confidence=c.calibrated_score,
                            is_healthy=c.is_healthy,
                            scientific_name=c.scientific_name
                        )
                    )

                warnings = []
                if res.is_uncertain:
                    warnings.append(
                        res.uncertainty_note or "Confidence score is below calibrated decision threshold."
                    )

                return ProviderDiagnosisResult(
                    provider=self.name,
                    status="success" if not res.is_uncertain else "uncertain",
                    plant=res.crop_detected,
                    scientific_name=sci_name,
                    disease=res.disease_name,
                    disease_code=res.disease_code,
                    confidence=res.confidence,
                    is_healthy=res.is_healthy,
                    top_predictions=top_candidates,
                    warnings=warnings,
                    latency_ms=round(latency, 1),
                    is_demo=False
                )

            except Exception as e:
                logger.warning(f"MobileNetV2 inference failed: {e}. Falling to botanical classifier.")
                self.failure_count += 1

        # Path 2: Advanced Botanical Plant Species & Pathology Classifier
        # Used for explicit non-MobileNetV2 crops (Sugarcane, Cotton, Rice, Wheat, Mango, etc.)
        crop_entry = get_crop_support(plant_name)
        species_info = PlantSpeciesClassifier.identify_species(image_bytes, target_crop=plant_name)
        code = species_info["disease_code"]
        kb_info = get_disease_by_code(code)

        latency = (time.time() - t0) * 1000.0
        self.last_latency_ms = latency
        self.last_success_at = datetime.now(timezone.utc)

        is_healthy = species_info["is_healthy"]
        crop_name = species_info["crop"]
        sci_name = species_info.get("scientific_name") or kb_info.get("scientific_name", "N/A")

        warnings = []
        if is_target_specified and not is_target_mobilenet_supported:
            warnings.append(
                f"Crop '{crop_name}' is outside MobileNetV2's 14 native PlantVillage crops. "
                f"Diagnosed using AgroScan Botanical Morphology Classifier."
            )

        return ProviderDiagnosisResult(
            provider=self.name,
            status="success",
            plant=crop_name,
            scientific_name=sci_name,
            disease=species_info["disease_name"],
            disease_code=code,
            confidence=species_info["confidence"],
            is_healthy=is_healthy,
            top_predictions=[
                PredictionCandidate(
                    crop=crop_name,
                    disease_name=species_info["disease_name"],
                    disease_code=code,
                    confidence=species_info["confidence"],
                    is_healthy=is_healthy,
                    scientific_name=sci_name
                )
            ],
            warnings=warnings,
            latency_ms=round(latency, 1),
            is_demo=False
        )
