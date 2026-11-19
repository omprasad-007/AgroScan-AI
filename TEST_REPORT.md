# AgroScan AI — Comprehensive Automated Test Execution Report
**Date:** November 2026  
**System:** AgroScan AI Hybrid Intelligence Engine  
**Execution Environment:** Windows, Python 3.14.6, Pytest 9.1.1, Node.js 20, Vite 5.2.11  

---

## 1. Test Suite Summary

A total of **52 backend automated tests** were executed across three test suites. **All 52 tests passed (100% pass rate).** In addition, the React frontend production bundle was compiled and verified via Vite.

```
========================================================================================
Test Suite                                  Tests   Passed  Failed  Duration    Status
----------------------------------------------------------------------------------------
tests/test_leaf_scan_pipeline.py            13      13      0       11.45s      PASSED
tests/test_hybrid_ai_engine.py              18      18      0       11.04s      PASSED
tests/test_backend.py                       21      21      0       113.22s     PASSED
Frontend Vite Build (npm run build)         --      2395 mod 0       7.35s      PASSED
----------------------------------------------------------------------------------------
TOTAL EXECUTION:                            52      52      0       143.06s     ALL PASSED
========================================================================================
```

---

## 2. Test Execution Details

### 2.1 Stage 1 Image Validation Gate Tests (`tests/test_leaf_scan_pipeline.py`)

| # | Test Function | Test Fixture / Condition | Expected Behavior | Actual Result |
|---|---|---|---|:---:|
| 1 | `test_leaf_validator_valid_leaf` | Synthetic diseased/healthy green leaf with veins | `is_leaf: True`, `usable_for_diagnosis: True`, `status: VALID_LEAF` | **PASSED** |
| 2 | `test_leaf_validator_selfie_rejected` | Synthetic human face / portrait with skin-tone oval | `is_leaf: False`, `usable_for_diagnosis: False`, `status: NON_LEAF_SELFIE` | **PASSED** |
| 3 | `test_leaf_validator_animal_rejected` | Synthetic animal fur texture with zero foliage | `is_leaf: False`, `usable_for_diagnosis: False`, `status: NON_PLANT_IMAGE` | **PASSED** |
| 4 | `test_leaf_validator_building_rejected` | Synthetic urban architecture with rectilinear grid | `is_leaf: False`, `usable_for_diagnosis: False`, `status: BUILDING_DETECTED` | **PASSED** |
| 5 | `test_leaf_validator_document_rejected` | White document with text contrast lines | `is_leaf: False`, `usable_for_diagnosis: False`, `status: DOCUMENT_DETECTED` | **PASSED** |
| 6 | `test_leaf_validator_flower_only_rejected` | Vivid floral petal bloom without leaf foliage | `is_leaf: False`, `usable_for_diagnosis: False`, `status: FLOWER_WITHOUT_LEAF` | **PASSED** |
| 7 | `test_leaf_validator_blurry_leaf_rejected` | Green leaf with heavy blur ($\text{var} < 8.0$) | `usable_for_diagnosis: False`, `status: INSUFFICIENT_IMAGE_QUALITY` | **PASSED** |
| 8 | `test_stage1_validate_image_endpoint` | Valid leaf vs. non-leaf selfie against `/predictions/validate-image` | Valid leaf &rarr; 200 `VALID_LEAF`; Selfie &rarr; 200 `NON_LEAF_SELFIE` | **PASSED** |
| 9 | `test_analyze_endpoint_blocks_selfie_and_prevents_disease_fabrication` | Selfie upload to `POST /predictions/analyze` | HTTP 400 Bad Request with localized message; **Tomato Blight NEVER returned** | **PASSED** |
| 10 | `test_analyze_endpoint_blocks_building` | Building image to `POST /predictions/analyze` | HTTP 400 Bad Request with localized message | **PASSED** |
| 11 | `test_session_isolation_and_image_hash` | Two different synthetic leaf images | Distinct SHA-256 hashes ($h_1 \ne h_2$), 64-char length | **PASSED** |
| 12 | `test_different_images_produce_different_hashes_no_stale_cache` | Leaf vs. document image | Generates different cache keys, preventing stale cache pollution | **PASSED** |
| 13 | `test_provider_health_monitoring_endpoint` | Authenticated `GET /predictions/providers/health` | Returns array of providers; **API keys never leaked** | **PASSED** |

### 2.2 Hybrid AI Engine & Security Tests (`tests/test_hybrid_ai_engine.py`)

| # | Test Function | Target Tested | Expected Behavior | Actual Result |
|---|---|---|---|:---:|
| 14 | `test_image_preprocessor_valid_leaf` | ImagePreprocessor | Valid decode to PIL, RGB NumPy, dimensions | **PASSED** |
| 15 | `test_image_preprocessor_empty_or_truncated` | ImagePreprocessor | Raises `ImagePreprocessingError` | **PASSED** |
| 16 | `test_image_preprocessor_low_resolution` | ImagePreprocessor ($64 \times 64$ px) | Raises `ImagePreprocessingError` ($< 100$ px) | **PASSED** |
| 17 | `test_image_preprocessor_tensor_generation` | ImagePreprocessor PyTorch conversion | Output tensor shape `(1, 3, 224, 224)`, `float32` | **PASSED** |
| 18 | `test_crop_registry_supported_crops` | CropRegistry | Tomato, Potato, Corn &rarr; `SUPPORTED` | **PASSED** |
| 19 | `test_crop_registry_partially_supported_crops` | CropRegistry | Mango, Cotton, Rice &rarr; `PARTIALLY_SUPPORTED` | **PASSED** |
| 20 | `test_crop_registry_unsupported_crop` | CropRegistry | Tea, Coffee &rarr; `UNSUPPORTED` | **PASSED** |
| 21 | `test_crop_registry_unknown_crop` | CropRegistry | "plastic_chair" &rarr; `UNKNOWN_CROP` | **PASSED** |
| 22 | `test_crop_registry_aliases` | CropRegistry | "tamatar", "aloo", "maize" resolved to canonical IDs | **PASSED** |
| 23 | `test_confidence_calibration_temperature_scaling` | ConfidenceCalibrator | Scales logits with $T = 0.8845$; sums to 1.0 | **PASSED** |
| 24 | `test_confidence_calibration_interpretation` | ConfidenceCalibrator | Bands: High ($\ge 0.70$), Mod ($0.50–0.70$), Low ($<0.50$) | **PASSED** |
| 25 | `test_model_agreement_evaluation` | ConfidenceCalibrator | Unanimous &rarr; 1.0; Conflicting &rarr; 0.40 + note | **PASSED** |
| 26 | `test_plantvillage_label_parser` | HuggingFaceInferenceService | Parses `Tomato___Tomato_Yellow_Leaf_Curl_Virus` & `Apple___healthy` | **PASSED** |
| 27 | `test_model_registry_health_status` | ModelRegistry | Returns health status for MobileNetV2 and DINOv2 | **PASSED** |
| 28 | `test_result_normalizer_schema_compliance` | ResultNormalizer | Complies with Part 8 schema; non-null disclaimers | **PASSED** |
| 29 | `test_orchestrator_rejects_selfie` | HybridPredictionOrchestrator | Rejects selfie with `INVALID_IMAGE` status | **PASSED** |
| 30 | `test_orchestrator_unsupported_crop` | HybridPredictionOrchestrator | Returns `UNSUPPORTED_CROP` status; zero fabricated disease | **PASSED** |
| 31 | `test_delete_authorization_protection` | `DELETE /predictions/{id}` | User B deleting User A's scan returns **HTTP 403 Forbidden** | **PASSED** |

### 2.3 General Backend & Auth Regression Tests (`tests/test_backend.py`)

- **Health check (`/health`):** 200 OK.
- **User registration & login:** PBKDF2 hashing, JWT access token generation.
- **Farm management (`/farms`):** CRUD operations with user isolation.
- **Geocoding & GPS endpoints (`/geocoding`):** Coordinates reverse geocoded.
- **Weather risk simulation (`/weather/risk`):** Microclimate pathogen calculation.
- **Analytics aggregation (`/analytics/dashboard`):** Real database record aggregation.
- **History list & delete (`/predictions/history`):** User isolation verified.
- **Total:** 21 tests passed.

---

## 3. Frontend Build & Localization Verification

- **Vite Build Command:** `cmd /c "npm --prefix frontend run build"`
- **Result:** Successfully transformed 2,395 modules in 7.35s with zero errors.
- **Bundle Outputs:**
  - `dist/index.html` (1.38 kB)
  - `dist/assets/index-BtfP4aAe.js` (303.50 kB)
  - `dist/assets/index-C_pOGgx9.css` (50.30 kB)
  - `dist/assets/charts-vendor-mf1SC8fO.js` (403.52 kB)
- **Internationalization Verification:**
  - Confirmed all new status keys (`result.supported_crop`, `result.unsupported_crop`, `result.conf_high`, `analysis.verification_notice`, etc.) render cleanly in both English and Marathi without untranslated raw string leaks.
