from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.all_models import ScanPrediction, Recommendation
from app.schemas.schemas import RecommendationResponse
from app.api.deps import get_current_user
from app.services.disease_knowledge_base import get_disease_by_code

router = APIRouter()

@router.get("/{prediction_id}", response_model=RecommendationResponse)
def get_recommendation_by_prediction(
    prediction_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    pred = db.query(ScanPrediction).filter(
        ScanPrediction.id == prediction_id,
        ScanPrediction.user_id == current_user.id
    ).first()
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction record not found")

    recom = db.query(Recommendation).filter(Recommendation.prediction_id == prediction_id).first()
    kb = get_disease_by_code(pred.disease_code)

    return RecommendationResponse(
        id=recom.id if recom else "rec_gen",
        prediction_id=prediction_id,
        disease_name=kb["disease_name"],
        crop=kb["crop"],
        symptoms=kb["symptoms"],
        organic_treatment=recom.organic_remedy if recom else kb["organic_treatment"],
        chemical_treatment=recom.chemical_remedy if recom else kb["chemical_treatment"],
        prevention=recom.preventive_steps if recom else kb["prevention"],
        general_guidance=kb["general_guidance"],
        disclaimer="Decision-support guidance only. Follow locally approved product labels and agricultural extension guidelines."
    )
