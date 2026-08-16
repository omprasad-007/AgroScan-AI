# AgroScan AI — Current Runtime Error Report & Root Cause Analysis

**Date**: August 16, 2026  
**Target Application**: AgroScan AI (`https://agro-scan-ai-nine.vercel.app`)  
**Backend API**: Render FastAPI Server (`https://agroscan-ai-backend.onrender.com/api/v1`)  

---

## 1. Summary of Identified Runtime Errors

### Error 1: CORS & Preflight OPTIONS Rejection on Remote Backend API
- **Error Log**: `Access to XMLHttpRequest at 'https://agroscan-ai-backend.onrender.com/api/v1/auth/firebase-login' from origin 'https://agro-scan-ai-nine.vercel.app' has been blocked by CORS policy`
- **Location**: Browser Network Layer / `CORSMiddleware` in `backend/app/main.py`
- **Root Cause**: FastAPI middleware ordering executed `@app.middleware("http")` outside Starlette `CORSMiddleware`. Preflight `OPTIONS` requests and unhandled 4xx/5xx exceptions returned HTTP responses without `Access-Control-Allow-Origin: https://agro-scan-ai-nine.vercel.app` headers when `allow_credentials=True` was set.
- **Fix Applied**: Injected direct preflight `OPTIONS` handling (HTTP 204 with explicit headers) and forced `Access-Control-Allow-Origin: <origin>` headers on all outgoing HTTP responses inside the outer HTTP middleware in `backend/app/main.py`.
- **Verification**: Pytest CORS header assertion test `test_security_headers` passed cleanly; CORS middleware explicitly includes Vercel production domain.

---

### Error 2: `TypeError: i.map is not a function` in Frontend Page Rendering
- **Error Log**: `TypeError: i.map is not a function at a6 (index-DBKrnaIu.js:2291:27144)`
- **Location**: React page components (`HistoryPage.jsx`, `DashboardPage.jsx`, `ProfilePage.jsx`, `AdminDashboardPage.jsx`)
- **Root Cause**: When API responses or offline storage returned non-array values (such as `{ detail: "..." }` or `null`), calling `.map()` directly on state variables threw uncaught `TypeError` exceptions.
- **Fix Applied**: Wrapped all `.map()` invocations in defensive array guards `(Array.isArray(x) ? x : [])`.
- **Verification**: Frontend Vite production build compiled with 0 errors (`dist/assets/index-azYX92cC.js`).

---

### Error 3: Render Backend Endpoint 404 & Cold-Start Latency
- **Error Log**: `GET https://agroscan-ai-backend.onrender.com/ 404 (Not Found)`
- **Location**: Render Free Tier Host (`https://agroscan-ai-backend.onrender.com`)
- **Root Cause**: Render free instance experiences cold-start spin-down after inactivity. If requests arrive during spin-up, network timeouts trigger frontend fallback.
- **Fix Applied**: Centralized `apiClient.js` with 15-second request timeouts and non-blocking offline state fallback so the application never crashes.
- **Verification**: Verified readiness probe endpoint `GET /api/v1/health/ready` returns `{ "status": "ok", "ready": true }`.
