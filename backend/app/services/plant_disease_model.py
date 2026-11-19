"""
AgroScan AI — Local Plant Disease Classification Inference Service
Hugging Face MobileNetV2 (neghani/plantvillage-mobilenetv2, revision v1.1)

Executes genuine, deterministic neural network evaluation in PyTorch inference mode.
Features:
- Thread-safe singleton model lifecycle
- Offline local execution (zero outbound calls during inference)
- Exact model label mapping across 38 PlantVillage classes
- Temperature-scaled calibration (T = 0.8845188130635788 from calibration.json)
- Statistical threshold gating (threshold = 0.50 from threshold.json)
- Top-3 candidate ranking with calibrated and raw probability scores
- Crop coverage validation and uncertainty detection
"""

import io
import os
import json
import time
import logging
import threading
from typing import Dict, List, Any, Optional, Union, Tuple
from pydantic import BaseModel, Field
from PIL import Image
import numpy as np

# Lazy-loaded ML imports to preserve memory in constrained cloud environments (e.g. Render 512MB RAM)
_torch = None
_AutoImageProcessor = None
_AutoModelForImageClassification = None

def _get_torch():
    global _torch
    if _torch is None:
        try:
            import torch
            _torch = torch
        except Exception as e:
            logger.info(f"PyTorch runtime not available in this environment: {e}")
            _torch = None
    return _torch

def _get_transformers():
    global _AutoImageProcessor, _AutoModelForImageClassification
    if _AutoImageProcessor is None or _AutoModelForImageClassification is None:
        try:
            from transformers import AutoImageProcessor, AutoModelForImageClassification
            _AutoImageProcessor = AutoImageProcessor
            _AutoModelForImageClassification = AutoModelForImageClassification
        except Exception as e:
            logger.info(f"Transformers runtime not available in this environment: {e}")
            _AutoImageProcessor = None
            _AutoModelForImageClassification = None
    return _AutoImageProcessor, _AutoModelForImageClassification

from app.services.crop_registry import (
    get_crop_support,
    is_crop_supported_by_local_model,
    CropSupportStatus
)

logger = logging.getLogger("agroscan.model")

# Standard paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCAL_MODEL_DIR = os.path.join(BASE_DIR, "backend", "models", "plantvillage-mobilenetv2")
if not os.path.exists(LOCAL_MODEL_DIR):
    # Fallback if working directory is already inside backend/
    ALT_DIR = os.path.join(BASE_DIR, "models", "plantvillage-mobilenetv2")
    if os.path.exists(ALT_DIR):
        LOCAL_MODEL_DIR = ALT_DIR

MANIFEST_PATH = os.path.join(os.path.dirname(LOCAL_MODEL_DIR), "model_manifest.json")


class PredictionCandidate(BaseModel):
    index: int
    raw_label: str
    crop: str
    disease_name: str
    canonical_disease_code: str
    raw_score: float
    calibrated_score: float
    is_healthy: bool
    scientific_name: Optional[str] = None


class ModelPredictionResult(BaseModel):
    status: str  # "DISEASE_DETECTED", "HEALTHY", "UNCERTAIN", "UNSUPPORTED_CROP", "ERROR"
    top_prediction: PredictionCandidate
    top_predictions: List[PredictionCandidate]
    crop_detected: str
    disease_name: str
    disease_code: str
    confidence: float
    raw_score: float
    calibrated_score: float
    is_calibrated: bool
    temperature_applied: float
    threshold_applied: float
    is_healthy: bool
    is_uncertain: bool
    uncertainty_note: Optional[str] = None
    crop_support_status: str
    latency_ms: float
    model_name: str = "MobileNetV2 (PlantVillage v1.1)"
    model_revision: str = "v1.1"
    commit_sha: str = "77e6d262dca53b818f7ad1d67088700754515639"
    device: str = "cpu"


class PlantDiseaseModelService:
    """
    Singleton service managing local MobileNetV2 PyTorch model inference.
    """
    _instance: Optional["PlantDiseaseModelService"] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(PlantDiseaseModelService, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_dir: Optional[str] = None):
        if self._initialized:
            return
        
        self.model_dir = model_dir or LOCAL_MODEL_DIR
        self.device = "cpu"  # String representation initially to avoid importing torch at module load
        self.model = None
        self.processor = None
        self.id2label: Dict[str, str] = {}
        self.label2id: Dict[str, int] = {}
        self.temperature: float = 0.8845188130635788  # From calibration.json
        self.threshold: float = 0.50                  # From threshold.json
        self.manifest: Dict[str, Any] = {}
        self.is_loaded: bool = False
        self.load_error: Optional[str] = None
        self.load_duration_ms: float = 0.0

        # Attempt safe initial loading (loads JSON metadata only, zero torch dependency)
        self._load_metadata()
        self._initialized = True

    def has_weights(self) -> bool:
        """Returns True if local weights and config exist on disk."""
        if not os.path.exists(self.model_dir):
            return False
        weights_path = os.path.join(self.model_dir, "model.safetensors")
        config_path = os.path.join(self.model_dir, "config.json")
        return os.path.exists(weights_path) and os.path.exists(config_path)

    def _load_metadata(self):
        """Loads calibration, threshold, and manifest metadata from local files."""
        # 1. Calibration
        calib_file = os.path.join(self.model_dir, "calibration.json")
        if os.path.exists(calib_file):
            try:
                with open(calib_file, "r", encoding="utf-8") as f:
                    calib_data = json.load(f)
                    self.temperature = float(calib_data.get("temperature", self.temperature))
            except Exception as e:
                logger.warning(f"Could not parse calibration.json: {e}")

        # 2. Threshold
        thresh_file = os.path.join(self.model_dir, "threshold.json")
        if os.path.exists(thresh_file):
            try:
                with open(thresh_file, "r", encoding="utf-8") as f:
                    thresh_data = json.load(f)
                    self.threshold = float(thresh_data.get("threshold", self.threshold))
            except Exception as e:
                logger.warning(f"Could not parse threshold.json: {e}")

        # 3. Manifest
        if os.path.exists(MANIFEST_PATH):
            try:
                with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                    self.manifest = json.load(f)
            except Exception as e:
                logger.warning(f"Could not parse model_manifest.json: {e}")

    def load_model(self, force_reload: bool = False) -> bool:
        """
        Loads processor and model weights from disk once into memory.
        Safe for repeated calls (idempotent).
        """
        if self.is_loaded and self.model is not None and self.processor is not None and not force_reload:
            return True

        with self._lock:
            if self.is_loaded and self.model is not None and self.processor is not None and not force_reload:
                return True

            t0 = time.time()
            if not self.has_weights():
                self.load_error = f"Model weights not present in {self.model_dir}"
                logger.info(f"[PlantDiseaseModelService] {self.load_error}. Cloud / botanical fallback will be used.")
                return False

            torch = _get_torch()
            AutoImageProcessor, AutoModelForImageClassification = _get_transformers()
            if torch is None or AutoImageProcessor is None or AutoModelForImageClassification is None:
                self.load_error = "PyTorch or Transformers runtime not available in this environment"
                logger.info(f"[PlantDiseaseModelService] {self.load_error}. Cloud / botanical fallback will be used.")
                return False

            try:
                # Check for CUDA genuine compatibility
                if torch.cuda.is_available():
                    try:
                        # Verify tensor allocation on GPU works
                        t_test = torch.zeros(1).cuda()
                        del t_test
                        self.device = torch.device("cuda")
                        logger.info("CUDA acceleration detected and enabled for MobileNetV2 inference.")
                    except Exception as cuda_err:
                        logger.warning(f"CUDA reported available but tensor allocation failed: {cuda_err}. Falling to CPU.")
                        self.device = torch.device("cpu")
                else:
                    self.device = torch.device("cpu")

                # Load processor and model strictly offline
                self.processor = AutoImageProcessor.from_pretrained(
                    self.model_dir,
                    local_files_only=True
                )
                self.model = AutoModelForImageClassification.from_pretrained(
                    self.model_dir,
                    local_files_only=True
                )

                self.model.to(self.device)
                self.model.eval()

                # Extract label mappings directly from config
                self.id2label = {str(k): str(v) for k, v in self.model.config.id2label.items()}
                self.label2id = {str(k): int(v) for k, v in self.model.config.label2id.items()}

                self.load_duration_ms = round((time.time() - t0) * 1000.0, 2)
                self.is_loaded = True
                self.load_error = None
                logger.info(
                    f"MobileNetV2 model loaded successfully in {self.load_duration_ms}ms "
                    f"({len(self.id2label)} classes, device={self.device})."
                )
                return True

            except Exception as e:
                self.load_error = f"Failed to initialize MobileNetV2 model: {e}"
                logger.exception(self.load_error)
                self.is_loaded = False
                return False

    @staticmethod
    def parse_plantvillage_label(raw_label: str) -> Tuple[str, str, str, bool]:
        """
        Parses PlantVillage raw label (e.g. 'Tomato___Early_blight' or 'Corn_(maize)___Common_rust_')
        into (crop, disease_name, canonical_code, is_healthy).
        """
        parts = raw_label.split("___")
        raw_crop = parts[0]
        raw_disease = parts[1] if len(parts) > 1 else "Unknown"

        # Format crop name
        crop_clean = (
            raw_crop.replace("_", " ")
            .replace("(including sour)", "(Sour)")
            .replace("(maize)", "")
            .replace(",", "")
            .strip()
        )
        if "Pepper" in crop_clean:
            crop_clean = "Bell Pepper"
        elif "Cherry" in crop_clean:
            crop_clean = "Cherry"
        elif "Corn" in crop_clean:
            crop_clean = "Corn (Maize)"
        elif "Grape" in crop_clean:
            crop_clean = "Grapes"

        # Format disease name
        is_healthy = "healthy" in raw_disease.lower()
        if is_healthy:
            disease_clean = "Healthy Leaf"
        else:
            disease_clean = (
                raw_disease.replace("_", " ")
                .replace("  ", " ")
                .replace("(Citrus greening)", "Greening (Huanglongbing)")
                .replace("(Black Measles)", "(Esca)")
                .replace("(Isariopsis Leaf Spot)", "(Isariopsis Spot)")
                .strip()
            )

        # Generate canonical code
        code_crop = crop_clean.lower().split()[0]
        code_disease = "healthy" if is_healthy else raw_disease.lower().replace(" ", "_").replace(",", "").strip("_")
        canonical_code = f"{code_crop}_{code_disease}"

        return crop_clean, disease_clean, canonical_code, is_healthy

    def predict_disease(
        self,
        image_input: Union[bytes, Image.Image, np.ndarray],
        target_crop: Optional[str] = None
    ) -> ModelPredictionResult:
        """
        Executes local neural network disease inference.
        Returns top 3 predictions with calibrated and raw probability scores.
        """
        if not self.is_loaded:
            success = self.load_model()
            if not success or self.model is None or self.processor is None:
                raise RuntimeError(self.load_error or "Local MobileNetV2 model is not loaded.")

        torch = _get_torch()
        if torch is None:
            raise RuntimeError("PyTorch runtime is not available in this environment.")

        t0 = time.time()

        # 1. Decode / convert to PIL RGB image
        if isinstance(image_input, bytes):
            pil_img = Image.open(io.BytesIO(image_input)).convert("RGB")
        elif isinstance(image_input, np.ndarray):
            pil_img = Image.fromarray(image_input).convert("RGB")
        elif isinstance(image_input, Image.Image):
            pil_img = image_input.convert("RGB")
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")

        # 2. Check if a target crop was explicitly provided and whether it is supported
        crop_entry = get_crop_support(target_crop)
        crop_support_status = crop_entry.status.value

        # 3. Preprocess image
        inputs = self.processor(images=pil_img, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # 4. Neural Network Inference under torch.inference_mode()
        with torch.inference_mode():
            outputs = self.model(**inputs)
            logits = outputs.logits  # shape [1, 38]

            # Raw Softmax probabilities
            raw_probs = torch.softmax(logits, dim=-1)[0]

            # Calibrated temperature scaling: z_cal = z / T
            temp = self.temperature if self.temperature > 0 else 1.0
            calibrated_logits = logits / temp
            calibrated_probs = torch.softmax(calibrated_logits, dim=-1)[0]

            # Top 3 predictions
            topk = torch.topk(calibrated_probs, k=min(3, len(self.id2label)))
            top_indices = topk.indices.tolist()

        candidates: List[PredictionCandidate] = []
        for idx in top_indices:
            raw_label = self.id2label.get(str(idx), f"Class_{idx}")
            crop, disease, code, is_healthy = self.parse_plantvillage_label(raw_label)
            r_score = float(raw_probs[idx].cpu().item())
            c_score = float(calibrated_probs[idx].cpu().item())

            candidates.append(
                PredictionCandidate(
                    index=idx,
                    raw_label=raw_label,
                    crop=crop,
                    disease_name=disease,
                    canonical_disease_code=code,
                    raw_score=round(r_score, 4),
                    calibrated_score=round(c_score, 4),
                    is_healthy=is_healthy,
                    scientific_name=get_crop_support(crop).scientific_name
                )
            )

        top_pred = candidates[0]
        latency = round((time.time() - t0) * 1000.0, 2)

        # 5. Crop Cross-Validation: Check if caller requested a crop that contradicts prediction
        if target_crop and target_crop.lower() != "auto":
            if not is_crop_supported_by_local_model(target_crop):
                # The crop requested is explicitly unsupported by this model weights file
                return ModelPredictionResult(
                    status="UNSUPPORTED_CROP",
                    top_prediction=top_pred,
                    top_predictions=candidates,
                    crop_detected=top_pred.crop,
                    disease_name=f"Unsupported Crop: {target_crop.capitalize()}",
                    disease_code="unsupported_crop",
                    confidence=0.0,
                    raw_score=top_pred.raw_score,
                    calibrated_score=top_pred.calibrated_score,
                    is_calibrated=True,
                    temperature_applied=self.temperature,
                    threshold_applied=self.threshold,
                    is_healthy=False,
                    is_uncertain=True,
                    uncertainty_note=(
                        f"Crop '{target_crop.capitalize()}' is not present in MobileNetV2 PlantVillage weights. "
                        f"AgroScan AI avoids coercing unsupported crops into nearest visual matches."
                    ),
                    crop_support_status=CropSupportStatus.UNSUPPORTED.value,
                    latency_ms=latency,
                    device=str(self.device)
                )

        # 6. Uncertainty Policy based on threshold.json (theta = 0.50)
        is_uncertain = top_pred.calibrated_score < self.threshold
        uncertainty_note = None

        if is_uncertain:
            status = "UNCERTAIN"
            uncertainty_note = (
                f"Confidence ({top_pred.calibrated_score:.1%}) is below the calibrated decision threshold "
                f"({self.threshold:.1%}). Further agronomic evaluation or clearer photography recommended."
            )
        else:
            status = "HEALTHY" if top_pred.is_healthy else "DISEASE_DETECTED"

        return ModelPredictionResult(
            status=status,
            top_prediction=top_pred,
            top_predictions=candidates,
            crop_detected=top_pred.crop,
            disease_name=top_pred.disease_name,
            disease_code=top_pred.canonical_disease_code,
            confidence=top_pred.calibrated_score,
            raw_score=top_pred.raw_score,
            calibrated_score=top_pred.calibrated_score,
            is_calibrated=True,
            temperature_applied=self.temperature,
            threshold_applied=self.threshold,
            is_healthy=top_pred.is_healthy,
            is_uncertain=is_uncertain,
            uncertainty_note=uncertainty_note,
            crop_support_status=crop_support_status,
            latency_ms=latency,
            device=str(self.device)
        )

    def get_model_metadata(self) -> Dict[str, Any]:
        """Returns verified model metadata, architecture, revision, and parameters."""
        num_params = sum(p.numel() for p in self.model.parameters()) if self.model else 2272550
        return {
            "repository_id": "neghani/plantvillage-mobilenetv2",
            "model_name": "MobileNetV2 (PlantVillage v1.1)",
            "architecture": "MobileNetV2ForImageClassification",
            "base_model": "google/mobilenet_v2_1.0_224",
            "task": "image-classification",
            "revision": "v1.1",
            "immutable_commit_sha": "77e6d262dca53b818f7ad1d67088700754515639",
            "license": "Apache-2.0",
            "local_dir": self.model_dir,
            "weights_format": "safetensors",
            "weights_size_bytes": 9264680,
            "num_parameters": num_params,
            "num_classes": len(self.id2label) if self.id2label else 38,
            "crops_covered_count": 14,
            "device": str(self.device),
            "temperature_calibration": self.temperature,
            "confidence_threshold": self.threshold,
            "is_loaded": self.is_loaded
        }

    def get_model_health(self) -> Dict[str, Any]:
        """Health check verifying model loading, memory state, and inference readiness."""
        health_status = "HEALTHY" if self.is_loaded else "NOT_LOADED"
        if self.load_error:
            health_status = "ERROR"

        return {
            "status": health_status,
            "service": "plant_disease_mobilenetv2",
            "is_loaded": self.is_loaded,
            "device": str(self.device),
            "load_duration_ms": self.load_duration_ms,
            "load_error": self.load_error,
            "model_dir": self.model_dir,
            "num_classes": len(self.id2label) if self.id2label else 38,
            "temperature": self.temperature,
            "threshold": self.threshold
        }

    def get_supported_labels(self) -> List[Dict[str, Any]]:
        """Returns structured list of all 38 supported PlantVillage labels."""
        results = []
        for idx in range(len(self.id2label) if self.id2label else 38):
            label = self.id2label.get(str(idx), f"Class_{idx}")
            crop, disease, code, is_healthy = self.parse_plantvillage_label(label)
            results.append({
                "index": idx,
                "raw_label": label,
                "crop": crop,
                "disease_name": disease,
                "canonical_code": code,
                "is_healthy": is_healthy
            })
        return results


# Global singleton instance
local_model_service = PlantDiseaseModelService()


def load_model() -> bool:
    """Convenience function to load model."""
    return local_model_service.load_model()


def predict_disease(image_input: Union[bytes, Image.Image, np.ndarray], target_crop: Optional[str] = None) -> ModelPredictionResult:
    """Convenience function to execute inference."""
    return local_model_service.predict_disease(image_input, target_crop=target_crop)


def get_model_metadata() -> Dict[str, Any]:
    """Convenience function for metadata."""
    return local_model_service.get_model_metadata()


def get_model_health() -> Dict[str, Any]:
    """Convenience function for health check."""
    return local_model_service.get_model_health()


def get_supported_labels() -> List[Dict[str, Any]]:
    """Convenience function for supported labels."""
    return local_model_service.get_supported_labels()
