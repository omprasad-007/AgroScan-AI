from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.all_models import User, ScanPrediction
from app.schemas.schemas import UserResponse
from app.api.deps import get_admin_user

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    return db.query(User).all()

@router.get("/analytics")
def get_admin_system_analytics(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    total_users = db.query(User).count()
    total_scans = db.query(ScanPrediction).count()
    demo_scans = db.query(ScanPrediction).filter(ScanPrediction.is_demo == True).count()
    
    return {
        "system_status": "Operational",
        "total_users": total_users,
        "total_scans": total_scans,
        "demo_scans": demo_scans,
        "ml_scans": total_scans - demo_scans
    }
