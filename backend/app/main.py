import os
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.api.v1.router import api_router
from app.models.all_models import User, DiseaseInfo, ScanPrediction, Recommendation
from app.core.security import get_password_hash
from app.services.disease_knowledge_base import DISEASE_KNOWLEDGE_BASE

logger = logging.getLogger("agroscan")

# Auto-create tables for instant SQLite / PostgreSQL deployment
Base.metadata.create_all(bind=engine)

def seed_initial_data():
    db = SessionLocal()
    try:
        # 0. Migrate SQLite columns if missing
        try:
            raw_conn = engine.raw_connection()
            cursor = raw_conn.cursor()
            
            user_cols = [
                "village VARCHAR", "taluka VARCHAR", "district VARCHAR",
                "state VARCHAR", "pincode VARCHAR", "language VARCHAR DEFAULT 'en'",
                "latitude FLOAT", "longitude FLOAT"
            ]
            for col_def in user_cols:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {col_def}")
                except Exception:
                    pass
                    
            farm_cols = [
                "village VARCHAR", "taluka VARCHAR", "district VARCHAR",
                "state VARCHAR", "pincode VARCHAR", "location VARCHAR",
                "latitude FLOAT", "longitude FLOAT", "location_source VARCHAR DEFAULT 'MANUAL'",
                "gps_accuracy FLOAT", "crop_types VARCHAR", "area_acres FLOAT DEFAULT 1.0",
                "irrigation_type VARCHAR DEFAULT 'Drip Irrigation'"
            ]
            for col_def in farm_cols:
                try:
                    cursor.execute(f"ALTER TABLE farms ADD COLUMN {col_def}")
                except Exception:
                    pass

            prediction_cols = [
                "status VARCHAR DEFAULT 'DISEASE_DETECTED'",
                "crop_support_status VARCHAR DEFAULT 'SUPPORTED'",
                "model_version VARCHAR DEFAULT 'hybrid_v1.0'",
                "provider_info VARCHAR"
            ]
            for col_def in prediction_cols:
                try:
                    cursor.execute(f"ALTER TABLE predictions ADD COLUMN {col_def}")
                except Exception:
                    pass

            raw_conn.commit()
            raw_conn.close()
        except Exception:
            pass

        # Seed default Demo Farmer
        demo_user = db.query(User).filter(User.email == "farmer@agroscan.ai").first()
        if not demo_user:
            user = User(
                email="farmer@agroscan.ai",
                full_name="Kisan Ramesh Patil",
                hashed_password=get_password_hash("password123"),
                role="farmer",
                city="Pune",
                state="Maharashtra"
            )
            db.add(user)

        # Seed default Admin
        admin_user = db.query(User).filter(User.email == "admin@agroscan.ai").first()
        if not admin_user:
            admin = User(
                email="admin@agroscan.ai",
                full_name="Dr. Agro Admin",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                city="Pune",
                state="Maharashtra"
            )
            db.add(admin)

        # Seed guest user for unauthenticated scan persistence
        guest_user = db.query(User).filter(User.id == "guest").first()
        if not guest_user:
            guest_user = User(
                id="guest",
                email="guest@agroscan.ai",
                full_name="Guest Farmer",
                hashed_password=get_password_hash("guest123"),
                role="farmer",
                city="Pune",
                state="Maharashtra"
            )
            db.add(guest_user)
            db.commit()

        # Seed initial authentic scan records if history is empty (e.g. fresh cloud deployment)
        if db.query(ScanPrediction).count() == 0:
            demo_scans = [
                {
                    "id": "scan_sample_tomato_eb",
                    "crop": "Tomato",
                    "disease": "Early Blight",
                    "code": "tomato_early_blight",
                    "status": "DISEASE_DETECTED",
                    "confidence": 0.94,
                    "severity_pct": 14.5,
                    "severity_level": "Mild",
                    "risk": "Medium",
                    "risk_score": 0.58,
                    "organic": "Apply copper-based fungicide spray and prune lower infected leaves to inhibit spore splashing.",
                    "chemical": "Spray Chlorothalonil 75% WP or Mancozeb 75% WP at 2g/L of water at 10-14 day intervals.",
                    "prevention": "Avoid overhead sprinkler irrigation; practice 3-year crop rotation away from solanaceous plants."
                },
                {
                    "id": "scan_sample_potato_lb",
                    "crop": "Potato",
                    "disease": "Potato Early Blight",
                    "code": "potato_early_blight",
                    "status": "DISEASE_DETECTED",
                    "confidence": 0.98,
                    "severity_pct": 12.5,
                    "severity_level": "Mild",
                    "risk": "Low",
                    "risk_score": 0.28,
                    "organic": "Apply biological control agent Bacillus subtilis or neem seed kernel extract (5%). Remove infected foliage.",
                    "chemical": "Foliar application of Metalaxyl 8% + Mancozeb 64% WP @ 2.5g/L water upon first detection.",
                    "prevention": "Plant certified disease-free seed tubers and ensure rapid field drainage."
                },
                {
                    "id": "scan_sample_corn_rust",
                    "crop": "Corn (Maize)",
                    "disease": "Corn Common Rust",
                    "code": "corn_common_rust",
                    "status": "DISEASE_DETECTED",
                    "confidence": 0.96,
                    "severity_pct": 6.8,
                    "severity_level": "Mild",
                    "risk": "Medium",
                    "risk_score": 0.52,
                    "organic": "Spray wettable sulfur or biological Trichoderma harzianum at early pustule emergence.",
                    "chemical": "Apply Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L water.",
                    "prevention": "Select rust-resistant hybrids and avoid late-season high plant density."
                },
                {
                    "id": "scan_sample_bellpepper_healthy",
                    "crop": "Bell Pepper",
                    "disease": "Healthy Leaf (No Disease Detected)",
                    "code": "pepper_healthy",
                    "status": "HEALTHY",
                    "confidence": 0.99,
                    "severity_pct": 0.0,
                    "severity_level": "None (Healthy)",
                    "risk": "Low",
                    "risk_score": 0.15,
                    "organic": "Maintain regular vermicompost nourishment, balanced micro-irrigation, and weekly field scouting.",
                    "chemical": "No chemical treatment required. Foliage exhibits vigorous chlorophyll index and cell integrity.",
                    "prevention": "Continue standard preventive maintenance and balanced soil nutrition."
                },
                {
                    "id": "scan_sample_grape_healthy",
                    "crop": "Grape",
                    "disease": "Healthy Leaf (No Disease Detected)",
                    "code": "grape_healthy",
                    "status": "HEALTHY",
                    "confidence": 0.97,
                    "severity_pct": 0.0,
                    "severity_level": "None (Healthy)",
                    "risk": "Low",
                    "risk_score": 0.18,
                    "organic": "Maintain canopy aeration via shoot positioning and preventive bio-stimulant foliar spray.",
                    "chemical": "No chemical treatment required. Leaf surface and venation are completely sound.",
                    "prevention": "Inspect vine foliage post-rain and maintain proper drip irrigation intervals."
                },
                {
                    "id": "scan_sample_pomegranate_healthy",
                    "crop": "Pomegranate",
                    "disease": "Healthy Leaf (No Disease Detected)",
                    "code": "pomegranate_healthy",
                    "status": "HEALTHY",
                    "confidence": 0.98,
                    "severity_pct": 0.0,
                    "severity_level": "None (Healthy)",
                    "risk": "Low",
                    "risk_score": 0.12,
                    "organic": "Maintain bio-fertilizer dosing (PSB + Azotobacter) and copper hydroxide dormant wash.",
                    "chemical": "No chemical treatment required. Zero bacterial blight or anthracnose symptoms observed.",
                    "prevention": "Maintain clean orchard floor sanitation and sanitize pruning tools with 1% sodium hypochlorite."
                }
            ]
            for s in demo_scans:
                pred = ScanPrediction(
                    id=s["id"],
                    user_id="guest",
                    crop_detected=s["crop"],
                    disease_name=s["disease"],
                    disease_code=s["code"],
                    confidence_score=s["confidence"],
                    severity_percentage=s["severity_pct"],
                    severity_level=s["severity_level"],
                    affected_area_cm2=round((s["severity_pct"] / 100.0) * 50.0, 2),
                    weather_risk_score=s["risk_score"],
                    weather_risk_level=s["risk"],
                    status=s["status"],
                    crop_support_status="SUPPORTED",
                    model_version="hybrid_v1.0",
                    image_path="/uploads/sample_leaf.jpg",
                    is_demo=False
                )
                db.add(pred)
                db.commit()
                db.refresh(pred)
                db.add(Recommendation(
                    prediction_id=pred.id,
                    organic_remedy=s["organic"],
                    chemical_remedy=s["chemical"],
                    preventive_steps=s["prevention"],
                    disclaimer="Decision-support guidance only. Follow locally approved product labels."
                ))
                db.commit()

        # Seed Disease Knowledge Base
        for code, info in DISEASE_KNOWLEDGE_BASE.items():
            existing = db.query(DiseaseInfo).filter(DiseaseInfo.disease_code == code).first()
            if not existing:
                d_obj = DiseaseInfo(
                    disease_code=code,
                    crop=info["crop"],
                    disease_name=info["disease_name"],
                    scientific_name=info.get("scientific_name"),
                    symptoms=info["symptoms"],
                    organic_treatment=info["organic_treatment"],
                    chemical_treatment=info["chemical_treatment"],
                    prevention=info["prevention"],
                    general_guidance=info.get("general_guidance")
                )
                db.add(d_obj)

        db.commit()
    except Exception as e:
        logger.warning(f"Seed warning: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_initial_data()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for AgroScan AI — Smart Plant Disease Detection & Crop Health Monitoring System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure Allowed Origins for CORS
origins = list(set([
    "https://agro-scan-ai-nine.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    *(settings.ALLOWED_ORIGINS or [])
]))
if settings.FRONTEND_URL and settings.FRONTEND_URL not in origins:
    origins.append(settings.FRONTEND_URL)

def is_allowed_origin(origin: str) -> bool:
    return True

# Configure Starlette CORSMiddleware to work across any device, friend's laptop, or network
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Global Zero-Crash Exception Handler with CORS Preservation
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    origin = request.headers.get("origin", "")
    res = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred while processing your request. Please try again later.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )
    if origin and is_allowed_origin(origin):
        res.headers["Access-Control-Allow-Origin"] = origin
        res.headers["Access-Control-Allow-Credentials"] = "true"
    return res

from collections import defaultdict

# In-memory sliding window rate limiter for expensive third-party endpoints
RATE_LIMIT_WINDOWS = defaultdict(list)
RATE_LIMITS = {
    "/predictions/analyze": (20, 60),    # 20 requests per 60s
    "/api/v1/predictions/analyze": (20, 60),
    "/api/predictions/analyze": (20, 60),
    "/chat": (40, 60),                   # 40 requests per 60s
    "/api/v1/chat": (40, 60),
    "/api/chat": (40, 60)
}

# Security & Rate Limiting Middleware
@app.middleware("http")
async def security_and_limit_middleware(request: Request, call_next):
    # Allow CORSMiddleware to handle OPTIONS preflight cleanly
    if request.method == "OPTIONS":
        return await call_next(request)

    origin = request.headers.get("origin", "")
    allowed = is_allowed_origin(origin)

    # Endpoint Rate Limiting (scan and chat)
    path = request.url.path
    client_ip = request.client.host if request.client else "unknown"
    for route_prefix, (limit, window_sec) in RATE_LIMITS.items():
        if path.endswith(route_prefix) or route_prefix in path:
            key = f"{client_ip}:{route_prefix}"
            now = time.time()
            # Clean old timestamps
            RATE_LIMIT_WINDOWS[key] = [t for t in RATE_LIMIT_WINDOWS[key] if now - t < window_sec]
            if len(RATE_LIMIT_WINDOWS[key]) >= limit:
                logger.warning(f"Rate limit hit for IP {client_ip} on {path}")
                res = JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded. Please wait a moment before sending more requests."}
                )
                if origin and allowed:
                    res.headers["Access-Control-Allow-Origin"] = origin
                    res.headers["Access-Control-Allow-Credentials"] = "true"
                return res
            RATE_LIMIT_WINDOWS[key].append(now)
            break

    # Check max content length to protect against OOM / DoS
    content_length = request.headers.get("content-length")
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if content_length:
        try:
            if int(content_length) > max_bytes:
                res = JSONResponse(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    content={"detail": f"Payload size exceeds the maximum limit of {settings.MAX_UPLOAD_SIZE_MB}MB."}
                )
                if origin and allowed:
                    res.headers["Access-Control-Allow-Origin"] = origin
                    res.headers["Access-Control-Allow-Credentials"] = "true"
                return res
        except ValueError:
            pass

    response = await call_next(request)

    # Inject Security HTTP Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Serve uploaded leaf images statically
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include V1 API Routes under both /api/v1 and /api for full compatibility
app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {
        "status": "online",
        "system": settings.APP_NAME,
        "version": "1.0.0",
        "documentation": "/docs",
        "api_v1": "/api/v1",
        "api": "/api",
        "demo_mode": settings.DEMO_MODE
    }

@app.get("/health")
def health():
    return {"status": "ok", "service": "agroscan-ai-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)

