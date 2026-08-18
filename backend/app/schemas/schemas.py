from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Location Schema ---
class LocationSchema(BaseModel):
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# --- Auth & User Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: Optional[str] = "farmer"
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    city: Optional[str] = None

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
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class FirebaseLoginRequest(BaseModel):
    email: EmailStr
    full_name: Optional[str] = "Farmer User"
    firebase_uid: Optional[str] = None
    role: Optional[str] = "farmer"
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    city: Optional[str] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# --- Farm Schemas ---
class FarmCreate(BaseModel):
    name: str
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_source: Optional[str] = "MANUAL"
    gps_accuracy: Optional[float] = None
    crop_types: Optional[str] = "General Crops"
    area_acres: Optional[float] = 1.0
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
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    name: str
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_source: Optional[str] = "MANUAL"
    gps_accuracy: Optional[float] = None
    crop_types: Optional[str] = None
    area_acres: float
    irrigation_type: Optional[str] = "Drip Irrigation"
    created_at: datetime
    updated_at: Optional[datetime] = None

# --- Disease & Prediction Schemas ---
class DiseaseInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    disease_code: str
    crop: str
    disease_name: str
    scientific_name: Optional[str] = None
    symptoms: str
    organic_treatment: str
    chemical_treatment: str
    prevention: str

class RecommendationResponse(BaseModel):
    organic_treatment: str
    chemical_treatment: str
    prevention: str
    disclaimer: Optional[str] = "Decision-support guidance only. Follow locally approved product labels."

class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    image_url: str
    plant: str
    scientific_name: Optional[str] = None
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
    is_demo: Optional[bool] = False
    created_at: Optional[datetime] = None

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
    conversation_history: Optional[List[Dict[str, str]]] = None
    location: Optional[Dict[str, Any]] = None

class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: Optional[str] = None
    sender: str
    content: str
    created_at: datetime

class ChatSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    created_at: datetime
    messages: List[ChatMessageResponse] = []
