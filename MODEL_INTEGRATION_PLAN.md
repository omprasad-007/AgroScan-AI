# AgroScan AI — Model Integration Plan
## Hugging Face MobileNetV2 Integration

---

## 1. Goal & Scope
Integrate `neghani/plantvillage-mobilenetv2` into AgroScan AI as the primary local plant-disease classifier.
- Architecture: `MobileNetV2` (`MobileNetV2ForImageClassification`)
- Revision: Tag `v1.1` (Immutable Commit SHA: `77e6d262dca53b818f7ad1d67088700754515639`)
- Destination: `backend/models/plantvillage-mobilenetv2/`
- Manifest: `backend/models/model_manifest.json`
- Preserve all existing functionality, database records, endpoints, frontend workflows, and test suites.

---

## 2. Phase-by-Phase Roadmap

### Phase 1: Audit & Baselines (Completed)
- Inspect project structure, backend routes, services, frontend pages, models, and tests.
- Produce `MODEL_INTEGRATION_AUDIT.md`, `EXISTING_FEATURES_BASELINE.md`, and `MODEL_INTEGRATION_PLAN.md`.
- Establish test baseline: 34 tests passing.

### Phase 2: Repository Verification (Completed)
- Verified Hugging Face API:
  - Repository ID: `neghani/plantvillage-mobilenetv2`
  - Tag: `v1.1`
  - Target Commit SHA: `77e6d262dca53b818f7ad1d67088700754515639`
  - Required files: `model.safetensors` (9.26 MB), `config.json`, `preprocessor_config.json`, `README.md`, `calibration.json`, `threshold.json`.
  - License: Apache 2.0.

### Phase 3: Automated Download
- Target directory: `backend/models/plantvillage-mobilenetv2/`.
- Download via Python script using `huggingface_hub.snapshot_download` pinned to revision `77e6d262dca53b818f7ad1d67088700754515639`.
- Download only required model and calibration files.
- Protect git by ensuring `backend/models/plantvillage-mobilenetv2/*.safetensors` is in `.gitignore`.

### Phase 4: Verification & Manifest Generation
- Verify file sizes and compute SHA-256 checksums for each downloaded file.
- Verify that `config.json` contains 38 labels across 14 crops.
- Generate `backend/models/model_manifest.json`.

### Phase 5: Dependency Management
- Install in `.venv`:
  - `torch`
  - `transformers`
  - `huggingface_hub`
  - `safetensors`
- Update `backend/requirements.txt` with exact version constraints.
- Verify no existing dependencies break.

### Phase 6: Local Inference Service (`plant_disease_model.py`)
- Location: `backend/app/services/plant_disease_model.py` (and export convenient access).
- Implement:
  - `load_model()`: Lazy singleton loading, loads once, eval mode, torch.inference_mode().
  - `predict_disease(image_bytes)`: Preprocesses image using `AutoImageProcessor`, runs inference, applies temperature scaling from `calibration.json` (T = 0.8845), returns top-3 predictions, calibrated softmax scores, and uncertainty evaluation using threshold (0.50).
  - `get_model_metadata()`: Returns architecture, revision, SHA, label count, device, memory.
  - `get_model_health()`: Verifies model loaded and operational.
  - `get_supported_labels()`: Returns all 38 classes with crop and disease breakdown.

### Phase 7: Image Validation Integration
- Connect `LeafValidator` as mandatory pre-inference filter before `predict_disease`.
- Return structured rejection for non-leaf images (selfies, documents, buildings, soil, animals, dark/blurry photos).

### Phase 8: Crop Registry & Label Validation
- Map the 38 PlantVillage classes into a structured registry with status flags:
  - `SUPPORTED`: Crops with native model classes (Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Bell Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato).
  - `PARTIALLY_SUPPORTED`: Crops where external providers or specific species classifier applies.
  - `UNSUPPORTED`: Crops without trained weights (e.g. Sugarcane, Cotton, Rice, Wheat, Mango in this specific model weights file).
- Route unsupported crops honestly with explicit status `UNSUPPORTED_CROP` or delegate to external providers if configured.

### Phase 9: FastAPI Integration
- Update `AgroScanLocalModelProvider` in `backend/app/services/providers/local_model_provider.py` to use `PlantDiseaseModelService`.
- Add dedicated model endpoints in `backend/app/api/v1/endpoints/model.py`:
  - `GET /api/v1/model/health` & `GET /api/model/health`
  - `GET /api/v1/model/info` & `GET /api/model/info`
  - `POST /api/v1/model/predict` & `POST /api/model/predict`
- Ensure non-blocking execution via `asyncio.to_thread` and thread pooling.

### Phase 10: Hybrid Provider Architecture
- Ensure `consensus_engine.py` incorporates MobileNetV2 results alongside any configured cloud vision providers.
- Maintain fallback resilience: if cloud APIs are unconfigured or fail, local MobileNetV2 completes the diagnosis.

### Phase 11 & 12: Frontend & System Preservation
- Ensure `ScanPage`, `AnalysisPage`, `ResultPage`, `DashboardPage`, `HistoryPage` work seamlessly with the new model outputs.
- Display model name (`MobileNetV2 (PlantVillage v1.1)`), calibrated confidence score, and top alternative predictions.
- Verify i18n English and Marathi strings.

### Phase 13: Comprehensive Testing
- Model tests: loading, inference, top-3 outputs, label mapping, error handling.
- Image tests: healthy leaf, diseased leaf, blur, dark, selfie, building, document, soil, unsupported crop.
- Integration tests: scan analyze endpoint, health check, concurrent requests.
- Verify test suite passes completely.

### Phase 14: Documentation
- Create all required reports:
  - `MODEL_SETUP_GUIDE.md`
  - `MODEL_DOWNLOAD_REPORT.md`
  - `MODEL_EVALUATION_REPORT.md`
  - `MODEL_INTEGRATION_REPORT.md`
  - `MODEL_TEST_REPORT.md`
  - `LOCAL_RUN_GUIDE.md`
  - Update `.env.example` with non-secret placeholders.
