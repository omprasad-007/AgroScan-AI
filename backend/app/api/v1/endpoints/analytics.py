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

    # Return genuine blank state if no scans exist
    if total == 0:
        disease_dist = []
        severity_dist = []
        monthly_trends = []
        top_diseases = []
        weather_summary = {
            "overall_risk_level": "None",
            "current_temp": 26.5,
            "current_humidity": 65.0,
            "alert": "No leaf scans recorded yet. Scan a plant leaf to start tracking health and disease risk."
        }
    else:
        disease_dist = [{"name": k, "count": v} for k, v in dist_map.items()]
        severity_dist = [{"name": k, "value": v} for k, v in severity_map.items()]
        top_diseases = [{"name": k, "percentage": round((v / total) * 100, 1)} for k, v in dist_map.items()][:3]
        monthly_trends = [
            {"month": "Recent", "scans": total, "healthy": healthy, "diseased": diseased, "avg_severity": 15.0}
        ]
        # Determine highest risk level from recent scans
        recent_risks = [p.weather_risk_level for p in preds if p.weather_risk_level]
        top_risk = "High" if "High" in recent_risks else ("Moderate" if "Moderate" in recent_risks else "Low")
        latest_pred = preds[-1]
        weather_summary = {
            "overall_risk_level": top_risk,
            "current_temp": latest_pred.ambient_temp_c or 26.5,
            "current_humidity": latest_pred.humidity_pct or 75.0,
            "alert": f"Active monitoring for {latest_pred.crop_detected} ({latest_pred.disease_name})."
        }

    return DashboardAnalytics(
        total_predictions=total,
        healthy_count=healthy,
        diseased_count=diseased,
        average_confidence=avg_conf if total > 0 else 0.0,
        top_diseases=top_diseases,
        disease_distribution=disease_dist,
        severity_distribution=severity_dist,
        monthly_trends=monthly_trends,
        weather_risk_summary=weather_summary
    )
