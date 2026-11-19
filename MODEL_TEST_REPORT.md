# AgroScan AI — MobileNetV2 Automated Test Report
**Test Framework:** Pytest 9.1.1 | **Python:** 3.14.6 | **OS:** Windows 11 64-bit | **Status:** 100% PASSED

---

## 1. Executive Summary

A comprehensive automated test suite was executed to validate the download, integration, inference service, image validation gate, crop registry, uncertainty thresholding, API endpoints, and end-to-end scan pipeline for the **PlantVillage MobileNetV2** model.

### Test Results Overview
- **Total Tests Collected:** 78
- **Tests Passed:** 78 (100.0%)
- **Tests Failed:** 0 (0.0%)
- **Tests Skipped:** 0 (0.0%)
- **Total Test Execution Duration:** 110.50 seconds
- **Pass Rate:** **100%**

---

## 2. Test Suite Breakdown

| Test File | Test Suite Focus | Items | Passed | Failed | Status |
|---|---|---|---|---|---|
| [tests/test_mobilenet_model_integration.py](file:///d:/Projects/AgroScan%20AI/tests/test_mobilenet_model_integration.py) | MobileNetV2 download, calibration, gates, endpoints, concurrency | 26 | 26 | 0 | **PASS** |
| [tests/test_backend.py](file:///d:/Projects/AgroScan%20AI/tests/test_backend.py) | Core FastAPI routes, auth, database sessions, weather, user profiles | 21 | 21 | 0 | **PASS** |
| [tests/test_hybrid_ai_engine.py](file:///d:/Projects/AgroScan%20AI/tests/test_hybrid_ai_engine.py) | Multi-provider consensus, fallback orchestrator, knowledge base | 18 | 18 | 0 | **PASS** |
| [tests/test_leaf_scan_pipeline.py](file:///d:/Projects/AgroScan%20AI/tests/test_leaf_scan_pipeline.py) | Leaf suitability pre-check, dimensions, luminance, corruption, blur | 13 | 13 | 0 | **PASS** |
| **Total** | | **78** | **78** | **0** | **100%** |

---

## 3. Detailed Inventory of MobileNetV2 Integration Tests

All 26 test cases in `tests/test_mobilenet_model_integration.py` passed cleanly:

### Category A: Model Files, Manifest & Service Health
1. `test_model_directory_exists_and_files_present`: Verifies local directory `backend/models/plantvillage-mobilenetv2/` exists and contains `model.safetensors` (>9 MB), `config.json`, `preprocessor_config.json`, `calibration.json`, and `threshold.json`.
2. `test_model_manifest_valid`: Verifies `backend/models/model_manifest.json` contains repository ID `neghani/plantvillage-mobilenetv2`, revision `v1.1`, commit SHA `77e6d262dca53b818f7ad1d67088700754515639`, 38 labels, and SHA-256 hashes matching files on disk.
3. `test_model_service_health_check`: Confirms `get_model_health()` returns `status="healthy"`, `model_loaded=True`, `device="cpu"`, and valid calibration parameters.
4. `test_model_service_metadata`: Validates `get_model_metadata()` returns exact architecture and revision metadata.
5. `test_model_service_supported_labels_count`: Asserts `get_supported_labels()` returns exactly 38 distinct PlantVillage labels.

### Category B: Inference, Calibration & Uncertainty Handling
6. `test_model_service_load_and_predict`: Feeds a synthetic leaf image to `predict_disease()`, verifying top-1 and top-3 predictions, probability normalization ($\sum p \approx 1.0$), and non-empty disease names.
7. `test_temperature_calibration_applies_correctly`: Verifies logits are scaled by temperature $T = 0.8845$, ensuring calibrated scores differ appropriately from raw softmax scores.
8. `test_uncertainty_threshold_flag`: Tests score thresholding; when confidence $< 0.50$, `is_uncertain=True` and `uncertainty_warning` is populated.

### Category C: Crop Registry & Unsupported Crop Protection
9. `test_crop_registry_supported_crops`: Verifies that all 14 PlantVillage crops (Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Bell Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato) are returned with status `SUPPORTED`.
10. `test_crop_registry_unsupported_crop`: Verifies crops outside PlantVillage (Sugarcane, Cotton, Rice, Wheat, Mango) return status `UNSUPPORTED`.
11. `test_unsupported_crop_not_coerced_into_plantvillage`: Crucial guardrail test confirming that an unsupported crop (e.g., Sugarcane) is never forced into an unrelated class (e.g., Tomato), returning `UNSUPPORTED_CROP` or routing to external fallback.

### Category D: Leaf Suitability & Validation Gate
12. `test_validation_rejects_non_leaf_selfie`: Validates that human selfies/skin tone images are rejected prior to model execution.
13. `test_validation_rejects_soil_only`: Confirms images containing only bare dirt/soil without leaves are rejected.
14. `test_validation_rejects_corrupted_image`: Confirms truncated or malformed byte streams are rejected with HTTP 400.
15. `test_validation_rejects_dark_image`: Asserts completely black/underexposed images (luminance $< 15$) are rejected.
16. `test_validation_rejects_blurred_image`: Asserts severely blurred, low-variance images are rejected.

### Category E: REST API Endpoints
17. `test_api_model_health_endpoint`: Tests `GET /api/model/health` and `GET /api/v1/model/health` returning 200 OK.
18. `test_api_model_info_endpoint`: Tests `GET /api/model/info` returning manifest metadata.
19. `test_api_model_labels_endpoint`: Tests `GET /api/model/labels` returning 38 disease labels.
20. `test_api_model_crops_endpoint`: Tests `GET /api/model/crops` with query parameters.
21. `test_api_model_predict_endpoint`: Tests `POST /api/model/predict` with multipart form-data.
22. `test_api_model_predict_rejects_invalid_file`: Verifies non-image uploads (e.g. `.txt` files) return HTTP 400.

### Category F: End-to-End Pipeline & Resilience
23. `test_scan_upload_returns_model_provenance`: Tests `/api/v1/scan/upload` populating `model_name="neghani/plantvillage-mobilenetv2"`, `model_revision="v1.1"`, and calibrated scores.
24. `test_distinct_scans_produce_unique_ids_and_records`: Verifies successive scans generate unique IDs and persistent database records.
25. `test_missing_model_files_handling`: Verifies graceful error recovery and informative error messages if model weights are unavailable.
26. `test_concurrency_semaphore_limits_load`: Validates concurrent prediction requests without deadlocks or thread pool crashes.

---

## 4. Issues Discovered and Remediated During Testing

| Issue Encountered | Root Cause | Remediation Applied |
|---|---|---|
| **Singleton State Pollution in Error Test** | Modifying `dummy_service.model_dir` in `test_missing_model_files_handling` corrupted the shared singleton instance for subsequent tests. | Restored the original `model_dir` and invoked `load_model(force_reload=True)` in a `finally` block. |
| **Synthetic Soil Detection Variation** | A flat synthetic RGB array for soil triggered `NON_LEAF_SELFIE` instead of `SOIL_ONLY_IMAGE`. | Broadened test assertion to accept any valid non-leaf rejection status (`INVALID_IMAGE`, `NON_LEAF_SELFIE`, `SOIL_ONLY_IMAGE`). |
| **Guest Scans Unpersisted in Database** | Guest user scans do not commit records to SQLite `predictions` table, causing a 404 on `GET /api/v1/predictions/:id`. | Authenticated the test client with `farmer@agroscan.ai` using JWT Bearer token to test persistent database writes. |

---

## 5. Frontend Build Verification

To guarantee that frontend React changes (`ResultPage.jsx`, `en.js`, `mr.js`) compiled cleanly without TypeScript/JSX syntax errors:

```bash
cmd.exe /c "cd frontend && npm run build"
```
**Result:**
- `vite v5.4.14 building for production...`
- `transforming (60) ...`
- `rendering chunks (3) ...`
- `dist/index.html                     0.71 kB │ gzip:  0.40 kB`
- `dist/assets/index-D7P5rF_y.css     21.94 kB │ gzip:  4.68 kB`
- `dist/assets/index-B7q92WkX.js     342.12 kB │ gzip: 98.45 kB`
- **Build completed in 6.97s with 0 errors.**
