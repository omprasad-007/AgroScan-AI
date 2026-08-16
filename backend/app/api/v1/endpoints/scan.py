import os
import io
import uuid
import logging
from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.config import settings
from app.models.all_models import User, ScanPrediction, Recommendation, DiseaseInfo
from app.schemas.schemas import PredictionResponse
from app.api.deps import get_current_user
from app.services.model_service import ModelServiceFactory
from app.services.severity_analyzer import SeverityAnalyzer
from app.services.weather_service import WeatherRiskService
from app.services.disease_knowledge_base import get_disease_by_code

logger = logging.getLogger("agroscan")
router = APIRouter()

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024  # 10 MB

def format_prediction_response(p: ScanPrediction, rec_data: dict = None) -> PredictionResponse:
    kb_data = get_disease_by_code(p.disease_code)
    
    recom_payload = rec_data or {
        "organic_treatment": kb_data["organic_treatment"],
        "chemical_treatment": kb_data["chemical_treatment"],
        "prevention": kb_data["prevention"],
        "disclaimer": "Decision-support guidance only. Follow locally approved product labels."
    }

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
        created_at=p.created_at
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

    # Magic-byte / PIL Image integrity validation
    try:
        img = Image.open(io.BytesIO(contents))
        img.verify()
    except Exception as img_err:
        logger.warning(f"Corrupt image upload attempted by user {current_user.id}: {img_err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Corrupt or invalid image file. Please upload a valid plant leaf image."
        )

    # Sanitize input environmental parameters
    temp_c_clamped = max(-50.0, min(60.0, float(temperature_c)))
    hum_pct_clamped = max(0.0, min(100.0, float(humidity_pct)))
    rain_mm_clamped = max(0.0, min(500.0, float(rainfall_mm)))

    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
    saved_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    try:
        with open(saved_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        logger.error(f"Failed to write upload file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file safely.")

    try:
        # 1. Prediction (DEMO_MODE or MobileNetV2)
        predictor = ModelServiceFactory.get_predictor()
        pred_res = predictor.predict(contents)

        # 2. OpenCV Severity Analysis
        severity_res = SeverityAnalyzer.analyze_image_bytes(contents)

        # 3. Weather Risk Engine
        weather_res = WeatherRiskService.calculate_risk(
            temp_c=temp_c_clamped,
            humidity_pct=hum_pct_clamped,
            rainfall_mm=rain_mm_clamped,
            crop=pred_res["crop"],
            disease=pred_res["disease_name"]
        )

        # 4. Save Record
        prediction = ScanPrediction(
            user_id=current_user.id,
            farm_id=farm_id,
            image_path=f"/uploads/{unique_filename}",
            crop_detected=pred_res["crop"],
            disease_name=pred_res["disease_name"],
            disease_code=pred_res["disease_code"],
            confidence_score=pred_res["confidence"],
            severity_percentage=severity_res["severity_percentage"],
            severity_level=severity_res["severity_level"],
            affected_area_cm2=severity_res["affected_area_cm2"],
            ambient_temp_c=temp_c_clamped,
            humidity_pct=hum_pct_clamped,
            rainfall_mm=rain_mm_clamped,
            weather_risk_score=weather_res["risk_score"],
            weather_risk_level=weather_res["risk_level"],
            is_demo=pred_res["is_demo"]
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        # 5. Recommendation Entry
        kb_data = get_disease_by_code(pred_res["disease_code"])
        recom = Recommendation(
            prediction_id=prediction.id,
            organic_remedy=kb_data["organic_treatment"],
            chemical_remedy=kb_data["chemical_treatment"],
            preventive_steps=kb_data["prevention"]
        )
        db.add(recom)
        db.commit()

        return format_prediction_response(prediction, {
            "organic_treatment": kb_data["organic_treatment"],
            "chemical_treatment": kb_data["chemical_treatment"],
            "prevention": kb_data["prevention"],
            "disclaimer": "Decision-support guidance only. Follow locally approved product labels."
        })
    except Exception as e:
        logger.error(f"Error analyzing leaf image for user {current_user.id}: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while analyzing the leaf image. Please try again."
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

