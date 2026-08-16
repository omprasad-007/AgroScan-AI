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
from app.models.all_models import User, DiseaseInfo
from app.core.security import get_password_hash
from app.services.disease_knowledge_base import DISEASE_KNOWLEDGE_BASE

logger = logging.getLogger("agroscan")

# Auto-create tables for instant SQLite / PostgreSQL deployment
Base.metadata.create_all(bind=engine)

def seed_initial_data():
    db = SessionLocal()
    try:
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

# Global Zero-Crash Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred while processing your request. Please try again later.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )

# Security Middleware: Payload Size & Security Headers
@app.middleware("http")
async def security_and_limit_middleware(request: Request, call_next):
    # Check max content length to protect against OOM / DoS
    content_length = request.headers.get("content-length")
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if content_length:
        try:
            if int(content_length) > max_bytes:
                return JSONResponse(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    content={"detail": f"Payload size exceeds the maximum limit of {settings.MAX_UPLOAD_SIZE_MB}MB."}
                )
        except ValueError:
            pass

    response = await call_next(request)
    
    # Inject Security HTTP Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Configure CORS with strict allowed origins
origins = settings.ALLOWED_ORIGINS.copy()
if settings.FRONTEND_URL:
    origins.append(settings.FRONTEND_URL)

if settings.DEBUG:
    origins = list(set(origins + ["http://localhost:5173", "http://localhost:3000", "*"]))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if not settings.DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)

