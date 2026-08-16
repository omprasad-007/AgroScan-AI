# AgroScan AI — Full System Audit & Vulnerability Classification Report

**Generated**: August 16, 2026  
**Target Application**: AgroScan AI — Smart Plant Disease Detection & Crop Health Monitoring System  
**Live Production URL**: `https://agro-scan-ai-nine.vercel.app/`  
**Repository**: `https://github.com/omprasad-007/AgroScan-AI`  

---

## Executive Summary & System Overview

AgroScan AI is an end-to-end AI-powered Smart Agriculture platform designed for plant disease detection, severity assessment, crop knowledge retrieval, weather outbreak risk forecasting, and AI agronomist consultation. 

This audit evaluates the codebase across 18 mandated domains following OWASP Top 10:2025 security standards, production reliability, fault tolerance, and software supply chain integrity.

---

## 1. System Architecture

```
[ Browser / Mobile Client ] 
        │
        ├── (HTTPS / JWT Bearer)
        ▼
[ Vercel Static CDN (Vite SPA) ] ── (apiClient.js + Interceptors)
        │
        ▼
[ Render / FastAPI Backend Engine ] ── (Python 3.14 + Uvicorn)
        │
        ├── (SQLAlchemy ORM) ──► [ SQLite / PostgreSQL Database ]
        ├── (Plant.id API) ─────► [ External Species & Pathogen API ]
        ├── (Perenual API) ────► [ Botanical Care & Cultivation API ]
        ├── (OpenWeatherMap) ──► [ Real-Time Microclimate Risk Engine ]
        └── (Google Gemini) ───► [ Context-Aware AI Agronomist ]
```

---

## 2. Component Audits & Vulnerability Classifications

### 1. Architecture
- **Status**: Modular architecture separating React SPA frontend and FastAPI backend.
- **Finding**: Needs clear production environment separation flags (`DEMO_MODE=false` in production, controlled error fallback without fake data).
- **Classification**: **MEDIUM**

### 2. Frontend Status
- **Status**: Vite 5 + React 18 SPA with 17 mapped routes, Tailwind CSS styling, Light/Dark mode, English/Marathi i18n, and MobileNav.
- **Finding**: API calls scattered between `api.js` interceptor and component calls; requires unified `apiClient.js` with structured timeouts, retry policies, and error handling.
- **Classification**: **HIGH**

### 3. Backend Status
- **Status**: FastAPI application mounted at `/api/v1` and `/api` with security middleware, Pydantic schemas, and SQLAlchemy ORM models.
- **Finding**: External API services (`plant_disease_service`, `plant_knowledge_service`, `gemini_service`, `weather_service`) need unified timeout, rate-limiting, circuit breaker, and error-masking guards.
- **Classification**: **HIGH**

### 4. Database Status
- **Status**: SQLite (`agroscan.db`) default with SQLAlchemy 2.0 models (`User`, `ScanPrediction`, `Recommendation`, `DiseaseInfo`, `Farm`, `ChatMessage`, `ChatSession`).
- **Finding**: Needs strict user data isolation (IDOR protection) on all endpoints and database migration readiness for PostgreSQL.
- **Classification**: **HIGH**

### 5. Authentication Status
- **Status**: Dual authentication via Firebase Auth (`agroscan-ai-07`) and PBKDF2-SHA256 FastAPI local auth.
- **Finding**: Firebase token verification on backend needs strict server-side validation; session expiry handled gracefully without crashes.
- **Classification**: **HIGH**

### 6. API Integration Status
- **Status**: Integrated with Plant.id, Perenual, OpenWeatherMap, and Google Gemini.
- **Finding**: Optional API failures must gracefully degrade (e.g., if Weather API fails, return disease result with `"Weather information temporarily unavailable"` without failing the whole request).
- **Classification**: **CRITICAL**

### 7. Camera System Status
- **Status**: HTML5 `navigator.mediaDevices.getUserMedia` scanner with rear/front camera switching, snapshot capture, retake, and stopMediaTracks cleanup on unmount.
- **Finding**: Needs safe browser fallbacks for restricted mobile webviews and seamless device upload fallback.
- **Classification**: **MEDIUM**

### 8. AI/ML Status
- **Status**: Custom MobileNetV2 pipeline in `ml/` (preprocessing, training, evaluation, inference predictor) + OpenCV HSV preliminary severity assessment.
- **Finding**: Clear distinction required between API confidence, ML model confidence, preliminary severity, and weather risk. No fake percentages.
- **Classification**: **MEDIUM**

### 9. Security Issues (OWASP Top 10:2025 Audit)
- **A01 Broken Access Control**: Ensure all user history, predictions, and farm resources strictly filter by `user_id == current_user.id` on server-side.
- **A02 Security Misconfiguration**: Disable wildcard CORS (`allow_origins=["*"]`) in production; enforce strict origins (`https://agro-scan-ai-nine.vercel.app`).
- **A03 Software Supply Chain**: Audit `npm` and `pip` dependencies; generate `.env.example` templates; keep `.env` ignored.
- **A04 Cryptographic Failures**: Enforce PBKDF2-SHA256 salted password hashing; rotate exposed key configurations.
- **A05 Injection**: Enforce SQLAlchemy ORM parameterized queries; sanitize inputs against XSS and prompt injection.
- **Classification**: **CRITICAL**

### 10. Performance Issues
- **Status**: Bundle size optimized via Vite build (`dist/` ~959KB minified JS, ~38KB CSS).
- **Finding**: Implement image compression/resizing on client-side before upload to reduce payload latency.
- **Classification**: **LOW**

### 11. Stability Issues
- **Status**: Global React ErrorBoundary wraps app layout.
- **Finding**: Add explicit scan state machine (`idle`, `camera_open`, `captured`, `uploading`, `validating`, `identifying`, `detecting`, `severity`, `enriching`, `completed`, `failed`) to prevent state corruption.
- **Classification**: **HIGH**

### 12. Broken Routes
- **Status**: All 17 routes functional.
- **Finding**: `vercel.json` SPA rewrite configured to prevent 404 on refresh.
- **Classification**: **LOW**

### 13. Broken Buttons
- **Status**: All interactive buttons functional.
- **Finding**: Disable scan button during active upload/processing to prevent duplicate request submissions.
- **Classification**: **MEDIUM**

### 14. Missing Functionality
- **Status**: Core scanner, diagnostics, weather risk, AI assistant, profile, and history implemented.
- **Finding**: Add health readiness endpoint (`GET /health/ready`) and user data deletion endpoint (`DELETE /api/v1/history/{id}`).
- **Classification**: **MEDIUM**

### 15. Duplicate Functionality
- **Status**: Clean routing structure without duplicate pages.
- **Classification**: **LOW**

### 16. Deployment Problems
- **Status**: Frontend configured for Vercel, Backend configured for Render via `render.yaml`.
- **Finding**: Ensure `DEMO_MODE=false` in production env without fallback to fake AI predictions.
- **Classification**: **HIGH**

### 17. Dependency Problems
- **Status**: Clean `requirements.txt` and `package.json`.
- **Finding**: Audit npm vulnerabilities (`npm audit`) and create `docs/DEPENDENCY_SECURITY.md`.
- **Classification**: **MEDIUM**

### 18. Environment Variable Problems
- **Status**: `.gitignore` configured to ignore `.env`.
- **Finding**: Provide complete `backend/.env.example` and `frontend/.env.example` with clear placeholders and zero hardcoded secrets.
- **Classification**: **CRITICAL**

---

## 3. Vulnerability & Issue Classification Summary

| ID | Domain | Problem Description | Severity Classification |
| :--- | :--- | :--- | :--- |
| **SEC-01** | Secrets & Config | Exposed/hardcoded API keys in environment or git history | 🔴 **CRITICAL** |
| **SEC-02** | Access Control | Potential IDOR risks on scan predictions / farm endpoints | 🔴 **CRITICAL** |
| **SEC-03** | CORS Policy | Wildcard CORS allowed in development/production config | 🔴 **CRITICAL** |
| **STB-01** | Fault Tolerance | External API failure (Weather/Perenual/Gemini) causing cascade failure | 🟠 **HIGH** |
| **STB-02** | Input Validation | Image upload bomb / corrupt payload handling in OpenCV pipeline | 🟠 **HIGH** |
| **STB-03** | Client Reliability | Unhandled network timeouts in API client | 🟠 **HIGH** |
| **DEV-01** | Environment Separation | Silent fallback to mock data in production mode | 🟠 **HIGH** |
| **PERF-01**| Image Payload | Uncompressed raw camera upload payload latency | 🟡 **MEDIUM** |
| **UI-01**  | UX Double Click | Duplicate request submission on rapid scan button clicks | 🟡 **MEDIUM** |
| **DOC-01** | Documentation | Complete documentation suite required across 8 markdown specs | 🟢 **LOW** |

---

## 4. Remediation Plan

All identified issues will be systematically addressed through server-side authorization enforcement, robust API client wrappers, fault-tolerant service degradation, input sanitization, complete documentation suite creation, and automated verification testing.
