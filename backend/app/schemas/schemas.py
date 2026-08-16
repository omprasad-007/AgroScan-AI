from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Location Schema ---
class LocationSchema(BaseModel):
    village: Optional[str] = "Kagal"
    taluka: Optional[str] = "Kagal"
    district: Optional[str] = "Kolhapur"
    state: Optional[str] = "Maharashtra"
    pincode: Optional[str] = "416216"
    city: Optional[str] = "Kolhapur"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# --- Auth & User Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: Optional[str] = "farmer"
    village: Optional[str] = "Kagal"
    taluka: Optional[str] = "Kagal"
    district: Optional[str] = "Kolhapur"
    state: Optional[str] = "Maharashtra"
    pincode: Optional[str] = "416216"
    city: Optional[str] = "Kolhapur"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    city: Optional[str] = None
    language: Optional[str] = None

class FirebaseLoginRequest(BaseModel):
    email: EmailStr
    full_name: Optional[str] = "Farmer User"
    firebase_uid: Optional[str] = None
    role: Optional[str] = "farmer"
    village: Optional[str] = "Kagal"
    taluka: Optional[str] = "Kagal"
    district: Optional[str] = "Kolhapur"
    state: Optional[str] = "Maharashtra"
    pincode: Optional[str] = "416216"
    city: Optional[str] = "Kolhapur"

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    city: Optional[str] = None
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
    village: Optional[str] = "Kagal"
    taluka: Optional[str] = "Kagal"
    district: Optional[str] = "Kolhapur"
    state: Optional[str] = "Maharashtra"
    pincode: Optional[str] = "416216"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_source: Optional[str] = "MANUAL"
    gps_accuracy: Optional[float] = None
    crop_types: Optional[str] = "Tomato, Potato, Sugarcane"
    area_acres: Optional[float] = 2.5
    irrigation_type: Optional[str] = "Drip Irrigation"

class FarmUpdate(BaseModel):
    name: Optional[str] = None
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_source: Optional[str] = None
    gps_accuracy: Optional[float] = None
    crop_types: Optional[str] = None
    area_acres: Optional[float] = None
    irrigation_type: Optional[str] = None

class FarmResponse(BaseModel):
    id: str
    user_id: str
    name: str
    village: Optional[str]
    taluka: Optional[str]
    district: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_source: Optional[str] = "MANUAL"
    gps_accuracy: Optional[float] = None
    crop_types: Optional[str]
    area_acres: float
    irrigation_type: Optional[str] = "Drip Irrigation"
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Disease & Prediction Schemas ---
class DiseaseInfoResponse(BaseModel):
    id: str
    disease_code: str
    crop: str
    disease_name: str
    scientific_name: Optional[str] = None
    symptoms: str
    organic_treatment: str
    chemical_treatment: str
    prevention: str

    class Config:
        from_attributes = True

class RecommendationResponse(BaseModel):
    organic_treatment: str
    chemical_treatment: str
    prevention: str
    disclaimer: Optional[str] = "Decision-support guidance only. Follow locally approved product labels."

class PredictionResponse(BaseModel):
    id: str
    image_url: str
    plant: str
    scientific_name: Optional[str] = "Solanum lycopersicum"
    disease: str
    confidence: float
    severity: str
    severity_percentage: float
    affected_area: float
    risk: str
    recommendation: Dict[str, Any]
    
    # Backward compatibility aliases
    crop_detected: Optional[str] = None
    disease_name: Optional[str] = None
    severity_level: Optional[str] = None
    confidence_score: Optional[float] = None
    weather_risk_level: Optional[str] = None
    is_demo: Optional[bool] = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Analytics & Weather Schemas ---
class DashboardAnalyticsResponse(BaseModel):
    total_predictions: int
    healthy_count: int
    diseased_count: int
    average_confidence: float
    disease_distribution: List[Dict[str, Any]]
    severity_distribution: List[Dict[str, Any]]
    monthly_trends: List[Dict[str, Any]]
    weather_risk_summary: Dict[str, Any]

DashboardAnalytics = DashboardAnalyticsResponse

class WeatherRiskRequest(BaseModel):
    crop: Optional[str] = "Tomato"
    disease: Optional[str] = "Late Blight"
    temperature_c: Optional[float] = 26.5
    humidity_pct: Optional[float] = 82.0
    rainfall_mm: Optional[float] = 5.0

class WeatherRiskResponse(BaseModel):
    crop: Optional[str] = "Tomato"
    pathogen: Optional[str] = "Pathogen"
    risk_score: float
    risk_level: str
    contributing_factors: List[str]
    advice: str

# --- Chat Schemas ---
class ChatMessageCreate(BaseModel):
    message: str
    session_id: Optional[str] = None
    prediction_id: Optional[str] = None
    language: Optional[str] = "en"
    manual_plant: Optional[str] = None

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
