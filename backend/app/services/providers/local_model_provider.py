import os
import time
import hashlib
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.core.config import settings
from app.services.disease_knowledge_base import get_disease_by_code, ALL_DISEASES
from app.services.providers.base_provider import (
    DiseaseDetectionProvider, ProviderDiagnosisResult, PredictionCandidate
)

logger = logging.getLogger("agroscan")

class AgroScanLocalModelProvider(DiseaseDetectionProvider):
    """
    AgroScan Internal Model Provider (MobileNetV2 / ResNet Vision Model).
    Executes actual local neural network inference when model binary is compiled on disk.
    Never fabricates hardcoded diagnoses or manufactures fake confidence scores in production.
    """

    def __init__(self):
        super().__init__(name="agroscan_local", display_name="AgroScan Local Vision Engine")
        self.model = None
        self._model_loaded = False

    def _try_load_model(self):
        if not self._model_loaded:
            model_path = getattr(settings, "MODEL_PATH", "ml/models/plant_disease_model_v1.h5")
            if os.path.exists(model_path):
                try:
                    import importlib.util
                    if importlib.util.find_spec("tensorflow") is not None:
                        import tensorflow as tf  # type: ignore
                        self.model = tf.keras.models.load_model(model_path)
                        logger.info(f"Loaded local neural network model from {model_path}")
                except Exception as e:
                    logger.warning(f"Local TensorFlow model failed to load from {model_path}: {e}")
            self._model_loaded = True

    def is_available(self) -> bool:
        self._try_load_model()
        if self.model is not None:
            return True
        # Only available without compiled model if explicitly running in DEMO_MODE
        return bool(getattr(settings, "DEMO_MODE", False))

    async def diagnose(
        self,
        image_bytes: bytes,
        plant_name: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None,
        language: str = "en"
    ) -> ProviderDiagnosisResult:
        self.total_calls += 1
        t0 = time.time()
        self._try_load_model()

        # Path 1: Genuine Local TensorFlow / Keras Neural Network Inference
        if self.model is not None:
            try:
                from PIL import Image
                import io
                import numpy as np

                pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))
                img_arr = np.array(pil_img, dtype=np.float32) / 255.0
                img_tensor = np.expand_dims(img_arr, axis=0)

                preds = self.model.predict(img_tensor)[0]
                classes = [
                    "tomato_early_blight", "tomato_late_blight", "tomato_yellow_leaf_curl",
                    "potato_late_blight", "corn_common_rust", "healthy_leaf"
                ]
                top_idx = int(np.argmax(preds))
                confidence = round(float(preds[top_idx]), 3)
                code = classes[top_idx]
                info = get_disease_by_code(code)

                latency = (time.time() - t0) * 1000.0
                self.last_latency_ms = latency
                self.last_success_at = datetime.now(timezone.utc)

                is_healthy = code == "healthy_leaf"
                return ProviderDiagnosisResult(
                    provider=self.name,
                    status="success",
                    plant=info["crop"],
                    scientific_name=info.get("scientific_name", "N/A"),
                    disease=info["disease_name"],
                    disease_code=code,
                    confidence=confidence,
                    is_healthy=is_healthy,
                    top_predictions=[
                        PredictionCandidate(
                            crop=info["crop"],
                            disease_name=info["disease_name"],
                            disease_code=code,
                            confidence=confidence,
                            is_healthy=is_healthy,
                            scientific_name=info.get("scientific_name")
                        )
                    ],
                    latency_ms=round(latency, 1),
                    is_demo=False
                )
            except Exception as e:
                logger.warning(f"Local TF model prediction failed: {e}")
                self.failure_count += 1
                return ProviderDiagnosisResult(
                    provider=self.name,
                    status="error",
                    plant="Unknown",
                    disease="Unknown",
                    disease_code="model_error",
                    confidence=0.0,
                    error=f"Local neural network inference failed: {e}",
                    latency_ms=round((time.time() - t0) * 1000.0, 1)
                )

        # Path 2: Production Safe Handling when no model file exists
        if not getattr(settings, "DEMO_MODE", False):
            self.failure_count += 1
            return ProviderDiagnosisResult(
                provider=self.name,
                status="model_unavailable",
                plant="Unknown",
                disease="Unknown",
                disease_code="local_model_unavailable",
                confidence=0.0,
                error="Local MobileNet model binary is not installed on this server. External AI disease providers must be configured.",
                latency_ms=round((time.time() - t0) * 1000.0, 1),
                is_demo=False
            )

        # Path 3: Explicit DEMO_MODE fallback (only active when settings.DEMO_MODE is True)
        # Uses full image SHA-256 hash (never sum of first 64 bytes) to ensure different images yield diverse results
        img_sha = hashlib.sha256(image_bytes).hexdigest()
        hash_seed = int(img_sha[:8], 16)
        
        target_crop = (plant_name or "").strip().title()
        matching_diseases = []
        if target_crop and target_crop not in ["Crop", "General", "General Crop", "Unknown"]:
            for d in ALL_DISEASES:
                if target_crop.lower() in d["crop"].lower() or d["crop"].lower() in target_crop.lower():
                    matching_diseases.append(d)

        if not matching_diseases:
            matching_diseases = list(ALL_DISEASES)

        idx = hash_seed % len(matching_diseases)
        selected = matching_diseases[idx]

        is_healthy = selected["disease_code"] == "healthy_leaf"
        # Calibrated pseudo-score in demo mode based on full hash
        confidence = round(0.75 + (int(img_sha[8:12], 16) % 200) / 1000.0, 3)

        latency = (time.time() - t0) * 1000.0
        self.last_latency_ms = latency
        self.last_success_at = datetime.now(timezone.utc)

        return ProviderDiagnosisResult(
            provider=self.name,
            status="success",
            plant=selected["crop"],
            scientific_name=selected.get("scientific_name", "N/A"),
            disease=selected["disease_name"],
            disease_code=selected["disease_code"],
            confidence=confidence,
            is_healthy=is_healthy,
            top_predictions=[
                PredictionCandidate(
                    crop=selected["crop"],
                    disease_name=selected["disease_name"],
                    disease_code=selected["disease_code"],
                    confidence=confidence,
                    is_healthy=is_healthy,
                    scientific_name=selected.get("scientific_name")
                )
            ],
            latency_ms=round(latency, 1),
            is_demo=True
        )
