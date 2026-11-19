# AgroScan AI — Mandatory System Audit Report
**Date:** November 2026  
**System:** AgroScan AI – Smart Plant Disease Detection & Crop Health Monitoring System  
**Auditor:** Senior AI/ML & Application Security Architecture Team  

---

## 1. Executive Summary

A comprehensive, end-to-end audit of the AgroScan AI project was performed across both the React + Vite frontend and the Python FastAPI backend, encompassing codebase structure, dependency configurations, database integrity, authentication pathways, computer vision algorithms, and AI/ML inference pipelines.

The audit verified that the application possesses a functional core with 34 passing tests and a successful production frontend build. However, critical architectural shortcomings were discovered in the AI inference layer:
1. **Absence of True Local Neural Network Inference:** The previous local model provider attempted to import TensorFlow (which is unavailable for Python 3.14) and fell back to a pseudo-botanical species classifier that selected diseases via deterministic hash seeds (`hash_seed % len(candidate_keys)`).
2. **Client-Side Fallback Fabrication:** When the backend failed or external APIs timed out, `AnalysisPage.jsx` invoked `clientSideDiagnose` from `mockData.js`, fabricating disease reports and storing them into local storage.
3. **Broken Authorization in Scan Records:** Any caller could delete any scan record via `DELETE /api/v1/predictions/{id}` without verifying scan ownership.
4. **Lack of a Structured Crop Support Registry:** The system lacked an explicit classification for `Supported`, `Partially Supported`, `Unsupported`, and `Unknown` crops, risking forced inaccurate disease diagnoses for unsupported crops.

This audit establishes the baseline facts required to systematically upgrade AgroScan AI to a genuine, locally executable hybrid intelligence platform without regressing existing features.

---

## 2. Inventory of Existing System Components

### 2.1 Backend (`backend/app`)
- **FastAPI Core (`main.py`):** Configures CORS, lifecycle hooks, static file mounting for `/uploads`, auto-creation of SQLite tables via `Base.metadata.create_all`, and initial database seeding (`seed_initial_data`).
- **Configuration (`core/config.py`):** Pydantic `BaseSettings` reading from `.env` and `backend/.env`. Defines database URLs, security keys, CORS origins, provider API keys, and validation thresholds.
- **Database Engine (`core/database.py`):** SQLAlchemy SQLite engine with `check_same_thread=False` and session factory (`SessionLocal`).
- **Security (`core/security.py`):** Salted PBKDF2-SHA256 password hashing (100,000 iterations) with HMAC legacy fallback, and PyJWT token generation/decoding.
- **Authentication Dependencies (`api/deps.py`):** Provides `get_current_user` (enforces Bearer token) and `get_optional_current_user` (allows guest users while authenticating registered farmers).
- **API Router (`api/v1/router.py`):** Exposes 12 domain routers: `/auth`, `/farms`, `/geocoding`, `/plants`, `/predictions` (scans), `/weather`, `/recommendations`, `/chat`, `/assistant`, `/analytics`, `/admin`, `/crop-guides`.
- **Knowledge Bases (`knowledge/`):**
  - `plants_data.py`: Extensive agronomic parameters for 10+ crops (Mango, Sugarcane, Cotton, Rice, Wheat, Soybean, Tomato, Potato, Chilli, Onion).
  - `diseases_data.py`: Detailed etiology, symptoms, organic, and chemical management protocols.
  - `general_agri_data.py`: Soil, irrigation, and season guidelines.

### 2.2 Machine Learning & Computer Vision Services
- **Image Validation Gate (`services/leaf_validator.py`):**
  - Pure NumPy/PIL implementation resilient to headless Linux/Windows environments without OpenCV binaries.
  - Computes discrete Laplacian variance (sharpness, threshold $\ge 8.0$).
  - Evaluates luminance ($[15, 245]$) and glare ratio ($< 0.35$).
  - Rejects human selfies (skin YCbCr/HSV masks and Haar cascades), documents/screenshots (white background $> 45\%$), building grids (rectilinear gradient metric $> 0.14$), bare soil, flower-only photos, and sky landscapes.
  - Calculates Excess Green Index ($\text{ExG} = 2G - R - B \ge 12.0$) and Normalized Difference Vegetation Index ($\text{NDI} \ge 0.04$).
  - Validated by 13 automated tests in `tests/test_leaf_scan_pipeline.py`.
- **Consensus Engine (`services/consensus_engine.py`):**
  - Queries active providers (`KindwisePlantIdProvider`, `PlantNetProvider`, `PlantixProvider`, `AgrioProvider`, `GeminiVisionProvider`, `OpenRouterVisionProvider`, `AgroScanLocalModelProvider`).
  - Implements canonical disease mapping and agreement scoring.
- **Severity Analyzer (`services/severity_analyzer.py`):**
  - Segments necrotic leaf lesions using RGB color decomposition and computes percentage area affected ($0\% - 100\%$).
- **Weather Risk Engine (`services/weather_service.py`):**
  - Multi-factor microclimate risk algorithm correlating temperature, humidity, rainfall, and crop-specific pathogen profiles.

### 2.3 Frontend (`frontend/src`)
- **Technology Stack:** React 18.3.1, Vite 5.2.11, Tailwind CSS 3.4.3, React Router 6.23.1, Recharts 2.12.7, Lucide React icons.
- **Pages:**
  - `ScanPage.jsx`: Live camera capture (`CameraScanner`), file upload, crop selector, and target farm selector.
  - `AnalysisPage.jsx`: Progress animation, `AbortController` cancellation, and scan transaction dispatch.
  - `ResultPage.jsx`: Diagnostic report card with lesion severity, weather risk, model agreement, and treatment guidance.
  - `WeatherRiskPage.jsx`: Interactive microclimate weather risk simulator.
  - `HistoryPage.jsx`: Filterable scan history reading both backend and local storage.
  - `AnalyticsPage.jsx`: Real-time charts for disease distribution, severity levels, and monthly trends.
  - `LoginPage.jsx` / `RegisterPage.jsx`: Authentication views supporting standard and Firebase login.
  - `LandingPage.jsx`: Overview and feature showcase.
- **Internationalization (`i18n/`):**
  - Dual language support (English and Marathi `mr`).
  - Domain-specific translations for crops, diseases, severity levels, and rejection messages.

---

## 3. Database Audit & Data Inventory

The existing SQLite database (`agroscan.db`) was inspected directly:
- File size: 319,488 bytes.
- Tables present: `users`, `diseases`, `weather`, `farms`, `chat_sessions`, `predictions`, `chat_messages`, `recommendations`.
- Existing row counts:
  - `users`: 4 registered users (including demo farmer and admin).
  - `diseases`: 28 pre-seeded diagnostic profiles.
  - `farms`: 3 registered agricultural plots.
  - `chat_sessions`: 79 recorded agronomist consultation threads.
  - `chat_messages`: 257 persistent messages.
  - `predictions`: 6 persistent scan records.
  - `recommendations`: 6 diagnostic treatment prescriptions.

**Retention Mandate:** The database contains real user history and operational data. All existing tables and rows must be preserved. Any schema enhancements must be strictly additive and applied via safe, idempotent migrations.

---

## 4. Defect and Vulnerability Findings

| # | Severity | Component | Finding | Impact |
|---|----------|-----------|---------|--------|
| 1 | **Critical** | `backend/app/services/providers/local_model_provider.py` | Fallback to `PlantSpeciesClassifier` uses hash seed modulo (`hash_seed % len(...)`) to choose diseases. | Fake predictions generated when TensorFlow model is absent. |
| 2 | **Critical** | `frontend/src/pages/AnalysisPage.jsx` | `clientSideDiagnose` invoked on API failure/timeout/401/503. | Synthetic mock results saved to user history instead of honest error display. |
| 3 | **High** | `backend/app/api/v1/endpoints/scan.py` (`delete_prediction_by_id`) | No user ownership check on `DELETE /predictions/{id}`. | Any caller can delete another user's scan record. |
| 4 | **High** | `backend/app/services/ai/` | Lack of a dedicated Hugging Face local inference engine. | No genuine on-device deep learning execution. |
| 5 | **Medium** | `backend/app/services/consensus_engine.py` | No formal crop registry or honest unsupported crop handling. | Unsupported crops forced into model classes or generic failure. |
| 6 | **Medium** | `backend/app/api/v1/endpoints/scan.py` (`get_prediction_by_id`) | Guest queries allow accessing any scan ID without session validation. | Guest user data isolation weakness. |
| 7 | **Low** | `frontend/src/pages/ScanPage.jsx` | Crop selector dropdown includes "Other / Field Plant" but backend has no structured unsupported-crop outcome. | User receives unexpected error or misdiagnosis on unsupported plants. |

---

## 5. Verification of Candidate Hugging Face Models

Three candidate models were evaluated against the Hugging Face Hub:

1. **`neghani/plantvillage-mobilenetv2`**
   - **Architecture:** MobileNetV2 for Image Classification (`google/mobilenet_v2_1.0_224` backbone).
   - **Format:** `model.safetensors` (~9 MB), PyTorch & Transformers compatible.
   - **Parameters:** ~3.5M parameters.
   - **Classes:** 38 PlantVillage classes covering 14 crops (Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Bell Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato).
   - **Inference Speed:** ~15–30 ms on modern CPU. Memory footprint < 100 MB RAM.
   - **License:** Apache 2.0.
   - **Calibration Data:** Pre-computed temperature scaling parameter ($T = 0.8845$) and ECE report included on repository.
   - **Recommendation:** **Primary lightweight local model** for immediate, low-latency CPU inference.

2. **`rodynaemad/plant-disease-dinov2-small`**
   - **Architecture:** DINOv2 Small (`facebook/dinov2-small` backbone).
   - **Format:** `model.safetensors` (~85 MB) and ONNX weights.
   - **Parameters:** ~22M parameters.
   - **Classes:** 38 PlantVillage classes.
   - **Inference Speed:** ~90–160 ms on CPU.
   - **License:** CC-BY-SA 4.0.
   - **Recommendation:** **Secondary high-accuracy vision transformer model** for ensemble verification.

3. **`Khawajaa/plant-disease-detector`**
   - **Format:** PyTorch legacy pickle weights (`best_model.pth`, no `config.json` or `safetensors`).
   - **Recommendation:** Not recommended due to pickle security risk and lack of Hugging Face Transformers pipeline metadata.

---

## 6. Audit Conclusion & Next Steps

The existing system provides an excellent foundation with hardened leaf image validation, rich agronomic knowledge bases, and a responsive frontend. Upgrading the application requires:
1. Installing `torch`, `torchvision`, and `transformers` in `.venv`.
2. Implementing a modular Hugging Face local inference engine (`neghani/plantvillage-mobilenetv2` + `rodynaemad/plant-disease-dinov2-small`).
3. Constructing an extensible `CropRegistry` with explicit support statuses (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `UNKNOWN_CROP`).
4. Implementing the 10-step `HybridPredictionOrchestrator` with calibrated confidence rules.
5. Removing all mock/hash-based prediction fallbacks in backend and frontend.
6. Patching authorization vulnerabilities in scan history endpoints.
