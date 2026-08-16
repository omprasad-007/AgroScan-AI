# AgroScan AI — Production Deployment Guide

## Production Topology
- **Frontend Host**: Vercel Static CDN (`https://agro-scan-ai-nine.vercel.app/`)
- **Backend Host**: Render Cloud Server (`https://agroscan-ai-backend.onrender.com/`)
- **Database**: PostgreSQL (Render Database) or SQLite (`agroscan.db`)

---

## Environment Variables Configuration

### Backend Production Environment (`backend/.env`)
```ini
APP_NAME="AgroScan AI"
APP_ENV="production"
DEBUG=false
DEMO_MODE=false
PORT=8000

DATABASE_URL="postgresql://user:password@hostname:5432/agroscan_db"
SECRET_KEY="generate_random_key_using_openssl"
FRONTEND_URL="https://agro-scan-ai-nine.vercel.app"

PLANT_ID_API_KEY="your_production_plant_id_key"
PERENUAL_API_KEY="your_production_perenual_key"
WEATHER_API_KEY="your_production_weather_key"
GEMINI_API_KEY="your_production_gemini_key"
```

### Frontend Production Environment (`frontend/.env`)
```ini
VITE_API_BASE_URL="https://agroscan-ai-backend.onrender.com/api/v1"
VITE_FIREBASE_API_KEY="your_firebase_key"
VITE_FIREBASE_AUTH_DOMAIN="agroscan-ai-07.firebaseapp.com"
VITE_FIREBASE_PROJECT_ID="agroscan-ai-07"
```

---

## Deployment Steps

### 1. Backend (Render)
1. Push latest code to GitHub repository `omprasad-007/AgroScan-AI`.
2. Connect Render Blueprint using `render.yaml`.
3. Set production environment variables in Render Dashboard.

### 2. Frontend (Vercel)
1. Import repository on Vercel (`Root Directory: frontend`).
2. Verify `vercel.json` SPA rewrite is active.
3. Deploy frontend production build.
