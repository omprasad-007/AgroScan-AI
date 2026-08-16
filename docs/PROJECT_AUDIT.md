# AgroScan AI — Complete Project Audit (Phase 1)

This audit documents the complete state of the **AgroScan AI** codebase, architecture, routes, APIs, services, security, database, and Stitch UI/UX design integration.

---

## 1. Existing Features
- **Frontend Architecture**: React 18 SPA with Vite 5, Tailwind CSS 3, Lucide React icons, Recharts for analytics, and custom context providers (`AuthContext`, `LanguageContext`).
- **Backend Architecture**: FastAPI application with Uvicorn/Gunicorn servers, Pydantic schemas, SQLAlchemy ORM, and SQLite database.
- **Authentication**: Dual Firebase Authentication (`agroscan-ai-07`) and FastAPI JWT token generation with salted PBKDF2-SHA256 password hashing (100,000 iterations).
- **Camera Functionality**: Native HTML5 `navigator.mediaDevices.getUserMedia()` camera scanner component with environment-facing video stream, framing overlay, snapshot capture, and image preview.
- **Image Validation**: FastAPI backend PIL magic-byte checker, extension whitelist, and 10MB payload size limiter.
- **Disease & Severity Engine**: Deterministic fallback disease classifier, OpenCV lesion severity analyzer, and rule-based recommendation knowledge base.
- **Weather Risk Engine**: OpenWeatherMap API proxy with relative humidity and temperature outbreak risk scoring.
- **AI Agronomist Chatbot**: Proxy to Google Gemini and OpenRouter models for contextual crop advice.
- **Multilingual i18n**: Support for English (`en`) and Marathi (`mr`).

---

## 2. Missing Features
- **Dedicated Plant Disease Service (`plant_disease_service.py`)**: `PLANT_ID_API_KEY` calls require explicit service isolation for Plant.id identification & disease classification.
- **Dedicated Plant Knowledge Service (`plant_knowledge_service.py`)**: `PERENUAL_API_KEY` calls require structured species care details (soil, watering, sunlight, growth stages).
- **Expanded ML Data Science Pipeline (`ml/`)**: Missing modular `ml/data/`, `ml/notebooks/`, `ml/preprocessing/`, `ml/training/`, `ml/evaluation/`, and `ml/inference/` repository structure.
- **Pre-Inference Image Quality Check**: Brightness, resolution, and blur (variance of Laplacian) evaluation prior to sending image to disease API.
- **Crop Guides Endpoint (`GET /api/v1/crop-guides/{crop}`)**: Dedicated endpoint for crop-specific cultivation timelines (sowing, nursery, spacing, fertilization, harvest indicators).

---

## 3. Mock vs Real API Integrations
| Subsystem | Status | Details |
|---|---|---|
| **Plant ID & Disease API** | Configured / Proxy | Uses `PLANT_ID_API_KEY` in FastAPI with fallback to `DemoPredictor` when `DEMO_MODE=true` |
| **Plant Knowledge API** | Configured / Proxy | Uses `PERENUAL_API_KEY` merged with local `CROP_CULTIVATION_KB` |
| **Weather Risk API** | Real Proxy | Uses OpenWeatherMap `WEATHER_API_KEY` for live weather & risk matrix |
| **AI Chatbot** | Real Proxy | Uses Google Gemini / OpenRouter API (`GEMINI_API_KEY` & `OPENROUTER_API_KEY`) |
| **Firebase Auth** | Real Frontend | Project `agroscan-ai-07` configured in `frontend/.env` |

---

## 4. Frontend & Backend Routes Audit
| Route | Page Component | Purpose | Backend Endpoint | Status |
|---|---|---|---|---|
| `/` | `LandingPage.jsx` | AgroScan AI Welcome & Core Features | N/A | Operational |
| `/login` | `LoginPage.jsx` | Farmer / Admin Login | `POST /api/v1/auth/login` | Operational |
| `/register` | `RegisterPage.jsx` | Account Creation | `POST /api/v1/auth/register` | Operational |
| `/forgot-password` | `ForgotPasswordPage.jsx` | Password Reset Request | Firebase Auth | Operational |
| `/dashboard` | `DashboardPage.jsx` | Farmer Overview & Statistics | `GET /api/v1/analytics/dashboard` | Operational |
| `/scan` | `ScanPage.jsx` | Camera-First Leaf Diagnostic | `POST /api/v1/predictions/analyze` | Operational |
| `/analysis` | `AnalysisPage.jsx` | 8-Step Scanning Progress | `POST /api/v1/predictions/analyze` | Operational |
| `/results/:scanId` | `ResultPage.jsx` | Comprehensive Diagnosis Report | `GET /api/v1/predictions/{id}` | Operational |
| `/history` | `HistoryPage.jsx` | Scan History Archive | `GET /api/v1/predictions/history` | Operational |
| `/analytics` | `AnalyticsPage.jsx` | Farm Analytics & Outbreak Trends | `GET /api/v1/analytics/dashboard` | Operational |
| `/weather` | `WeatherRiskPage.jsx` | Weather Outbreak Risk | `GET /api/v1/weather/current` | Operational |
| `/assistant` | `AssistantPage.jsx` | AI Agronomist Chatbot | `POST /api/v1/chat` | Operational |
| `/profile` | `ProfilePage.jsx` | My Farm Profile | `GET /api/v1/farms` | Operational |
| `/admin` | `AdminDashboardPage.jsx` | System Admin Console | `GET /api/v1/admin/analytics` | Operational |

---

## 5. Security & Risk Audit
- **API Key Exposure**: ALL API keys (`GEMINI_API_KEY`, `WEATHER_API_KEY`, `PLANT_ID_API_KEY`, `PERENUAL_API_KEY`) are secured inside `backend/.env`. Zero keys in React.
- **IDOR Protection**: Enforced `user_id` ownership checks on scan predictions, chat context, and farm profiles.
- **Password Protection**: Salted PBKDF2-SHA256 (100,000 iterations) with legacy bcrypt compatibility.
- **Global Exception Shield**: Prevents unhandled exceptions from crashing FastAPI workers.
- **CORS Handling**: Strictly configured for frontend domains with security headers (`X-Frame-Options`, `X-Content-Type-Options`).

---

## 6. Data Science Audit
- Current backend supports OpenCV image loading and color space ratio calculations for preliminary lesion severity.
- ML Directory structure `ml/` needs complete expansion into data, notebooks, preprocessing, training, evaluation, and inference modules to enable custom computer vision model comparisons.
