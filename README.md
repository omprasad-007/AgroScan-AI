# AgroScan AI — Smart Plant Disease Detection & Crop Health Monitoring System

**AgroScan AI** is an enterprise-grade Smart Agriculture & Data Science platform designed for instant plant disease identification, leaf lesion severity analysis, crop cultivation guidance, weather outbreak forecasting, and context-aware AI advisory.

---

## 🌟 Key Features & Capabilities

1. **📷 Real Browser Camera Scanner**:
   - Built using browser `MediaDevices.getUserMedia()` with live video feed.
   - Features an environment-facing (rear) camera switcher, snapshot canvas rendering, visual leaf-viewfinder target overlay, and guidance prompts (*"Place the affected leaf inside the frame"*).
   - Supports mobile phones, tablets, laptops, and desktop webcams with graceful permission error handling and device file upload fallbacks.

2. **🌿 Plant Identification & Crop Cultivation Knowledge Base**:
   - Integrates complete plant species information, botanical names, and family classification.
   - Provides step-by-step agricultural cultivation guidance covering **Soil Type**, **Sunlight**, **Sowing Time**, **Transplanting Spacing**, **Irrigation Schedule**, **Fertilization Doses**, and **Harvesting Indicators**.

3. **🔒 Enterprise Security & Anti-Hacking Hardening**:
   - **IDOR Protection**: Enforces user ownership (`user_id`) on scan predictions, chat context, and recommendation endpoints to prevent unauthorized cross-tenant data access.
   - **Salted Password Hashing**: Upgraded password security to salted **PBKDF2-SHA256** (100,000 iterations) with constant-time comparison and legacy hash compatibility.
   - **Privilege Escalation Shield**: Eliminated user self-assignment of `admin` role in signup endpoints.
   - **SSRF / URL Injection Defense**: URL-encodes external API queries.
   - **HTTP Security Headers**: Enforces `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection`, and strict CORS policies.

4. **🛡️ Zero-Crash Architecture (Fault Tolerance)**:
   - **Global FastAPI Exception Handler**: Captures all unhandled runtime errors, preventing server crashes or stack trace leakage.
   - **Image Payload & Magic-Byte Verification**: Validates file MIME types, extensions, and byte headers via PIL prior to OpenCV or ML model inference.
   - **Payload Size Limiter**: Enforces a 10MB payload size limit to prevent Out-Of-Memory (OOM) worker crashes.
   - **React Error Boundary**: Catches uncaught UI rendering exceptions and displays a graceful fallback screen with recovery buttons.

5. **💾 Per-User LocalStorage Persistence**:
   - Every registered user (`name@gmail.com`) receives clean, isolated `localStorage` state (`agroscan_predictions_${email}`, `agroscan_farms_${email}`).
   - New user accounts start 100% fresh with 0 initial scans, clean user profile, and personalized dashboard stats.
   - Complete logout state cleanup ensures secure session termination upon clicking **Logout**.

6. **🌦️ Weather Outbreak Risk Engine**:
   - Evaluates ambient temperature, humidity, and rainfall matrix to compute disease transmission risk scores (`Low`, `Medium`, `High`, `Critical`).

7. **🤖 AI Agronomist Assistant**:
   - Context-aware chatbot supporting Google Gemini and OpenAI / OpenRouter API models.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite 5, Tailwind CSS 3, React Router v6, Axios, Recharts, Lucide Icons, i18n
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL / SQLite, PyJWT, Passlib (PBKDF2 / Bcrypt), Uvicorn, Gunicorn
- **Data Science & Computer Vision**: OpenCV, NumPy, Pandas, Scikit-learn, PIL / Pillow, TensorFlow / Keras (MobileNetV2 Transfer Learning)
- **APIs & Models**: Plant.id, Perenual Plant API, Google Gemini, OpenRouter, OpenWeatherMap

---

## 🚀 Local Quick Start Instructions

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Run FastAPI Server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Backend API Root**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
- **React Frontend**: [http://127.0.0.1:5173/](http://127.0.0.1:5173/)

---

## ☁️ Live Cloud Deployment

### 1. Backend Deployment (Render)
- Deploy using **Render Blueprint** with `render.yaml` or create a Web Service pointing to `backend/`:
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2. Frontend Deployment (Vercel)
- Import repository to **Vercel** with Root Directory set to `frontend/`:
  - **Environment Variable**: `VITE_API_BASE_URL=https://agroscan-ai-backend.onrender.com/api/v1`

---

## 🧪 Testing

```bash
$env:PYTHONPATH="backend"; python -m pytest tests/
```
All 9 automated backend test cases cover security headers, PBKDF2 hashing, IDOR protection, image validation, and route authentication.
