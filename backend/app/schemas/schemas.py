from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: Optional[str] = "farmer"
    city: Optional[str] = "Pune"
    state: Optional[str] = "Maharashtra"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FirebaseLoginRequest(BaseModel):
    email: EmailStr
    full_name: Optional[str] = "Farmer User"
    firebase_uid: Optional[str] = None
    role: Optional[str] = "farmer"
    city: Optional[str] = "Pune"
    state: Optional[str] = "Maharashtra"

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    city: Optional[str] = None
    state: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# --- Farm Schemas ---
class FarmCreate(BaseModel):
    name: str
    location: Optional[str] = None
    crop_types: Optional[str] = "Tomato, Potato, Corn"
    area_acres: Optional[float] = 2.5

class FarmResponse(BaseModel):
    id: str
    user_id: str
    name: str
    location: Optional[str]
    crop_types: Optional[str]
    area_acres: float
    created_at: datetime

    class Config:
        from_attributes = True

# --- Recommendation Schema ---
class RecommendationResponse(BaseModel):
    id: str
    prediction_id: str
    disease_name: str
    crop: str
    symptoms: str
    organic_treatment: str
    chemical_treatment: str
    prevention: str
    general_guidance: str
    disclaimer: str

    class Config:
        from_attributes = True

# --- Stable Prediction Response Schema ---
class PredictionResponse(BaseModel):
    id: str
    image_url: str
    
    # Stable requested fields
    plant: str
    scientific_name: Optional[str] = "N/A"
    disease: str
    confidence: float
    severity: str
    severity_percentage: float
    affected_area: float
    risk: str
    recommendation: Optional[Dict[str, Any]] = None
    
    # Backward compatible fields
    crop_detected: str
    disease_name: str
    disease_code: str
    confidence_score: float
    severity_level: str
    affected_area_cm2: float
    weather_risk_level: str
    weather_risk_score: float
    ambient_temp_c: Optional[float] = 26.5
    humidity_pct: Optional[float] = 82.0
    rainfall_mm: Optional[float] = 5.0
    is_demo: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

# --- Weather Schemas ---
class WeatherRiskRequest(BaseModel):
    temperature_c: float
    humidity_pct: float
    rainfall_mm: float = 0.0
    crop: str = "Tomato"
    disease: Optional[str] = "Late Blight"

class WeatherRiskResponse(BaseModel):
    risk_score: float
    risk_level: str  # Low, Medium, High, Critical
    contributing_factors: List[str]
    advice: str

# --- Chat Schemas ---
class ChatMessageCreate(BaseModel):
    message: str
    session_id: Optional[str] = None
    prediction_id: Optional[str] = None

class ChatMessageResponse(BaseModel):
    id: str
    sender: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True

# --- Dashboard Analytics Schema ---
class DashboardAnalytics(BaseModel):
    total_predictions: int
    healthy_count: int
    diseased_count: int
    average_confidence: float
    top_diseases: List[dict]
    disease_distribution: List[dict]
    severity_distribution: List[dict]
    monthly_trends: List[dict]
    weather_risk_summary: dict
