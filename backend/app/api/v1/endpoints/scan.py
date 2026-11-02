import io
import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from PIL import Image
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_optional_current_user
from app.core.config import settings
from app.core.database import get_db
from app.models.all_models import Recommendation, ScanPrediction, User
from app.schemas.schemas import PredictionResponse
from app.services.consensus_engine import ConsensusResult, consensus_engine
from app.services.disease_knowledge_base import get_disease_by_code
from app.services.leaf_validator import LeafValidationResult, LeafValidator
from app.services.severity_analyzer import SeverityAnalyzer
from app.services.weather_service import WeatherRiskService

logger = logging.getLogger("agroscan")
router = APIRouter()

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@router.post("/validate-image")
async def validate_plant_image(file: UploadFile = File(...)):
    """Validate that an uploaded photo is usable before a diagnosis is requested."""
    contents = await file.read()
    if not contents or len(contents) > MAX_FILE_SIZE_BYTES:
        return {
            "is_plant": False,
            "is_leaf": False,
            "status": "EMPTY_OR_OVERSIZED_IMAGE",
            "message": "Please scan a clear photo of a plant leaf (size limit 10MB).",
            "message_mr": "कृपया वनस्पतीच्या पानाचा स्पष्ट फोटो स्कॅन करा (कमाल १० MB).",
        }

    val_res: LeafValidationResult = LeafValidator.validate_leaf_image(contents)
    if not val_res.usable_for_diagnosis or not val_res.is_leaf:
        return {
            "is_plant": val_res.is_plant,
            "is_leaf": val_res.is_leaf,
            "leaf_confidence": val_res.leaf_confidence,
            "image_quality": val_res.image_quality,
            "usable_for_diagnosis": False,
            "status": val_res.status_code,
            "message": val_res.message_en,
            "message_mr": val_res.message_mr,
            "quality_metrics": val_res.quality_metrics,
            "rejection_reason": val_res.rejection_reason,
        }

    return {
        "is_plant": True,
        "is_leaf": True,
        "leaf_confidence": val_res.leaf_confidence,
        "image_quality": val_res.image_quality,
        "usable_for_diagnosis": True,
        "leaf_visibility": val_res.leaf_visibility,
        "status": "VALID_LEAF",
        "message": val_res.message_en,
        "message_mr": val_res.message_mr,
        "quality_metrics": val_res.quality_metrics,
    }


@router.get("/providers/health")
def get_provider_health_status(current_user: User = Depends(get_current_user)):
    """Return provider monitoring data for signed-in users only."""
    health_list = consensus_engine.get_all_provider_health()
    return [health.model_dump() for health in health_list]


def format_prediction_response(
    prediction: ScanPrediction,
    recommendation: Optional[Dict[str, Any]] = None,
    extra_meta: Optional[Dict[str, Any]] = None,
) -> PredictionResponse:
    knowledge = get_disease_by_code(prediction.disease_code)
    recommendation_payload = recommendation or {
        "organic_treatment": knowledge["organic_treatment"],
        "chemical_treatment": knowledge["chemical_treatment"],
        "prevention": knowledge["prevention"],
        "disclaimer": "Decision-support guidance only. Follow locally approved product labels.",
    }
    meta = extra_meta or {}

    return PredictionResponse(
        id=prediction.id,
        image_url=prediction.image_path,
        plant=prediction.crop_detected,
        scientific_name=knowledge.get("scientific_name", "N/A"),
        disease=prediction.disease_name,
        confidence=prediction.confidence_score,
        severity=prediction.severity_level,
        severity_percentage=prediction.severity_percentage,
        affected_area=prediction.affected_area_cm2,
        risk=prediction.weather_risk_level,
        recommendation=recommendation_payload,
        crop_detected=prediction.crop_detected,
        disease_name=prediction.disease_name,
        disease_code=prediction.disease_code,
        confidence_score=prediction.confidence_score,
        severity_level=prediction.severity_level,
        affected_area_cm2=prediction.affected_area_cm2,
        weather_risk_level=prediction.weather_risk_level,
        weather_risk_score=prediction.weather_risk_score,
        ambient_temp_c=prediction.ambient_temp_c,
        humidity_pct=prediction.humidity_pct,
        rainfall_mm=prediction.rainfall_mm,
        is_demo=prediction.is_demo,
        is_guest=meta.get("is_guest", False),
        created_at=prediction.created_at,
        consensus_score=meta.get("consensus_score", prediction.confidence_score),
        providers_agreed=meta.get("providers_agreed", "1 of 1"),
        providers_called=meta.get("providers_called", 1),
        agreement_level=meta.get("agreement_level", "HIGH"),
        primary_provider=meta.get("primary_provider", "AgroScan Multi-Model Fusion"),
        supporting_providers=meta.get("supporting_providers", ["AgroScan Local Vision Engine"]),
        alternative_diagnoses=meta.get("alternative_diagnoses", []),
        image_quality_metrics=meta.get("image_quality_metrics", {}),
        leaf_validation=meta.get("leaf_validation", {"is_leaf": True, "leaf_confidence": 0.92}),
        uncertainty_note=meta.get("uncertainty_note"),
    )


@router.post("/analyze", response_model=PredictionResponse)
async def analyze_leaf(
    file: UploadFile = File(...),
    farm_id: Optional[str] = Form(None),
    target_crop: Optional[str] = Form(None),
    temperature_c: float = Form(24.0),
    humidity_pct: float = Form(78.0),
    rainfall_mm: float = Form(5.0),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Diagnose one photo. Guests receive an immediate result; signed-in users also save it."""
    raw_filename = file.filename or "leaf.jpg"
    file_ext = raw_filename.rsplit(".", 1)[-1].lower() if "." in raw_filename else "jpg"
    if file_ext not in ALLOWED_EXTENSIONS:
        file_ext = "jpg"

    if file.content_type and file.content_type.lower() not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Supported formats: JPEG, PNG, WEBP.",
        )

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded image file is empty.")
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image size exceeds limit of {settings.MAX_UPLOAD_SIZE_MB}MB.",
        )

    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()
    except Exception as image_error:
        actor = f"user {current_user.id}" if current_user else "guest"
        logger.warning("Corrupt or invalid image upload attempted by %s: %s", actor, image_error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please capture a clearer image of the affected leaf.",
        )

    validation: LeafValidationResult = LeafValidator.validate_leaf_image(contents)
    if not validation.usable_for_diagnosis or not validation.is_leaf:
        language = (getattr(current_user, "language", "en") or "en") if current_user else "en"
        message = validation.message_mr if language == "mr" else validation.message_en
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    temp_c = max(-50.0, min(60.0, float(temperature_c)))
    humidity = max(0.0, min(100.0, float(humidity_pct)))
    rainfall = max(0.0, min(500.0, float(rainfall_mm)))
    scan_id = f"scan_{uuid.uuid4().hex[:12]}"
    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    saved_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    try:
        with open(saved_path, "wb") as uploaded_file:
            uploaded_file.write(contents)
    except OSError as file_error:
        logger.error("Failed to store uploaded scan image: %s", file_error)
        raise HTTPException(status_code=500, detail="Could not save the uploaded image. Please try again.")

    try:
        language = (getattr(current_user, "language", "en") or "en") if current_user else "en"
        consensus: ConsensusResult = await consensus_engine.diagnose_with_consensus(
            image_bytes=contents,
            scan_id=scan_id,
            target_crop=target_crop,
            location={"latitude": 16.58, "longitude": 74.31},
            language=language,
        )
        severity = SeverityAnalyzer.analyze_image_bytes(contents)
        weather = WeatherRiskService.calculate_risk(
            temp_c=temp_c,
            humidity_pct=humidity,
            rainfall_mm=rainfall,
            crop=consensus.plant,
            disease=consensus.disease,
        )
        prediction = ScanPrediction(
            id=scan_id,
            user_id=current_user.id if current_user else "guest",
            farm_id=farm_id if current_user else None,
            image_path=f"/uploads/{unique_filename}",
            crop_detected=consensus.plant,
            disease_name=consensus.disease,
            disease_code=consensus.disease_code,
            confidence_score=consensus.confidence,
            severity_percentage=severity["severity_percentage"],
            severity_level=severity["severity_level"],
            affected_area_cm2=severity["affected_area_cm2"],
            ambient_temp_c=temp_c,
            humidity_pct=humidity,
            rainfall_mm=rainfall,
            weather_risk_score=weather["risk_score"],
            weather_risk_level=weather["risk_level"],
            is_demo=consensus.is_demo,
        )

        knowledge = get_disease_by_code(consensus.disease_code)
        recommendation = {
            "organic_treatment": knowledge["organic_treatment"],
            "chemical_treatment": knowledge["chemical_treatment"],
            "prevention": knowledge["prevention"],
            "disclaimer": "Decision-support guidance only. Follow locally approved product labels.",
        }

        if current_user:
            db.add(prediction)
            db.commit()
            db.refresh(prediction)
            db.add(
                Recommendation(
                    prediction_id=prediction.id,
                    organic_remedy=recommendation["organic_treatment"],
                    chemical_remedy=recommendation["chemical_treatment"],
                    preventive_steps=recommendation["prevention"],
                )
            )
            db.commit()

        extra_meta = {
            "is_guest": current_user is None,
            "consensus_score": consensus.consensus_score,
            "providers_agreed": f"{consensus.providers_agreed} of {consensus.providers_called}",
            "providers_called": consensus.providers_called,
            "agreement_level": consensus.agreement_level,
            "primary_provider": consensus.primary_provider,
            "supporting_providers": consensus.supporting_providers,
            "alternative_diagnoses": consensus.alternative_diagnoses,
            "image_quality_metrics": validation.quality_metrics,
            "leaf_validation": {
                "is_leaf": validation.is_leaf,
                "leaf_confidence": validation.leaf_confidence,
                "image_quality": validation.image_quality,
                "leaf_visibility": validation.leaf_visibility,
            },
            "uncertainty_note": consensus.uncertainty_note,
        }
        return format_prediction_response(prediction, recommendation, extra_meta)

    except HTTPException:
        db.rollback()
        raise
    except ValueError as error:
        logger.warning("Leaf/diagnosis rejection: %s", error)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except RuntimeError as error:
        logger.warning("Disease detection provider failure: %s", error)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error))
    except Exception as error:
        logger.exception("Error analyzing leaf image for %s", current_user.id if current_user else "guest")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Disease analysis is currently unavailable. Please try again later or upload another clear leaf image.",
        )


@router.get("/history", response_model=List[PredictionResponse])
def get_prediction_history(
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    predictions = (
        db.query(ScanPrediction)
        .filter(ScanPrediction.user_id == current_user.id)
        .order_by(ScanPrediction.created_at.desc())
        .limit(limit)
        .all()
    )
    return [format_prediction_response(prediction) for prediction in predictions]


@router.get("/{id}", response_model=PredictionResponse)
def get_prediction_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prediction = (
        db.query(ScanPrediction)
        .filter(ScanPrediction.id == id, ScanPrediction.user_id == current_user.id)
        .first()
    )
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction record not found")
    return format_prediction_response(prediction)
