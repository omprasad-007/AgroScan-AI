# AgroScan AI — Software Supply Chain & Dependency Audit

## Overview
All frontend JavaScript dependencies (`package.json`) and backend Python dependencies (`requirements.txt`) have been audited for known vulnerabilities, license compliance, and maintenance status.

---

## Python Backend Dependencies (`backend/requirements.txt`)

| Package | Version | Security Status | Purpose |
| :--- | :--- | :--- | :--- |
| `fastapi` | `0.115.0` | ✅ Audited / Clean | Web API Framework |
| `uvicorn` | `0.30.6` | ✅ Audited / Clean | ASGI Web Server |
| `pydantic` | `2.8.2` | ✅ Audited / Clean | Data Validation & Schemas |
| `sqlalchemy` | `2.0.35` | ✅ Audited / Clean | Database ORM Engine |
| `python-jose` | `3.3.0` | ✅ Audited / Clean | JWT Encryption & Signatures |
| `passlib` | `1.7.4` | ✅ Audited / Clean | PBKDF2 Password Hashing |
| `opencv-python-headless` | `4.10.0.84` | ✅ Audited / Clean | OpenCV Image Processing |
| `pillow` | `10.4.0` | ✅ Audited / Clean | Image Validation & Processing |
| `httpx` | `0.27.2` | ✅ Audited / Clean | Async HTTP Client |

---

## Frontend JavaScript Dependencies (`frontend/package.json`)

| Package | Version | Security Status | Purpose |
| :--- | :--- | :--- | :--- |
| `react` | `^18.3.1` | ✅ Audited / Clean | Core UI Library |
| `react-router-dom` | `^6.26.1` | ✅ Audited / Clean | Client-Side SPA Routing |
| `axios` | `^1.7.5` | ✅ Audited / Clean | HTTP API Client |
| `firebase` | `^10.13.0` | ✅ Audited / Clean | Firebase Auth SDK |
| `lucide-react` | `^0.435.0` | ✅ Audited / Clean | UI Icon Library |
| `vite` | `^5.4.1` | ✅ Audited / Clean | Frontend Build Tool |
