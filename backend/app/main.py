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
        # 0. Migrate SQLite columns if missing
        try:
            with engine.connect() as conn:
                for col_def in [
                    "village VARCHAR", "taluka VARCHAR", "district VARCHAR",
                    "state VARCHAR", "pincode VARCHAR", "latitude FLOAT", "longitude FLOAT"
                ]:
                    col_name = col_def.split()[0]
                    try:
                        conn.execute(Base.metadata.schema and None or engine.raw_connection().cursor().execute(f"ALTER TABLE users ADD COLUMN {col_def}"))
                    except Exception:
                        pass
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

from fastapi.responses import JSONResponse, Response
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

def is_allowed_origin(origin: str) -> bool:
    if not origin:
        return True
    if origin in origins:
        return True
    # Allow localhost / 127.0.0.1 and vercel preview domains
    if origin.startswith("http://localhost:") or origin.startswith("http://127.0.0.1:"):
        return True
    if origin.endswith(".vercel.app"):
        return True
    return False

# Security & CORS Middleware: Origin Verification, Rate Limiting, Payload Size & Headers
@app.middleware("http")
async def security_and_limit_middleware(request: Request, call_next):
    origin = request.headers.get("origin", "")
    allowed = is_allowed_origin(origin)

    # Clean preflight OPTIONS handling to prevent CORS block on browser preflight
    if request.method == "OPTIONS":
        res = Response(status_code=204)
        if origin and allowed:
            res.headers["Access-Control-Allow-Origin"] = origin
            res.headers["Access-Control-Allow-Credentials"] = "true"
            res.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            res.headers["Access-Control-Allow-Headers"] = "*"
        return res

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
    
    # Guarantee CORS Headers on authorized origins
    if origin and allowed:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "*"

    # Inject Security HTTP Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Configure Starlette CORSMiddleware as fallback
origins = settings.ALLOWED_ORIGINS.copy()
if settings.FRONTEND_URL and settings.FRONTEND_URL not in origins:
    origins.append(settings.FRONTEND_URL)

if "https://agro-scan-ai-nine.vercel.app" not in origins:
    origins.append("https://agro-scan-ai-nine.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
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

@app.get("/health")
def health():
    return {"status": "ok", "service": "agroscan-ai-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)

