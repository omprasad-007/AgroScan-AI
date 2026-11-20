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
from app.services.ai import orchestrator, ModelRegistry

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
    """Return provider and local Hugging Face model monitoring data for signed-in users only."""
    health_list = consensus_engine.get_all_provider_health()
    res = [health.model_dump() for health in health_list]
    for hf in ModelRegistry.get_health_status():
        res.append({
            "provider_name": hf["model_id"],
            "display_name": hf["display_name"],
            "status": "AVAILABLE" if hf["status"] in ["LOADED_HEALTHY", "READY_TO_LOAD"] else "DEGRADED",
            "is_configured": True,
            "requires_key": False,
            "latency_ms": hf["average_latency_ms"],
            "failure_count": 1 if hf["last_error"] else 0,
            "total_calls": hf["total_inferences"],
            "success_rate": 1.0 if not hf["last_error"] else 0.8,
            "supported_crops": ["Tomato", "Potato", "Apple", "Corn", "Grapes", "Soybean", "Bell Pepper"],
            "notes": f"Local hardware execution ({hf['device']})"
        })
    return res


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
        "disclaimer": "Preliminary AI decision-support estimate. Follow locally approved product labels and consult an agronomist.",
    }
    meta = extra_meta or {}

    pred_status = getattr(prediction, "status", None) or meta.get("status") or "DISEASE_DETECTED"
    crop_support = getattr(prediction, "crop_support_status", None) or meta.get("crop_support_status") or "SUPPORTED"
    mod_ver = getattr(prediction, "model_version", None) or meta.get("model_version") or "hybrid_v1.0"

    return PredictionResponse(
        id=prediction.id,
        scan_id=prediction.id,
        status=pred_status,
        image_url=prediction.image_path,
        plant=prediction.crop_detected,
        plant_name=prediction.crop_detected,
        scientific_name=knowledge.get("scientific_name", "N/A"),
        crop_support_status=crop_support,
        disease=prediction.disease_name,
        disease_name=prediction.disease_name,
        disease_code=prediction.disease_code,
        disease_category=meta.get("disease_category", "Foliar Pathology"),
        healthy_status="healthy" in prediction.disease_code.lower(),
        confidence=prediction.confidence_score,
        prediction_confidence=prediction.confidence_score,
        confidence_interpretation=(
            "HIGH_CONFIDENCE" if prediction.confidence_score >= 0.70
            else ("MODERATE_CONFIDENCE" if prediction.confidence_score >= 0.50 else "LOW_CONFIDENCE_UNCERTAIN")
        ),
        severity=prediction.severity_level,
        severity_percentage=prediction.severity_percentage,
        affected_area=prediction.affected_area_cm2,
        risk=prediction.weather_risk_level,
        recommendation=recommendation_payload,
        treatment_guidance=recommendation_payload,
        prevention_guidance=recommendation_payload.get("prevention"),
        recommended_next_steps=meta.get("recommended_next_steps", [
            "Monitor crop foliage closely and ensure proper irrigation scheduling.",
            "Verify symptoms with a field inspection before applying chemical controls."
        ]),
        limitations=meta.get("limitations", "Visual computer vision analysis evaluates superficial leaf features only."),
        analysis_timestamp=str(prediction.created_at or ""),
        model_version=mod_ver,
        provider_information=meta.get("provider_information"),
        model_predictions=meta.get("model_predictions", []),
        provider_predictions=meta.get("provider_predictions", []),
        agreement_status=meta.get("agreement_status", "SINGLE_SOURCE"),
        crop_detected=prediction.crop_detected,
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
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    location_name: Optional[str] = Form(None),
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
        weather_params = {"temperature_c": temp_c, "humidity_pct": humidity, "rainfall_mm": rainfall}

        orch_res = await orchestrator.orchestrate_scan(
            image_bytes=contents,
            scan_id=scan_id,
            target_crop=target_crop,
            weather_params=weather_params,
            location={
                "latitude": latitude or 16.6941,
                "longitude": longitude or 74.2366,
                "location_name": location_name or "Local Farm"
            },
            is_guest=current_user is None,
            image_url=f"/uploads/{unique_filename}",
            language=language
        )

        if orch_res.get("status") in ["INVALID_IMAGE", "POOR_IMAGE_QUALITY"]:
            message = orch_res.get("message") or "No clear leaf was detected in this image."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

        if orch_res.get("status") == "PROVIDER_UNAVAILABLE":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=orch_res.get("message") or "Disease detection provider failure."
            )

        prediction = ScanPrediction(
            id=scan_id,
            user_id=current_user.id if current_user else "guest",
            farm_id=farm_id if current_user else None,
            image_path=f"/uploads/{unique_filename}",
            crop_detected=orch_res.get("plant", "Plant"),
            disease_name=orch_res.get("disease", "Unknown"),
            disease_code=orch_res.get("disease_code", "unknown_condition"),
            confidence_score=orch_res.get("confidence", 0.50),
            severity_percentage=orch_res.get("severity_percentage", 0.0),
            severity_level=orch_res.get("severity_level", "Mild"),
            affected_area_cm2=orch_res.get("affected_area_cm2", 0.0),
            ambient_temp_c=temp_c,
            humidity_pct=humidity,
            rainfall_mm=rainfall,
            weather_risk_score=orch_res.get("weather_risk_score", 0.0),
            weather_risk_level=orch_res.get("weather_risk_level", "Low"),
            is_demo=False,
            status=orch_res.get("status", "DISEASE_DETECTED"),
            crop_support_status=orch_res.get("crop_support_status", "SUPPORTED"),
            model_version=orch_res.get("model_version", "hybrid_v1.0"),
            provider_info=orch_res.get("primary_provider", "Local Hugging Face Engine")
        )

        rec_data = orch_res.get("recommendation", {})
        if current_user:
            db.add(prediction)
            db.commit()
            db.refresh(prediction)
            db.add(
                Recommendation(
                    prediction_id=prediction.id,
                    organic_remedy=rec_data.get("organic_treatment", ""),
                    chemical_remedy=rec_data.get("chemical_treatment", ""),
                    preventive_steps=rec_data.get("prevention", ""),
                    disclaimer=rec_data.get("disclaimer", "")
                )
            )
            db.commit()

        return PredictionResponse(**orch_res)

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
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    user_id = current_user.id if current_user else "guest"
    query = db.query(ScanPrediction).filter(
        (ScanPrediction.user_id == user_id) | (ScanPrediction.user_id == "guest")
    ) if not current_user else db.query(ScanPrediction).filter(ScanPrediction.user_id == current_user.id)

    predictions = query.order_by(ScanPrediction.created_at.desc()).limit(limit).all()
    return [format_prediction_response(prediction) for prediction in predictions]


@router.delete("/history")
def clear_prediction_history(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Permanently delete all scan prediction history and associated recommendations."""
    if current_user:
        preds = db.query(ScanPrediction).filter(
            (ScanPrediction.user_id == current_user.id) | (ScanPrediction.user_id == "guest")
        ).all()
    else:
        # In demo or guest mode, clear all guest/demo scans
        demo_farmer = db.query(User).filter(User.email == "farmer@agroscan.ai").first()
        demo_ids = [demo_farmer.id] if demo_farmer else []
        preds = db.query(ScanPrediction).filter(
            (ScanPrediction.user_id == "guest") | (ScanPrediction.user_id.in_(demo_ids))
        ).all()

    pred_ids = [p.id for p in preds]
    if pred_ids:
        db.query(Recommendation).filter(Recommendation.prediction_id.in_(pred_ids)).delete(synchronize_session=False)
        db.query(ScanPrediction).filter(ScanPrediction.id.in_(pred_ids)).delete(synchronize_session=False)
        db.commit()

    return {
        "status": "success",
        "deleted_count": len(pred_ids),
        "message": "Scan history and diagnostic records cleared permanently from database.",
    }


@router.delete("/{id}")
def delete_prediction_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Delete a single scan prediction record and its recommendations with strict ownership checks."""
    pred = db.query(ScanPrediction).filter(ScanPrediction.id == id).first()
    if not pred:
        return {"status": "not_found", "id": id, "message": "Prediction record not found"}

    if current_user:
        if pred.user_id != current_user.id and pred.user_id != "guest":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this scan record."
            )
    else:
        if pred.user_id != "guest":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authentication required to delete non-guest scan records."
            )

    db.query(Recommendation).filter(Recommendation.prediction_id == pred.id).delete(synchronize_session=False)
    db.delete(pred)
    db.commit()
    return {"status": "success", "id": id, "message": "Scan record deleted successfully."}


@router.get("/{id}", response_model=PredictionResponse)
def get_prediction_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    query = db.query(ScanPrediction).filter(ScanPrediction.id == id)
    if current_user:
        query = query.filter((ScanPrediction.user_id == current_user.id) | (ScanPrediction.user_id == "guest"))
    else:
        query = query.filter(ScanPrediction.user_id == "guest")
    prediction = query.first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction record not found")
    return format_prediction_response(prediction)
