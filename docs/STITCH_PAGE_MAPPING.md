# AgroScan AI — 17 Stitch Page Mapping Specification (Phase 17)

This document maps all **17 Stitch UI Design System** screens directly to React components, routes, backend APIs, database dependencies, current status, and functionality.

---

## 🗺️ 17 Stitch Screen Mapping Matrix

| # | Stitch Screen Title | Screen ID | React Component | Application Route | Backend API Required | Database Entity Required | Current Status | Functionality Details |
|---|---------------------|-----------|-----------------|-------------------|----------------------|--------------------------|----------------|-----------------------|
| 1 | **AgroScan AI - Welcome** | `13fb6ea49a4a4dd892294344a15068a3` | `LandingPage.jsx` | `/` | N/A | N/A | Operational | Landing page hero, system features, quick scan CTA |
| 2 | **Farmer Registration** | `7f66bf3546574aed83069e369595e36a` | `RegisterPage.jsx` | `/register` | `POST /api/v1/auth/register` | `User` | Operational | Account registration, preferred language, location |
| 3 | **Farmer Dashboard** | `6b61dbc32e744634b103cea62b333d69` | `DashboardPage.jsx` | `/dashboard` | `GET /api/v1/analytics/dashboard` | `Prediction`, `Scan` | Operational | Scan summary, healthy/diseased counts, quick scan CTA |
| 4 | **Scan a Leaf (v1)** | `8e7ead7d835f4dfe912d40a45ecf8d39` | `ScanPage.jsx` | `/scan` | `POST /api/v1/predictions/analyze` | `Scan` | Operational | Camera-first leaf scanner with framing overlay & upload |
| 5 | **Scan a Leaf (v2)** | `4b0113bc82d6465c97e957c9d4f5bab4` | `ScanPage.jsx` | `/scan` | `POST /api/v1/predictions/analyze` | `Scan` | Operational | Secondary device image upload & file drag/drop |
| 6 | **Analyzing... (v1)** | `5847b6920c3e435495cca0ecd0a9a315` | `AnalysisPage.jsx` | `/analysis` | `POST /api/v1/predictions/analyze` | `Scan`, `Prediction` | Operational | 8-step visual scanning progress sequence |
| 7 | **Analyzing... (v2)** | `b4f161ef0c104a88a0028f5d051fbf81` | `AnalysisPage.jsx` | `/analysis` | `POST /api/v1/predictions/analyze` | `Scan`, `Prediction` | Operational | Preprocessing progress & OpenCV matrix feedback |
| 8 | **Diagnosis Result** | `948773e83ae54348acdccd13faefad47` | `ResultPage.jsx` | `/results/:scanId` | `GET /api/v1/predictions/{id}` | `Prediction`, `Recommendation` | Operational | Full report: Plant ID, Disease, Severity, Remedies |
| 9 | **Scan History** | `9af7142a951644edb94687095fcbcac1` | `HistoryPage.jsx` | `/history` | `GET /api/v1/predictions/history` | `Prediction`, `User` | Operational | User scan archive with thumbnails & report links |
| 10 | **Farm Analytics** | `9ae97ab56a2c41bca3958b748ec6bcaa` | `AnalyticsPage.jsx` | `/analytics` | `GET /api/v1/analytics/dashboard` | `Prediction` | Operational | Outbreak distributions, severity charts, monthly trends |
| 11 | **Farm Analytics (Farmer View)** | `86e7d4b2189c491ea6f989f37d890fd5` | `AnalyticsPage.jsx` | `/analytics` | `GET /api/v1/analytics/dashboard` | `Prediction`, `Farm` | Operational | Crop health percentage & field disease risk |
| 12 | **Weather & Disease Risk** | `ab66ec76a5924cdfb885fbb166853b2b` | `WeatherRiskPage.jsx` | `/weather` | `GET /api/v1/weather/current` | `WeatherObservation` | Operational | Temperature, humidity, rainfall & disease risk matrix |
| 13 | **Weather & Disease Risk Details** | `04e8021060884d958d071d4cb64a86bf` | `WeatherRiskPage.jsx` | `/weather` | `POST /api/v1/weather/risk` | `WeatherObservation` | Operational | Preventive weather spraying guidance & forecast |
| 14 | **AI Assistant** | `d683bd75c92b4109b17fc2e39bbae9cc` | `AssistantPage.jsx` | `/assistant` | `POST /api/v1/chat` | `User` | Operational | Gemini AI Agronomist chat interface |
| 15 | **Agriculture AI Assistant** | `9f848e2f7b22403dbf11e09338bdf52c` | `AssistantPage.jsx` | `/assistant` | `POST /api/v1/chat` | `User` | Operational | Diagnostic explanation & multilingual treatment advice |
| 16 | **My Farm Profile** | `7eae9f419dda415b9733289a14a758b6` | `ProfilePage.jsx` | `/profile` | `GET /api/v1/farms` | `Farm`, `User` | Operational | Farm details, crop list, soil type, location |
| 17 | **Admin Overview** | `fcffaa817b1d426184fb75acf8bb5d0f` | `AdminDashboardPage.jsx` | `/admin` | `GET /api/v1/admin/analytics` | `User`, `Prediction` | Operational | Admin system metrics, user list, ML scan counts |
