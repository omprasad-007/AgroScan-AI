# AgroScan AI — Model Integration Audit
**Date:** 2026-11-19  
**System:** Windows 11, Intel Core i5, 8 GB RAM, Dell Latitude 5420  
**Target Model:** `neghani/plantvillage-mobilenetv2`  

---

## 1. Executive Summary
This audit reviews the AgroScan AI codebase to prepare for the local download, configuration, and integration of the Hugging Face plant disease classification model `neghani/plantvillage-mobilenetv2` (MobileNetV2, 38 classes across 14 crops).

The existing AgroScan AI system is a production-grade web application featuring:
- **Frontend:** React 18 + Vite, Tailwind CSS, Lucide icons, multilingual i18n (English + Marathi).
- **Backend:** FastAPI, SQLAlchemy, SQLite (`agroscan.db`), Pydantic v2, Pillow, OpenCV (headless).
- **Validation Engine:** Multi-stage computer vision leaf validation gate (`LeafValidator`) rejecting non-leaves, selfies, documents, buildings, soil, blurred/dark images.
- **Provider Architecture:** Multi-provider consensus orchestrator (`consensus_engine.py`) designed for local models and cloud vision APIs (Gemini, OpenRouter, Kindwise/Plant.id, Plantix, PlantNet, Agrio).
- **Knowledge Base:** Comprehensive agronomic, botanical, and treatment guidelines (`DISEASE_KNOWLEDGE_BASE`, `PLANTS_KNOWLEDGE_BASE`).

---

## 2. Codebase Structure & Component Inventory

### 2.1 Frontend (`frontend/src/`)
- **Entry & Routing:** `App.jsx`, `main.jsx`, `index.css`.
- **Pages:**
  - `ScanPage.jsx`: Photo capture via camera or file upload; target crop selection ("Auto-Detect" or specific crop), farm selection, validation messaging, navigation to `AnalysisPage`.
  - `AnalysisPage.jsx`: Multi-stage progress indicator, calls `/api/v1/predictions/analyze` or `/api/predictions/analyze`, handles errors (rejections), saves scan locally, navigates to `ResultPage`.
  - `ResultPage.jsx`: Displays diagnosis for the current scan ID, plant species, disease, confidence score, consensus agreement, severity metrics, organic & chemical recommendations, and embedded AI agronomist chat.
  - `DashboardPage.jsx`: Real-time summary cards, recent scan history, live microclimate weather risk, quick scan CTA, reset data modal.
  - `HistoryPage.jsx`: Saved historical scans, deletion per scan or clear all, filters by user / guest.
  - `AnalyticsPage.jsx`: Outbreak analytics, disease frequency, severity distribution, monthly trends.
  - `WeatherRiskPage.jsx`: Microclimate outbreak prediction based on temperature, humidity, rainfall, and crop disease susceptibility.
  - `AssistantPage.jsx`: Interactive agronomist chat and research advisory.
  - `CropGuidesPage.jsx`: Cultivation and disease management guides.
  - `LoginPage.jsx`, `RegisterPage.jsx`: Farmer and admin authentication with JWT and Firebase support.
  - `LandingPage.jsx`: Product overview, key features, mobile responsiveness.
- **Contexts:**
  - `AuthContext.jsx`: Manages user credentials, JWT tokens, guest fallback.
  - `LanguageContext.jsx`: Dynamic localization between English (`en`) and Marathi (`mr`).
  - `ThemeContext.jsx`: Theme handling.
- **Translations:**
  - `i18n/en.js`: Complete English translations.
  - `i18n/mr.js`: Complete Marathi translations.
  - `i18n/crop_diseases.js`: Standardized bilingual names for crops, diseases, and severities.

### 2.2 Backend (`backend/app/`)
- **FastAPI Core:**
  - `main.py`: Application lifecycle (`lifespan`), initial data seeding (`seed_initial_data`), CORS middleware with credential handling, rate limiting middleware (20 req/60s for scan), max upload size enforcement (10MB), static uploads mount (`/uploads`), dual routing (`/api/v1` and `/api`).
  - `core/config.py`: Environment configuration via Pydantic settings.
  - `core/database.py`: SQLAlchemy database engine and session factory (`agroscan.db`).
  - `core/security.py`: Password hashing (bcrypt) and JWT generation/validation.
- **API Endpoints (`app/api/v1/endpoints/`):**
  - `scan.py`: Leaf scan endpoints:
    - `POST /validate-image`: Validates image quality and leaf presence without executing diagnosis.
    - `POST /analyze`: Validates upload, runs consensus engine, evaluates severity and weather risk, persists to database, returns `PredictionResponse`.
    - `GET /history`: Retrieves scan history with pagination.
    - `DELETE /history`: Clears scan history.
    - `DELETE /{id}`: Deletes a specific scan record.
    - `GET /{id}`: Retrieves a single scan by ID.
    - `GET /providers/health`: Returns health status of integrated vision providers.
  - `health.py`: System health and status endpoint.
  - `weather.py`: Weather retrieval and disease risk computation.
  - `recommendations.py`: Disease treatment and preventive protocols.
  - `analytics.py`: Outbreak trends and statistics.
  - `auth.py`: User registration, login, profile updates, Firebase token exchange.
  - `chat.py`: AI Agronomist conversation and RAG advisory.
  - `farm.py`: Farmer field and plot management.
  - `crop_guides.py`: Agronomic guides.
- **Services (`app/services/`):**
  - `leaf_validator.py`: `LeafValidator` CV gate evaluating sharpness (Laplacian variance), brightness, glare, skin/selfie detection (Haar cascade + YCbCr/HSV), document/screen detection, building/grid detection, bare soil detection, floral-only detection, and spectral excess green (ExG) / NDI.
  - `consensus_engine.py`: Orchestrates multi-provider predictions, handles provider fallbacks, canonical disease mapping, and agreement levels.
  - `providers/local_model_provider.py`: `AgroScanLocalModelProvider` — previously attempted TensorFlow H5 and fell back to species classifier.
  - `severity_analyzer.py`: Computes lesion area and percentage on leaf surface.
  - `weather_service.py`: Computes disease outbreak risk based on ambient temperature, humidity, rainfall.
  - `disease_knowledge_base.py`: Centralized pathology dictionary and disease details.

---

## 3. Hugging Face Model Verification Audit

| Metric | Verification Result |
| :--- | :--- |
| **Repository ID** | `neghani/plantvillage-mobilenetv2` |
| **Official URL** | https://huggingface.co/neghani/plantvillage-mobilenetv2 |
| **Architecture** | MobileNetV2 (`MobileNetV2ForImageClassification`) |
| **Task** | `image-classification` |
| **Format** | Safetensors (`model.safetensors`) |
| **Weights Size** | 9,264,680 bytes (~9.26 MB) |
| **License** | Apache 2.0 |
| **Selected Tag** | `v1.1` (ref: `refs/tags/v1.1`, target commit: `8bacd1d165f1cb5d0608e280e3caeb0da4e49424`) |
| **Immutable Commit SHA** | `77e6d262dca53b818f7ad1d67088700754515639` |
| **Labels Count** | 38 classes across 14 crops |
| **Files Present** | `config.json`, `model.safetensors`, `preprocessor_config.json`, `README.md`, `calibration.json`, `threshold.json` |
| **Temperature Calibration** | T = 0.884518813 (from `calibration.json`) |
| **Decision Threshold** | 0.50 (selected threshold from `threshold.json`) |

---

## 4. Hardware and Environment Audit
- **OS:** Windows 11 64-bit
- **Python Version:** 3.14.6 in `.venv`
- **CPU:** Intel Core i5
- **RAM:** 8 GB
- **CUDA / GPU Status:** `nvidia-smi` is not installed in system PATH; NVIDIA GPU Computing Toolkit is not present. PyTorch CPU inference mode (`device = "cpu"`) is selected and fully compatible.
- **Dependencies:**
  - Installed: `fastapi==0.141.1`, `numpy==2.5.2`, `pillow==12.3.0`, `opencv-python-headless==5.0.0.93`, `pydantic==2.13.4`, `sqlalchemy==2.0.52`.
  - Required for model: `torch>=2.15.0`, `transformers>=5.0.0`, `huggingface_hub>=2.4.0`, `safetensors>=0.8.0`.

---

## 5. Identified Integration Points & Preservation Constraints
1. **Preserve Database & Schema:** Do not drop SQLite tables (`users`, `farms`, `predictions`, `recommendations`, `diseases`).
2. **Preserve Existing Scan Route:** Keep `/api/v1/predictions/analyze` and `/api/predictions/analyze` contracts intact while enhancing them with the local MobileNetV2 model outputs.
3. **Preserve Image Validation:** Run `LeafValidator.validate_leaf_image` *before* model inference.
4. **Preserve Frontend Workflow:** ScanPage -> AnalysisPage -> ResultPage flow must remain seamless and display real model metadata.
5. **Add Dedicated Model Endpoints:** Provide `/api/model/health`, `/api/model/info`, and `/api/model/predict` (and mirror under `/api/v1/model/...`) for direct model observability.
