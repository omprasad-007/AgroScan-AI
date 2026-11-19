"""
AgroScan AI — Dedicated Model API Endpoints
Provides direct observability, health checks, and standalone inference for the local MobileNetV2 classifier.
"""

import asyncio
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from PIL import Image
import io

from app.services.plant_disease_model import (
    local_model_service,
    ModelPredictionResult,
    get_model_metadata,
    get_model_health,
    get_supported_labels
)
from app.services.crop_registry import (
    get_all_supported_crops,
    get_crop_support,
    CropRegistryEntry
)
from app.services.leaf_validator import LeafValidator, LeafValidationResult

router = APIRouter()

# Max 2 concurrent neural network inferences to protect 8GB system RAM
MODEL_INFERENCE_SEMAPHORE = asyncio.Semaphore(2)


@router.get("/health")
def model_health():
    """Health check for local MobileNetV2 model inference service."""
    return get_model_health()


@router.get("/info")
def model_info():
    """Model architecture, commit SHA, revision, calibration parameters, and licensing."""
    return get_model_metadata()


@router.get("/labels")
def model_labels():
    """Returns the complete 38 PlantVillage classification labels supported natively."""
    return get_supported_labels()


@router.get("/crops", response_model=List[CropRegistryEntry])
def registered_crops():
    """Returns all registered agricultural crops and their explicit support statuses."""
    return get_all_supported_crops()


@router.post("/predict")
async def model_predict_standalone(
    file: UploadFile = File(...),
    target_crop: Optional[str] = Form(None),
    validate_leaf: bool = Form(True)
):
    """
    Direct model inference endpoint.
    Performs mandatory leaf validation before invoking MobileNetV2.
    Offloaded to thread pool to avoid blocking the FastAPI event loop.
    """
    contents = await file.read()
    if not contents or len(contents) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty or exceeds the 10MB limit."
        )

    # Image validation gate
    if validate_leaf:
        val_res: LeafValidationResult = LeafValidator.validate_leaf_image(contents)
        if not val_res.usable_for_diagnosis or not val_res.is_leaf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image rejected by Leaf Validation Gate: {val_res.rejection_reason or val_res.message_en}"
            )

    # Thread-pool execution under concurrency semaphore
    async with MODEL_INFERENCE_SEMAPHORE:
        try:
            result = await asyncio.to_thread(
                local_model_service.predict_disease,
                image_input=contents,
                target_crop=target_crop
            )
            return result.model_dump()
        except ValueError as ve:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Inference error: {e}")
