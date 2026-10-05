import os
import io
import uuid
import logging
from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.core.database import get_db
from app.core.config import settings
from app.models.all_models import User, ScanPrediction, Recommendation, DiseaseInfo
from app.schemas.schemas import PredictionResponse
from app.api.deps import get_current_user
from app.services.leaf_validator import LeafValidator, LeafValidationResult
from app.services.consensus_engine import consensus_engine, ConsensusResult
from app.services.severity_analyzer import SeverityAnalyzer
from app.services.weather_service import WeatherRiskService
from app.services.disease_knowledge_base import get_disease_by_code

logger = logging.getLogger("agroscan")
router = APIRouter()

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024  # 10 MB

@router.post("/validate-image")
async def validate_plant_image(file: UploadFile = File(...)):
    """
    Stage 1 Leaf-Only & Image Quality Validation Gate.
    Verifies if uploaded image contains a recognizable plant leaf and meets diagnostic quality standards
    BEFORE executing plant identification or disease analysis.
    """
    contents = await file.read()
    if not contents or len(contents) > MAX_FILE_SIZE_BYTES:
        return {
            "is_plant": False,
            "is_leaf": False,
            "status": "EMPTY_OR_OVERSIZED_IMAGE",
            "message": "Please scan a clear photo of a plant leaf (size limit 10MB).",
            "message_mr": "कृपया वनस्पतीच्या पानाचा स्पष्ट फोटो स्कॅन करा (कमाल १० MB)."
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
            "rejection_reason": val_res.rejection_reason
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
        "quality_metrics": val_res.quality_metrics
    }

@router.get("/providers/health")
def get_provider_health_status(current_user: User = Depends(get_current_user)):
    """
    Provider Health & Diagnostic Monitoring Endpoint.
    Returns status, latency, success rate, and active providers WITHOUT exposing credentials.
    """
    health_list = consensus_engine.get_all_provider_health()
    return [h.model_dump() for h in health_list]

def format_prediction_response(
    p: ScanPrediction,
    rec_data: dict = None,
    extra_meta: dict = None
) -> PredictionResponse:
    kb_data = get_disease_by_code(p.disease_code)
    
    recom_payload = rec_data or {
        "organic_treatment": kb_data["organic_treatment"],
        "chemical_treatment": kb_data["chemical_treatment"],
        "prevention": kb_data["prevention"],
        "disclaimer": "Decision-support guidance only. Follow locally approved product labels."
    }

    meta = extra_meta or {}

    return PredictionResponse(
        id=p.id,
        image_url=p.image_path,
        plant=p.crop_detected,
        scientific_name=kb_data.get("scientific_name", "N/A"),
        disease=p.disease_name,
        confidence=p.confidence_score,
        severity=p.severity_level,
        severity_percentage=p.severity_percentage,
        affected_area=p.affected_area_cm2,
        risk=p.weather_risk_level,
        recommendation=recom_payload,
        
        # Backward compatibility aliases
        crop_detected=p.crop_detected,
        disease_name=p.disease_name,
        disease_code=p.disease_code,
        confidence_score=p.confidence_score,
        severity_level=p.severity_level,
        affected_area_cm2=p.affected_area_cm2,
        weather_risk_level=p.weather_risk_level,
        weather_risk_score=p.weather_risk_score,
        ambient_temp_c=p.ambient_temp_c,
        humidity_pct=p.humidity_pct,
        rainfall_mm=p.rainfall_mm,
        is_demo=p.is_demo,
        created_at=p.created_at,

        # Multi-API Consensus & Leaf Gate Metadata
        consensus_score=meta.get("consensus_score", p.confidence_score),
        providers_agreed=meta.get("providers_agreed", "1 of 1"),
        providers_called=meta.get("providers_called", 1),
        agreement_level=meta.get("agreement_level", "HIGH"),
        primary_provider=meta.get("primary_provider", "AgroScan Multi-Model Fusion"),
        supporting_providers=meta.get("supporting_providers", ["AgroScan Local Vision Engine"]),
        alternative_diagnoses=meta.get("alternative_diagnoses", []),
        image_quality_metrics=meta.get("image_quality_metrics", {}),
        leaf_validation=meta.get("leaf_validation", {"is_leaf": True, "leaf_confidence": 0.92}),
        uncertainty_note=meta.get("uncertainty_note", None)
    )

@router.post("/analyze", response_model=PredictionResponse)
async def analyze_leaf(
    file: UploadFile = File(...),
    farm_id: Optional[str] = Form(None),
    temperature_c: float = Form(24.0),
    humidity_pct: float = Form(78.0),
    rainfall_mm: float = Form(5.0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Safe filename and extension extraction
    raw_filename = file.filename or "leaf.jpg"
    file_ext = raw_filename.split(".")[-1].lower() if "." in raw_filename else "jpg"
    if file_ext not in ALLOWED_EXTENSIONS:
        file_ext = "jpg"

    if file.content_type and file.content_type.lower() not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Supported formats: JPEG, PNG, WEBP."
        )

    contents = await file.read()
    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image file is empty."
        )

    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image size exceeds limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    # 1. PIL Image Verification & Magic Byte Check
    try:
        img = Image.open(io.BytesIO(contents))
        img.verify()
    except Exception as img_err:
        logger.warning(f"Corrupt or invalid image upload attempted by user {current_user.id}: {img_err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please capture a clearer image of the affected leaf."
        )

    # 2. STRICT LEAF-ONLY & QUALITY VALIDATION GATE (CRITICAL REQUIREMENT)
    val_res: LeafValidationResult = LeafValidator.validate_leaf_image(contents)
    if not val_res.usable_for_diagnosis or not val_res.is_leaf:
        logger.info(f"Scan rejected at Leaf Gate: status={val_res.status_code}, reason={val_res.rejection_reason}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=val_res.message_en
        )

    # Sanitize input environmental parameters
    temp_c_clamped = max(-50.0, min(60.0, float(temperature_c)))
    hum_pct_clamped = max(0.0, min(100.0, float(humidity_pct)))
    rain_mm_clamped = max(0.0, min(500.0, float(rainfall_mm)))

    # Unique Scan Isolation
    scan_unique_id = f"scan_{uuid.uuid4().hex[:12]}"
    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
    saved_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    try:
        with open(saved_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        logger.error(f"Failed to write upload file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file safely.")

    try:
        # 3. Multi-API Provider Routing & Evidence Consensus Engine
        user_location = {"latitude": 16.58, "longitude": 74.31}
        consensus_res: ConsensusResult = await consensus_engine.diagnose_with_consensus(
            image_bytes=contents,
            scan_id=scan_unique_id,
            target_crop=None,
            location=user_location,
            language=current_user.language or "en"
        )

        # 4. Computer Vision Lesion Severity Analysis
        severity_res = SeverityAnalyzer.analyze_image_bytes(contents)

        # 5. Biological Weather Risk Engine
        weather_res = WeatherRiskService.calculate_risk(
            temp_c=temp_c_clamped,
            humidity_pct=hum_pct_clamped,
            rainfall_mm=rain_mm_clamped,
            crop=consensus_res.plant,
            disease=consensus_res.disease
        )

        # 6. Save Persistent Scan Record
        prediction = ScanPrediction(
            id=scan_unique_id,
            user_id=current_user.id,
            farm_id=farm_id,
            image_path=f"/uploads/{unique_filename}",
            crop_detected=consensus_res.plant,
            disease_name=consensus_res.disease,
            disease_code=consensus_res.disease_code,
            confidence_score=consensus_res.confidence,
            severity_percentage=severity_res["severity_percentage"],
            severity_level=severity_res["severity_level"],
            affected_area_cm2=severity_res["affected_area_cm2"],
            ambient_temp_c=temp_c_clamped,
            humidity_pct=hum_pct_clamped,
            rainfall_mm=rain_mm_clamped,
            weather_risk_score=weather_res["risk_score"],
            weather_risk_level=weather_res["risk_level"],
            is_demo=consensus_res.is_demo
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        # 7. Knowledge Base Treatment Recommendation
        kb_data = get_disease_by_code(consensus_res.disease_code)
        recom = Recommendation(
            prediction_id=prediction.id,
            organic_remedy=kb_data["organic_treatment"],
            chemical_remedy=kb_data["chemical_treatment"],
            preventive_steps=kb_data["prevention"]
        )
        db.add(recom)
        db.commit()

        extra_meta = {
            "consensus_score": consensus_res.consensus_score,
            "providers_agreed": f"{consensus_res.providers_agreed} of {consensus_res.providers_called}",
            "providers_called": consensus_res.providers_called,
            "agreement_level": consensus_res.agreement_level,
            "primary_provider": consensus_res.primary_provider,
            "supporting_providers": consensus_res.supporting_providers,
            "alternative_diagnoses": consensus_res.alternative_diagnoses,
            "image_quality_metrics": val_res.quality_metrics,
            "leaf_validation": {
                "is_leaf": val_res.is_leaf,
                "leaf_confidence": val_res.leaf_confidence,
                "image_quality": val_res.image_quality,
                "leaf_visibility": val_res.leaf_visibility
            },
            "uncertainty_note": consensus_res.uncertainty_note
        }

        return format_prediction_response(
            prediction,
            {
                "organic_treatment": kb_data["organic_treatment"],
                "chemical_treatment": kb_data["chemical_treatment"],
                "prevention": kb_data["prevention"],
                "disclaimer": "Decision-support guidance only. Follow locally approved product labels."
            },
            extra_meta
        )

    except HTTPException:
        db.rollback()
        raise
    except ValueError as val_err:
        logger.warning(f"Leaf/diagnosis rejection: {val_err}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )
    except Exception as e:
        logger.error(f"Error analyzing leaf image for user {current_user.id}: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Disease analysis is currently unavailable. Please try again later or upload another clear leaf image."
        )

@router.get("/history", response_model=List[PredictionResponse])
def get_prediction_history(
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    preds = db.query(ScanPrediction)\
        .filter(ScanPrediction.user_id == current_user.id)\
        .order_by(ScanPrediction.created_at.desc())\
        .limit(limit).all()

    return [format_prediction_response(p) for p in preds]

@router.get("/{id}", response_model=PredictionResponse)
def get_prediction_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    p = db.query(ScanPrediction).filter(ScanPrediction.id == id, ScanPrediction.user_id == current_user.id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Prediction record not found")

    return format_prediction_response(p)
