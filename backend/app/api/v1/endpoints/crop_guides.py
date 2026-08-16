from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List
from app.services.disease_knowledge_base import CROP_CULTIVATION_KB, get_crop_cultivation_info

router = APIRouter()

@router.get("", response_model=List[str])
def list_supported_crops():
    """
    Returns list of supported crops in AgroScan AI Crop Knowledge System.
    """
    return list(CROP_CULTIVATION_KB.keys())

@router.get("/{crop_name}")
def get_crop_guide(crop_name: str) -> Dict[str, Any]:
    """
    Returns structured cultivation & harvest guide for a specific crop:
    - Planting, nursery, transplanting, spacing, soil, irrigation, fertilization,
      growth stages, harvest indicators, and harvest period.
    """
    info = get_crop_cultivation_info(crop_name)
    if not info:
        raise HTTPException(
            status_code=404, 
            detail=f"Crop guide for '{crop_name}' not found. Supported crops: {', '.join(CROP_CULTIVATION_KB.keys())}"
        )
    return {
        "crop": crop_name.title(),
        **info
    }
