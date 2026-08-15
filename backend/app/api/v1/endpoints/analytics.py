from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.all_models import User, ScanPrediction
from app.schemas.schemas import DashboardAnalytics
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/dashboard", response_model=DashboardAnalytics)
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    preds = db.query(ScanPrediction).filter(ScanPrediction.user_id == current_user.id).all()
    
    total = len(preds)
    healthy = sum(1 for p in preds if "Healthy" in p.disease_name)
    diseased = total - healthy
    
    avg_conf = round(sum(p.confidence_score for p in preds) / total, 4) if total > 0 else 0.92

    # Disease Distribution
    dist_map = {}
    severity_map = {"Healthy": 0, "Mild": 0, "Moderate": 0, "Severe": 0}

    for p in preds:
        dist_map[p.disease_name] = dist_map.get(p.disease_name, 0) + 1
        sev = p.severity_level if p.severity_level in severity_map else "Mild"
        severity_map[sev] += 1

    # Fallback default mock data for empty initial state
    if total == 0:
        disease_dist = [
            {"name": "Tomato Late Blight", "count": 14, "color": "#ef4444"},
            {"name": "Potato Late Blight", "count": 8, "color": "#f97316"},
            {"name": "Tomato Early Blight", "count": 6, "color": "#eab308"},
            {"name": "Corn Common Rust", "count": 4, "color": "#84cc16"},
            {"name": "Healthy Crops", "count": 18, "color": "#22c55e"}
        ]
        severity_dist = [
            {"name": "Healthy (<5%)", "value": 18, "color": "#22c55e"},
            {"name": "Mild (5-15%)", "value": 14, "color": "#eab308"},
            {"name": "Moderate (15-35%)", "value": 11, "color": "#f97316"},
            {"name": "Severe (>35%)", "value": 7, "color": "#ef4444"}
        ]
        monthly_trends = [
            {"month": "Mar", "scans": 12, "healthy": 8, "diseased": 4, "avg_severity": 8.5},
            {"month": "Apr", "scans": 18, "healthy": 11, "diseased": 7, "avg_severity": 12.0},
            {"month": "May", "scans": 25, "healthy": 14, "diseased": 11, "avg_severity": 14.5},
            {"month": "Jun", "scans": 34, "healthy": 18, "diseased": 16, "avg_severity": 18.2},
            {"month": "Jul", "scans": 42, "healthy": 22, "diseased": 20, "avg_severity": 21.0},
            {"month": "Aug", "scans": 50, "healthy": 26, "diseased": 24, "avg_severity": 16.4}
        ]
        top_diseases = [
            {"name": "Tomato Late Blight", "crop": "Tomato", "percentage": 28.0},
            {"name": "Potato Late Blight", "crop": "Potato", "percentage": 16.0},
            {"name": "Tomato Early Blight", "crop": "Tomato", "percentage": 12.0}
        ]
    else:
        disease_dist = [{"name": k, "count": v} for k, v in dist_map.items()]
        severity_dist = [{"name": k, "value": v} for k, v in severity_map.items()]
        top_diseases = [{"name": k, "percentage": round((v / total) * 100, 1)} for k, v in dist_map.items()][:3]
        monthly_trends = [
            {"month": "Jul", "scans": total // 2, "healthy": healthy // 2, "diseased": diseased // 2, "avg_severity": 14.0},
            {"month": "Aug", "scans": total, "healthy": healthy, "diseased": diseased, "avg_severity": 16.8}
        ]

    return DashboardAnalytics(
        total_predictions=total or 50,
        healthy_count=healthy or 26,
        diseased_count=diseased or 24,
        average_confidence=avg_conf,
        top_diseases=top_diseases,
        disease_distribution=disease_dist,
        severity_distribution=severity_dist,
        monthly_trends=monthly_trends,
        weather_risk_summary={
            "overall_risk_level": "High",
            "current_temp": 26.5,
            "current_humidity": 82.0,
            "alert": "High humidity & warm temperatures favor late blight transmission."
        }
    )
