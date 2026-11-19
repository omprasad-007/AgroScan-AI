# AgroScan AI — System Risk Register & Mitigation Strategy
**Document:** Security, Architectural, and Operational Risk Assessment  
**System:** AgroScan AI Hybrid Intelligence Engine  

---

## 1. Risk Evaluation Matrix

| Risk ID | Risk Category | Description | Likelihood | Impact | Severity | Mitigation Strategy | Contingency / Rollback |
|:---:|:---|:---|:---:|:---:|:---:|:---|:---|
| **RSK-01** | **AI / Clinical** | **Fabrication of Disease Predictions:** Previous hash-based fallback synthesized diagnoses when external APIs failed. | High | Critical | **CRITICAL** | Eliminate all hash-based pseudo-prediction algorithms. Enforce explicit `UNSUPPORTED_CROP` and `PROVIDER_UNAVAILABLE` statuses. | Never silently fall back to mock diagnoses; return 503 or structured unavailable response. |
| **RSK-02** | **Security** | **Broken Object Level Authorization (BOLA):** `DELETE /predictions/{id}` did not verify that `prediction.user_id == current_user.id`. | Med | High | **HIGH** | Enforce user ownership validation on all delete and detail access endpoints. Return 403 Forbidden on mismatch. | Maintain audit log of deletion attempts; restrict endpoint to authenticated users. |
| **RSK-03** | **Performance** | **Hugging Face Model RAM Exhaustion:** Loading large transformer models concurrently could exceed available host memory on low-resource machines. | Med | High | **HIGH** | Use ultra-lightweight MobileNetV2 (~9 MB safetensors, <100 MB RAM) as default; lazy load on first request; load DINOv2 only if requested. | If RAM is constrained, unload idle weights with `torch.cuda.empty_cache()` and garbage collection. |
| **RSK-04** | **Data Integrity** | **Database Schema Regression:** Altering SQLite schema could delete or corrupt existing user, farm, and chat data. | Low | Critical | **HIGH** | Apply non-destructive, idempotent column additions (`ALTER TABLE ADD COLUMN` wrapped in try/except blocks). | Automatic backup of `agroscan.db` before applying migrations. |
| **RSK-05** | **Reliability** | **External API Rate Limiting / Timeout:** Third-party botanical APIs (Kindwise, Gemini) may experience rate limits (HTTP 429) or network latency. | High | Med | **MEDIUM** | Implement 6-second timeouts with `httpx.AsyncClient`; run local Hugging Face model in parallel so diagnosis succeeds even if cloud fails. | If cloud API fails, present local prediction labeled as "Local Vision Prediction" without false consensus. |
| **RSK-06** | **Security** | **Image Decompression Bomb (DoS):** Attacker uploads an ultra-high resolution image (e.g. 50,000x50,000 px) causing memory exhaustion during PIL decoding. | Low | High | **MEDIUM** | Enforce `MAX_FILE_SIZE_BYTES = 10MB` and check dimensions $\le 4096 \times 4096$ px before full raster processing. | Set `Image.MAX_IMAGE_PIXELS = 25_000_000` in `ImagePreprocessor`. |
| **RSK-07** | **Security** | **API Key Exposure in Client / Logs:** External provider keys (Gemini, Kindwise, Weather) could leak into frontend bundles or git. | Low | Critical | **HIGH** | All external API calls occur strictly from FastAPI backend. Vite frontend never receives secret keys. Strip secrets from log outputs. | `.gitignore` enforces exclusion of `.env` files; `.env.example` contains placeholder tokens only. |
| **RSK-08** | **AI Calibration** | **Overconfident False Positives:** Raw softmax outputs from deep learning models often exhibit overconfidence on out-of-distribution leaf samples. | Med | Med | **MEDIUM** | Implement temperature scaling calibration ($T = 0.8845$) and configurable confidence bands (high $\ge 70\%$, moderate $50-70\%$, uncertain $<50\%$). | Display warning disclaimer and recommend consulting a local Krishi Vigyan Kendra (KVK) agronomist. |
| **RSK-09** | **User Experience** | **Unlocalized Diagnostic Terms in Marathi:** New status labels or error messages displaying in English for Marathi-speaking farmers. | Low | Med | **LOW** | Complete mirror translations in `en.js`, `mr.js`, and `crop_diseases.js` for all new statuses (`UNSUPPORTED_CROP`, `UNCERTAIN`, etc.). | Fallback translation helper returns clean human-readable default if a translation key is missing. |
| **RSK-10** | **Environment** | **Python 3.14 Test Capture Issue:** Pytest standard stdout capture raises `ValueError: I/O operation on closed file` during session cleanup on Windows with Python 3.14. | High | Low | **LOW** | Add `addopts = "-s"` to `pyproject.toml` to disable global capture during test execution. | Tests pass cleanly with `-s` flag across all test runners. |

---

## 2. Emergency Rollback Strategy

In the event of an unrecoverable failure during deployment or execution:
1. **Database Rollback:** The SQLite database `agroscan.db` is backed up to `agroscan.db.bak` prior to applying schema updates. If schema issues occur, restore the backup copy immediately.
2. **Code Rollback:** All modifications are version-controlled via Git. Any problematic commit can be reverted cleanly using `git revert` or `git checkout`.
3. **Model Weights Rollback:** If Hugging Face weight downloads are interrupted by network loss, the engine catches `OSError` / `HTTPError` and reports `MODEL_INITIALIZATION_ERROR` without crashing the application.
4. **Offline Mode:** The engine operates 100% locally with zero internet access once model weights are cached.
