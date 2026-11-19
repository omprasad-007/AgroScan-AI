# AgroScan AI — MobileNetV2 Model Setup Guide
**Hugging Face Model:** `neghani/plantvillage-mobilenetv2` (Revision: `v1.1`, Commit SHA: `77e6d262dca53b818f7ad1d67088700754515639`)

---

## 1. Overview

AgroScan AI integrates the **PlantVillage MobileNetV2** image classification model as its primary on-device/local disease diagnosis engine. The model is hosted locally inside `backend/models/plantvillage-mobilenetv2/`, operating in PyTorch CPU inference mode with zero external network calls required during prediction.

### Key Specifications
- **Repository ID:** `neghani/plantvillage-mobilenetv2`
- **Revision Tag:** `v1.1`
- **Immutable Commit SHA:** `77e6d262dca53b818f7ad1d67088700754515639`
- **Model Architecture:** `MobileNetV2ForImageClassification`
- **Base Architecture:** `google/mobilenet_v2_1.0_224`
- **File Format:** Safetensors (`model.safetensors`, 9.26 MB)
- **License:** Apache 2.0
- **Label Coverage:** 38 PlantVillage classes across 14 crop categories
- **Inference Mode:** PyTorch CPU (`torch.inference_mode()`, evaluation mode)
- **Calibration:** Temperature scaling ($T = 0.8845$)
- **Decision Threshold:** $\theta = 0.50$ (scores $< 0.50$ trigger `UNCERTAIN` warning status)

---

## 2. Hardware Requirements & Architecture Compatibility

| Component | Minimum Specification | Recommended / Development Machine |
|---|---|---|
| **Operating System** | Windows 10/11, Ubuntu 20.04+, macOS 12+ | Windows 11 Pro 64-bit |
| **Processor** | Dual-core 2.0 GHz x86_64 | Intel Core i5 (Dell Latitude 5420) |
| **RAM** | 4 GB | 8 GB or 16 GB |
| **Storage** | 500 MB free disk space | 512 GB NVMe SSD |
| **GPU** | Not required (CPU inference default) | NVIDIA Quadro / Intel Iris Xe (CPU mode) |
| **Python Version** | Python 3.10 – 3.14 | Python 3.14.6 in virtual environment |

> [!NOTE]
> The inference service automatically detects whether CUDA is genuinely available and functional using `torch.cuda.is_available()`. If CUDA is absent, not initialized, or incompatible, it cleanly defaults to PyTorch CPU inference without errors or warnings.

---

## 3. Python Dependencies & Installation

All required Python libraries are configured in [backend/requirements.txt](file:///d:/Projects/AgroScan%20AI/backend/requirements.txt).

```bash
# 1. Activate the Python virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows Command Prompt:
.\.venv\Scripts\activate.bat

# 2. Upgrade pip and install backend dependencies
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

### Core Dependency Matrix
| Package | Version Installed | Purpose |
|---|---|---|
| `torch` | `2.15.0+cpu` | PyTorch runtime tensor operations & neural network execution |
| `transformers` | `5.23.0` | Hugging Face model loading (`AutoImageProcessor`, `AutoModelForImageClassification`) |
| `huggingface-hub` | `2.4.0` | Snapshot download, revision verification, commit SHA pinning |
| `safetensors` | `0.8.0` | Fast, zero-copy, secure tensor deserialization |
| `pillow` | `12.0.0` | Image loading, resizing, format conversion, and leaf quality checks |
| `numpy` | `2.4.0` | Array manipulation and probability calibration calculations |
| `fastapi` | `0.115.0+` | Asynchronous REST API routing and request handling |
| `uvicorn` | `0.30.0+` | ASGI web server |

---

## 4. Local Model Directory Structure

The model files are stored in `backend/models/plantvillage-mobilenetv2/`:

```
backend/models/
├── model_manifest.json          # Machine-readable manifest with SHA-256 hashes
└── plantvillage-mobilenetv2/
    ├── config.json              # Model configuration (38 labels, MobileNetV2)
    ├── model.safetensors        # Safetensors weights (9,264,680 bytes)
    ├── preprocessor_config.json # Image processor configuration (224x224, normalize)
    ├── calibration.json         # Temperature scaling parameter (T = 0.8845188)
    ├── threshold.json           # Decision threshold configuration (theta = 0.50)
    ├── eval_results.json        # Benchmark evaluation metrics
    ├── README.md                # Hugging Face model card
    └── reports/                 # Evaluation reports and confusion matrix
```

> [!IMPORTANT]
> The weights file `*.safetensors` is excluded from Git tracking via `.gitignore` to prevent large binary blobs in source control, while `backend/models/model_manifest.json` is committed to guarantee reproducible builds.

---

## 5. Environment Configuration

Copy or verify your environment configuration in `backend/.env`:

```env
# ML Engine Configuration
MODEL_TYPE="huggingface"
DEFAULT_LOCAL_MODEL="neghani/plantvillage-mobilenetv2"
LOCAL_INFERENCE_ENABLED=true
CONFIDENCE_CALIBRATION_TEMPERATURE=0.8845
HIGH_CONFIDENCE_THRESHOLD=0.70
MODERATE_CONFIDENCE_THRESHOLD=0.50
UPLOAD_DIR="./uploads"

# Database & Security
DATABASE_URL="sqlite:///./agroscan.db"
SECRET_KEY="your_super_secret_jwt_key_change_in_production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## 6. Starting the FastAPI Application

Start the FastAPI application using Uvicorn:

```bash
# Run from the repository root:
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

When the application boots, `PlantDiseaseModelService` initializes via lazy-loading on first use or upon calling the `/api/model/health` endpoint:

```
[AgroScan AI] Initializing PlantDiseaseModelService (CPU inference mode)
[AgroScan AI] Loading model from: d:\Projects\AgroScan AI\backend\models\plantvillage-mobilenetv2
[AgroScan AI] Model loaded successfully: 38 labels, calibration T=0.8845, threshold=0.50
```

---

## 7. Model API Endpoints & Verification

### 7.1 Model Health Check
```bash
curl -X GET http://127.0.0.1:8000/api/model/health
```
**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu",
  "label_count": 38,
  "calibration_temperature": 0.8845188130635788,
  "uncertainty_threshold": 0.5
}
```

### 7.2 Model Metadata & Manifest Information
```bash
curl -X GET http://127.0.0.1:8000/api/model/info
```

### 7.3 List Supported 38 Disease Labels
```bash
curl -X GET http://127.0.0.1:8000/api/model/labels
```

### 7.4 Query Crop Registry Support
```bash
curl -X GET "http://127.0.0.1:8000/api/model/crops?crop_name=Tomato"
```
**Response:**
```json
{
  "crop_name": "Tomato",
  "status": "SUPPORTED",
  "scientific_name": "Solanum lycopersicum",
  "supported_labels": [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
  ],
  "disease_count": 10
}
```

### 7.5 Direct Model Inference
```bash
curl -X POST http://127.0.0.1:8000/api/model/predict \
  -F "file=@tests/sample_leaf.jpg" \
  -F "crop_name=Tomato"
```

---

## 8. Troubleshooting

| Issue | Root Cause | Solution |
|---|---|---|
| `model.safetensors not found` | Model was not downloaded or directory path is incorrect | Run snapshot download script or verify `backend/models/plantvillage-mobilenetv2/model.safetensors` exists. |
| `CUDA out of memory` / `CUDA initialization error` | Incompatible GPU driver or missing CUDA toolkit | The model service automatically falls back to CPU. You can also explicitly set device to CPU in `backend/app/services/plant_disease_model.py`. |
| `UNSUPPORTED_CROP` returned | Uploaded crop is outside the 14 MobileNetV2 crops (e.g. Sugarcane, Cotton) | This is an expected safety guardrail. The system routes unsupported crops to external providers (Plant.id/Gemini) or botanical visual analysis. |
| `INVALID_IMAGE: NON_LEAF_SELFIE` | Uploaded image failed the leaf suitability pre-check | Upload a clear, focused photograph of a plant leaf under adequate lighting. |
