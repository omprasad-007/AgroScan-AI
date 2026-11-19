"""
Re-export module for backward/flexible import path compatibility.
Directs imports to app.services.plant_disease_model.
"""

from app.services.plant_disease_model import (
    PlantDiseaseModelService,
    local_model_service,
    load_model,
    predict_disease,
    get_model_metadata,
    get_model_health,
    get_supported_labels,
    ModelPredictionResult,
    PredictionCandidate
)

__all__ = [
    "PlantDiseaseModelService",
    "local_model_service",
    "load_model",
    "predict_disease",
    "get_model_metadata",
    "get_model_health",
    "get_supported_labels",
    "ModelPredictionResult",
    "PredictionCandidate"
]
