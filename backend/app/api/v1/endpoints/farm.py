from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.all_models import User, Farm
from app.schemas.schemas import FarmCreate, FarmResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.post("", response_model=FarmResponse)
def create_farm(farm_in: FarmCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    farm = Farm(
        user_id=current_user.id,
        name=farm_in.name,
        location=farm_in.location or current_user.city,
        crop_types=farm_in.crop_types,
        area_acres=farm_in.area_acres or 1.0
    )
    db.add(farm)
    db.commit()
    db.refresh(farm)
    return farm

@router.get("", response_model=List[FarmResponse])
def get_farms(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Farm).filter(Farm.user_id == current_user.id).all()
