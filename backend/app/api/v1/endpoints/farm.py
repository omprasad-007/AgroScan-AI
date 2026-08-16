from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.all_models import User, Farm
from app.schemas.schemas import FarmCreate, FarmUpdate, FarmResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.post("", response_model=FarmResponse)
def create_farm(farm_in: FarmCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    farm = Farm(
        user_id=current_user.id,
        name=farm_in.name,
        village=farm_in.village or current_user.village or "Kagal",
        taluka=farm_in.taluka or current_user.taluka or "Kagal",
        district=farm_in.district or current_user.district or "Kolhapur",
        state=farm_in.state or current_user.state or "Maharashtra",
        pincode=farm_in.pincode or current_user.pincode or "416216",
        latitude=farm_in.latitude,
        longitude=farm_in.longitude,
        location_source=farm_in.location_source or "MANUAL",
        gps_accuracy=farm_in.gps_accuracy,
        crop_types=farm_in.crop_types or "Tomato, Potato, Sugarcane",
        area_acres=farm_in.area_acres or 2.5,
        irrigation_type=farm_in.irrigation_type or "Drip Irrigation"
    )
    db.add(farm)
    db.commit()
    db.refresh(farm)
    return farm

@router.get("", response_model=List[FarmResponse])
def get_farms(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Farm).filter(Farm.user_id == current_user.id).all()

@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    farm = db.query(Farm).filter(Farm.id == farm_id, Farm.user_id == current_user.id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found or access denied.")
    return farm

@router.patch("/{farm_id}", response_model=FarmResponse)
def update_farm(farm_id: str, farm_in: FarmUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    farm = db.query(Farm).filter(Farm.id == farm_id, Farm.user_id == current_user.id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found or access denied.")

    if farm_in.name is not None: farm.name = farm_in.name
    if farm_in.village is not None: farm.village = farm_in.village
    if farm_in.taluka is not None: farm.taluka = farm_in.taluka
    if farm_in.district is not None: farm.district = farm_in.district
    if farm_in.state is not None: farm.state = farm_in.state
    if farm_in.pincode is not None: farm.pincode = farm_in.pincode
    if farm_in.latitude is not None: farm.latitude = farm_in.latitude
    if farm_in.longitude is not None: farm.longitude = farm_in.longitude
    if farm_in.location_source is not None: farm.location_source = farm_in.location_source
    if farm_in.gps_accuracy is not None: farm.gps_accuracy = farm_in.gps_accuracy
    if farm_in.crop_types is not None: farm.crop_types = farm_in.crop_types
    if farm_in.area_acres is not None: farm.area_acres = farm_in.area_acres
    if farm_in.irrigation_type is not None: farm.irrigation_type = farm_in.irrigation_type

    db.commit()
    db.refresh(farm)
    return farm

@router.delete("/{farm_id}")
def delete_farm(farm_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    farm = db.query(Farm).filter(Farm.id == farm_id, Farm.user_id == current_user.id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found or access denied.")
    db.delete(farm)
    db.commit()
    return {"message": "Farm deleted successfully."}
