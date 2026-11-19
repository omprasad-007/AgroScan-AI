# AgroScan AI — Local Developer Setup & Operations Guide
**Document:** Local First Development, Model Caching, and Operational Procedures  
**Target Environment:** Local Machine (Windows / Linux / macOS)  

---

## 1. System Requirements

- **Python:** 3.10 to 3.14 (Python 3.14.6 verified)
- **Node.js:** v18.0.0 or higher (v20+ recommended)
- **RAM:** Minimum 4 GB RAM (8 GB recommended for concurrent transformer execution)
- **Disk Space:** ~500 MB for Python/Node packages + ~50 MB for cached model weights
- **Hardware Acceleration:** CPU inference is default and fully functional (~18 ms latency); NVIDIA CUDA GPU will be automatically utilized if present.

---

## 2. Step-by-Step Installation

### Step 1: Clone Repository & Setup Virtual Environment
```bash
# Navigate to project root
cd "d:\Projects\AgroScan AI"

# Create a virtual environment (if not already existing)
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows Command Prompt:
.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate
```

### Step 2: Install Python Dependencies
```bash
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```
Key packages installed: `fastapi`, `uvicorn`, `torch`, `torchvision`, `transformers`, `huggingface-hub`, `numpy`, `pillow`, `opencv-python-headless`, `sqlalchemy`, `pydantic`.

### Step 3: Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

---

## 3. Environment Variable Configuration

AgroScan AI comes with template files. Create or verify your local `.env`:

```bash
# Copy backend template
copy backend\.env.example backend\.env
```

**Key Configuration Settings in `backend/.env`:**
```ini
APP_NAME="AgroScan AI"
APP_ENV="development"
DEBUG=true
PORT=8000
DEMO_MODE=false

# SQLite Local Database
DATABASE_URL="sqlite:///./agroscan.db"

# JWT Security
SECRET_KEY="your_super_secret_jwt_key_local_development"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Local Hugging Face Model Settings
MODEL_TYPE="huggingface"
DEFAULT_LOCAL_MODEL="neghani/plantvillage-mobilenetv2"
SECONDARY_LOCAL_MODEL="rodynaemad/plant-disease-dinov2-small"
MODEL_CACHE_DIR="./models_cache"
LOCAL_INFERENCE_ENABLED=true
HF_INFERENCE_TIMEOUT=8.0
CONFIDENCE_CALIBRATION_TEMPERATURE=0.8845

# Optional External API Keys (Leave blank or set if available)
PLANT_ID_API_KEY=""
GEMINI_API_KEY=""
WEATHER_API_KEY=""
```

*Note: AgroScan AI operates 100% locally with zero external API keys! If external keys are omitted, the local Hugging Face vision engine performs the complete diagnosis.*

---

## 4. Running the Application Locally

### Starting the FastAPI Backend
```bash
# In active .venv
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --app-dir backend
```
- API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`
- Health Check Endpoint: `http://127.0.0.1:8000/health`
- Model & Provider Health: `http://127.0.0.1:8000/api/v1/predictions/providers/health`

### Starting the React Frontend
```bash
cd frontend
npm run dev
```
- Frontend UI: `http://localhost:5173`

---

## 5. Automated Verification & Testing Commands

### Run Full Test Suite (52 Tests)
```bash
# In project root with .venv active
python -m pytest tests/test_leaf_scan_pipeline.py tests/test_hybrid_ai_engine.py tests/test_backend.py
```

### Build Production Frontend
```bash
cmd /c "npm --prefix frontend run build"
```

---

## 6. Common Errors and Troubleshooting

| Error | Root Cause | Solution |
|---|---|---|
| `ValueError: I/O operation on closed file` during pytest | Pytest capture conflict with Python 3.14 on Windows | Run pytest with `-s` flag or verify `addopts = "-s"` in `pyproject.toml`. |
| `ps1 cannot be loaded because running scripts is disabled` | Windows PowerShell execution policy restricts `.ps1` | Run commands via `cmd /c npm ...` or run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. |
| `Model file not found` / Hugging Face download timeout | First-time model download interrupted by network drop | The model will retry download automatically on next scan, or pre-cache weights by importing `ModelRegistry.load_model('neghani/plantvillage-mobilenetv2')`. |
| `HTTP 400 No clear leaf was detected` | Uploaded image is a selfie, animal, document, or blurry photo | Stage 1 validation gate intentionally rejected the image. Upload a clear, close-up photo of an actual plant leaf. |
