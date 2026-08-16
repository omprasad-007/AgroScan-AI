# AgroScan AI — API Architecture & Service Integration Matrix

## Overview & Base Endpoints
- **Base URL (V1)**: `/api/v1` (with `/api` fallback aliases)
- **Content-Type**: `application/json` (except `/api/v1/predictions/analyze` accepting `multipart/form-data`)

---

## Endpoint Catalog & Authentication Requirements

| Endpoint | Method | Auth Required | Rate Limit | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/api/v1/health` | `GET` | No | None | System health status & environment check |
| `/api/v1/health/ready` | `GET` | No | None | Readiness probe for production load balancers |
| `/api/v1/auth/register` | `POST` | No | 10/min | Register new farmer account |
| `/api/v1/auth/login` | `POST` | No | 10/min | Authenticate user credentials & issue JWT |
| `/api/v1/auth/firebase-login` | `POST` | No | 15/min | Synchronize Firebase Auth user session |
| `/api/v1/predictions/analyze` | `POST` | Yes | 15/min | Primary leaf scan analysis pipeline |
| `/api/v1/predictions/history` | `GET` | Yes | None | Retrieve user-specific scan history |
| `/api/v1/predictions/{id}` | `GET` | Yes | None | Retrieve single prediction report (IDOR protected) |
| `/api/v1/recommendations/{pred_id}`| `GET` | Yes | None | Retrieve certified organic & chemical treatments |
| `/api/v1/crop-guides/{crop}` | `GET` | No | None | Retrieve cultivation timeline & spacing care guide |
| `/api/v1/weather/risk` | `POST` | No | 30/min | Microclimate relative humidity & thermal risk matrix |
| `/api/v1/chat` | `POST` | Yes | 20/min | Gemini AI Agronomist consultation assistant |
| `/api/v1/farms` | `GET/POST` | Yes | None | Farm plot fields manager |
| `/api/v1/analytics/dashboard` | `GET` | Yes | None | Real user scan health distribution analytics |
| `/api/v1/admin/analytics` | `GET` | Yes (Admin) | None | System admin metrics console |

---

## Fault Tolerance & Graceful Degradation Strategy

```
[ Leaf Upload ] ──► [ Quality Check ] ──► [ Model Inference ]
                                                 │
                                                 ├── (SUCCESS) ──► Plant & Disease
                                                 │
                                                 ├── [ Optional: Weather Risk ] (Fallback if down)
                                                 ├── [ Optional: Perenual Care ] (Fallback if down)
                                                 └── [ Optional: Gemini AI ] (Fallback if down)
```
If an optional external API is unavailable, the core disease diagnosis still succeeds, marking optional sections as `"temporarily unavailable"`.
