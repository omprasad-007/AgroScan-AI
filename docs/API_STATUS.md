# AgroScan AI — API Service Status & Endpoint Readiness Report

**Audit Date**: August 16, 2026  
**Backend Base URL**: `/api/v1` (with `/api` compatibility aliases)  

---

## Endpoint Catalog & Integration Readiness

| Endpoint Route | Status | Auth Guard | Failure Strategy |
| :--- | :--- | :--- | :--- |
| `GET /api/v1/health` | 🟢 Active | Public | Returns system health & model type |
| `GET /api/v1/health/ready` | 🟢 Active | Public | Readiness probe for production load balancers |
| `POST /api/v1/auth/register` | 🟢 Active | Public | Creates user account with salted PBKDF2 hashing |
| `POST /api/v1/auth/login` | 🟢 Active | Public | Authenticates credentials & issues JWT token |
| `POST /api/v1/auth/firebase-login` | 🟢 Active | Public | Synchronizes Firebase user identity |
| `POST /api/v1/predictions/analyze` | 🟢 Active | Bearer JWT | Plant.id API / MobileNetV2 + OpenCV severity |
| `GET /api/v1/predictions/history` | 🟢 Active | Bearer JWT | Returns current user's scan history only |
| `GET /api/v1/predictions/{id}` | 🟢 Active | Bearer JWT | IDOR protected prediction report |
| `GET /api/v1/weather/risk` | 🟢 Active | Public | OpenWeatherMap microclimate risk engine |
| `POST /api/v1/chat` | 🟢 Active | Bearer JWT | Google Gemini AI Agronomist consultation |
| `GET /api/v1/analytics/dashboard` | 🟢 Active | Bearer JWT | Real user scan health metrics |
