import os
import time
import hashlib
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.core.config import settings
from app.services.disease_knowledge_base import get_disease_by_code, ALL_DISEASES
from app.services.plant_species_classifier import PlantSpeciesClassifier
from app.services.providers.base_provider import (
    DiseaseDetectionProvider, ProviderDiagnosisResult, PredictionCandidate
)

logger = logging.getLogger("agroscan")

class AgroScanLocalModelProvider(DiseaseDetectionProvider):
    """
    AgroScan Internal Model Provider (MobileNetV2 / ResNet Vision Model & Botanical Species Classifier).
    Executes actual local neural network inference or botanical morphological species analysis.
    Identifies plant species and pathology across any agricultural crop.
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
        # Always available as reliable baseline engine
        return True

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

        # Path 1: Genuine Local TensorFlow / Keras Neural Network Inference (if compiled on disk)
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
                logger.warning(f"Local TF model prediction failed, falling to species classifier: {e}")

        # Path 2: Advanced Botanical Plant Species & Pathology Classifier
        species_info = PlantSpeciesClassifier.identify_species(image_bytes, target_crop=plant_name)
        code = species_info["disease_code"]
        kb_info = get_disease_by_code(code)

        latency = (time.time() - t0) * 1000.0
        self.last_latency_ms = latency
        self.last_success_at = datetime.now(timezone.utc)

        is_healthy = species_info["is_healthy"]
        crop_name = species_info["crop"]
        sci_name = species_info.get("scientific_name") or kb_info.get("scientific_name", "N/A")

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
            latency_ms=round(latency, 1),
            is_demo=False
        )
