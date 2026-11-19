"""
AgroScan AI — Hybrid Intelligence Engine Package
Modular, local-first plant disease detection & crop health monitoring.
"""

from app.services.ai.image_preprocessor import ImagePreprocessor, ImagePreprocessingError
from app.services.ai.crop_registry import CropRegistry, CropSupportStatus, CropProfile
from app.services.ai.model_registry import ModelRegistry, ModelInitializationError
from app.services.ai.hf_inference_service import HuggingFaceInferenceService
from app.services.ai.confidence_calibrator import ConfidenceCalibrator
from app.services.ai.result_normalizer import ResultNormalizer
from app.services.ai.orchestrator import HybridPredictionOrchestrator, orchestrator

__all__ = [
    "ImagePreprocessor",
    "ImagePreprocessingError",
    "CropRegistry",
    "CropSupportStatus",
    "CropProfile",
    "ModelRegistry",
    "ModelInitializationError",
    "HuggingFaceInferenceService",
    "ConfidenceCalibrator",
    "ResultNormalizer",
    "HybridPredictionOrchestrator",
    "orchestrator",
]
