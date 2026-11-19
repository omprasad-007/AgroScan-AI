# AgroScan AI — Existing Features Baseline

This document lists every active feature, endpoint, and UI component in AgroScan AI that must be preserved without regressions during the Hugging Face MobileNetV2 model integration.

---

## 1. Authentication & User Management
- **Local Credentials:** Email/password authentication with bcrypt hashing (`User` model in `users` table).
- **Demo Farmer:** Pre-seeded account `farmer@agroscan.ai` with default password `password123`.
- **Admin Account:** Pre-seeded account `admin@agroscan.ai` with role `admin`.
- **Firebase Authentication Exchange:** Endpoint `/api/v1/auth/firebase-login` converts verified Firebase user accounts into system tokens without privilege escalation.
- **Guest Access:** Full guest scanning capability enabled on `/api/v1/predictions/analyze` and `/api/v1/predictions/validate-image` without requiring upfront authentication.
- **Session Tokens:** JWT bearer tokens generated with HS256 algorithm and expiration checks.

---

## 2. Leaf Image Validation Service (`LeafValidator`)
- **Resolution & Integrity:** Enforces minimum 100x100 resolution, max 10MB file size, and PIL RGB stream verification.
- **Blur & Sharpness:** Discrete Laplacian variance test with thresholding (variance >= 8.0, blur score calculation).
- **Luminance & Glare:** Dynamic grayscale mean brightness check (15.0 - 245.0) and glare pixel fraction (< 0.35).
- **Selfie / Face Detection:** Dual-layer rejection using OpenCV Haar Cascade Classifier (`haarcascade_frontalface_default.xml`) and YCbCr/HSV skin-tone masking.
- **Document / Paper Detection:** High-whiteness ratio (> 0.45) and lack of botanical spectral signals.
- **Architecture / Building Grid:** Horizontal and vertical rectilinear gradient energy metric (> 0.14).
- **Soil / Ground Detection:** Brown-earth color space thresholding (high red, low excess green).
- **Floral / Fruit Rejection:** Detects flower blooms and non-foliage elements when green leaf blade is absent.
- **Botanical Foliage & Spectral Index:** Evaluates Excess Green (`ExG = 2G - R - B`), Normalized Difference Index (`NDI = (G - R) / (G + R)`), and organic venation texture standard deviation.

---

## 3. Disease Detection & Hybrid Provider Orchestration
- **Consensus Engine:** `consensus_engine.py` orchestrates multi-provider diagnoses with fallback mechanisms.
- **Registered Providers:**
  - `AgroScanLocalModelProvider` (Local Vision Engine)
  - `GeminiVisionProvider` (Google Gemini 1.5 Pro / Flash)
  - `OpenRouterVisionProvider` (OpenRouter API)
  - `KindwisePlantIdProvider` (Plant.id / Kindwise API)
  - `PlantNetProvider`, `PlantixProvider`, `AgrioProvider`, `TajiriVisionProvider`
- **Canonical Disease Mapping:** Maps heterogeneous provider labels to standardized internal codes (`CANONICAL_DISEASE_MAP`).
- **Severity Analysis:** `SeverityAnalyzer` calculates lesion pixel coverage, percentage, and classifies into `Healthy`, `Low`, `Moderate`, `Severe`, or `Critical`.
- **Weather Outbreak Correlation:** `WeatherRiskService` computes environmental disease risk scores using temperature, relative humidity, and rainfall against crop/pathogen thresholds.

---

## 4. Frontend User Experience & Pages
- **ScanPage (`/scan`):**
  - Live webcam / mobile camera feed via `CameraScanner`.
  - Drag-and-drop file upload with format and size checking.
  - Crop target selector (Auto-Detect or 18+ specific crops).
  - Target farm selector with pre-populated GPS coordinates.
  - Error alert banners for invalid uploads.
- **AnalysisPage (`/analysis`):**
  - Animated laser scan effect on the uploaded image.
  - Multi-stage diagnostic progress bar (4 visual stages).
  - Rejection handler displaying bilingual guidance with retry and change photo actions.
  - Seamless navigation to `/results/:scanId`.
- **ResultPage (`/results/:scanId`):**
  - Detailed diagnostic report matching only the active `scanId`.
  - Botanical plant species and scientific name.
  - Disease name and severity badge (`Low`, `Moderate`, `Severe`).
  - Weather risk level badge.
  - Diagnostic metrics grid: Confidence score, consensus score, model agreement ratio, affected leaf area in cm².
  - Leaf validation gate verification badge.
  - Uncertainty warnings when predictions have low confidence.
  - Organic treatment, chemical management, and preventive guidance.
  - Embedded AI Agronomist chat (`AIAssistantPanel`) populated with scan context.
- **DashboardPage (`/dashboard`):**
  - Metric counters: Total scans, healthy scans, diseased scans, microclimate risk.
  - Recent scan cards with direct result links.
  - Farm microclimate weather card.
  - Quick Scan CTA button.
  - Reset scan records modal.
- **HistoryPage (`/history`):**
  - Chronological list of user diagnostic records.
  - Individual scan deletion (`DELETE /api/v1/predictions/:id`).
  - Clear all history (`DELETE /api/v1/predictions/history`).
- **AnalyticsPage (`/analytics`):**
  - Disease frequency bar charts.
  - Severity level distributions.
  - Monthly scan volume trends.
- **WeatherRiskPage (`/weather`):**
  - Outbreak risk simulation based on ambient temperature, humidity, rainfall.
  - Contributing factor breakdowns.
- **Multilingual Support (i18n):**
  - Full interface toggle between English (`en`) and Marathi (`mr`).
  - Dynamic translation for crops, diseases, severities, and error alerts.

---

## 5. Test Suite Baseline
- **Existing Pytest Suite:** 34 tests in `tests/test_backend.py` and `tests/test_leaf_scan_pipeline.py`.
- **Status:** 34 passed, 0 failed.
- **Coverage:** Auth, demo login, health check, weather risk, dashboard analytics, synthetic leaf validation, blurry image rejection, selfie rejection, multi-provider consensus, rate limiting.
