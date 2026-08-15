import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="farmer") # "farmer", "agronomist", "admin"
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    farms = relationship("Farm", back_populates="owner", cascade="all, delete-orphan")
    predictions = relationship("ScanPrediction", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")


class Farm(Base):
    __tablename__ = "farms"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    crop_types = Column(String, nullable=True) # comma separated or JSON string
    area_acres = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="farms")
    predictions = relationship("ScanPrediction", back_populates="farm")


class DiseaseInfo(Base):
    __tablename__ = "diseases"

    id = Column(String, primary_key=True, default=generate_uuid)
    disease_code = Column(String, unique=True, index=True, nullable=False) # e.g. "tomato_late_blight"
    crop = Column(String, nullable=False)
    disease_name = Column(String, nullable=False)
    scientific_name = Column(String, nullable=True)
    symptoms = Column(Text, nullable=False)
    organic_treatment = Column(Text, nullable=False)
    chemical_treatment = Column(Text, nullable=False)
    prevention = Column(Text, nullable=False)
    general_guidance = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    recommendations = relationship("Recommendation", back_populates="disease_info")


class ScanPrediction(Base):
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    farm_id = Column(String, ForeignKey("farms.id"), nullable=True)
    
    image_path = Column(String, nullable=False)
    crop_detected = Column(String, nullable=False)
    disease_name = Column(String, nullable=False)
    disease_code = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    
    severity_percentage = Column(Float, default=0.0)
    severity_level = Column(String, default="Mild") # Healthy, Mild, Moderate, Severe
    affected_area_cm2 = Column(Float, default=0.0)
    
    ambient_temp_c = Column(Float, nullable=True)
    humidity_pct = Column(Float, nullable=True)
    rainfall_mm = Column(Float, nullable=True)
    weather_risk_score = Column(Float, default=0.0)
    weather_risk_level = Column(String, default="Low") # Low, Medium, High, Critical
    
    is_demo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="predictions")
    farm = relationship("Farm", back_populates="predictions")
    recommendations = relationship("Recommendation", back_populates="prediction", cascade="all, delete-orphan")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, default=generate_uuid)
    prediction_id = Column(String, ForeignKey("predictions.id"), nullable=False)
    disease_id = Column(String, ForeignKey("diseases.id"), nullable=True)
    
    organic_remedy = Column(Text, nullable=False)
    chemical_remedy = Column(Text, nullable=False)
    preventive_steps = Column(Text, nullable=False)
    disclaimer = Column(Text, default="Decision-support guidance only. Follow locally approved product labels.")
    created_at = Column(DateTime, default=datetime.utcnow)

    prediction = relationship("ScanPrediction", back_populates="recommendations")
    disease_info = relationship("DiseaseInfo", back_populates="recommendations")


class WeatherRecord(Base):
    __tablename__ = "weather"

    id = Column(String, primary_key=True, default=generate_uuid)
    location = Column(String, nullable=False)
    temperature_c = Column(Float, nullable=False)
    humidity_pct = Column(Float, nullable=False)
    rainfall_mm = Column(Float, default=0.0)
    recorded_at = Column(DateTime, default=datetime.utcnow)


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, default="Agronomy Chat")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False)
    sender = Column(String, nullable=False) # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
