# AgroScan AI — Security Audit & Defense-in-Depth Specification

**Date**: August 16, 2026  
**Standards Compliance**: OWASP Top 10:2025, NIST SP 800-53, ISO 27001 Controls  

---

## 1. OWASP Top 10:2025 Mitigation Matrix

### A01: Broken Access Control
- **Server-Side Authorization**: Every endpoint verifying user data (`/api/v1/predictions/{id}`, `/api/v1/farms`, `/api/v1/history`) evaluates `filter(user_id == current_user.id)` on the server-side.
- **Role Isolation**: Admin routes (`/api/v1/admin/*`) require explicit `role == 'admin'` verification via `get_current_user` dependency.

### A02: Security Misconfiguration
- **CORS Protection**: Wildcard origins (`allow_origins=["*"]`) are disabled in production (`DEMO_MODE=false`).
- **Security Headers**: Standard HTTP headers injected via middleware:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Referrer-Policy: strict-origin-when-cross-origin`

### A03: Software Supply Chain Failures
- Dependencies audited via `npm audit` and `pip` security tools.
- Strict version pin templates provided in `requirements.txt` and `package.json`.

### A04: Cryptographic Failures
- Passwords salted and hashed using PBKDF2-SHA256 with 600,000 iterations.
- JWT tokens signed using HS256 algorithm with strong secret key.

### A05: Injection
- All database queries executed via SQLAlchemy 2.0 ORM parameterized statements.
- Input strings sanitized against XSS and prompt injection before forwarding to Gemini.

### A06: Insecure Design
- Defensive design prevents single-point-of-failure API cascade crashes.

### A07: Authentication Failures
- Firebase Authentication (`agroscan-ai-07`) with `browserLocalPersistence` and token verification.

### A08: Software & Data Integrity
- Image uploads verified via PIL magic-byte decoding and Variance of Laplacian blur checks.

### A09: Security Logging & Alerting
- Structured logging records failed auth attempts, file validation failures, and exception tracebacks without logging secrets or passwords.

### A10: Exceptional Conditions
- Global zero-crash exception handlers return sanitized `500` JSON errors without exposing stack traces to end users.
