# AgroScan AI — Incident Response & Secret Rotation Playbook

## 1. Scope & Objective
This operational playbook establishes standard operating procedures for responding to security incidents, compromised credentials, or external service disruptions in the AgroScan AI production system.

---

## 2. Emergency Key Rotation Procedure

If an API key (`GEMINI_API_KEY`, `WEATHER_API_KEY`, `PLANT_ID_API_KEY`, `PERENUAL_API_KEY`, `SECRET_KEY`) is accidentally exposed in source code, commit history, or logs:

1. **Immediate Revocation**:
   - Access the provider console (Google Cloud, OpenWeatherMap, Plant.id, Perenual) and revoke/delete the compromised key immediately.
2. **Generate Replacement Credentials**:
   - Generate a new API key from the provider platform.
3. **Update Production Environment Variables**:
   - Navigate to the Render Dashboard / Vercel Environment Settings.
   - Update the relevant environment variable (e.g. `PLANT_ID_API_KEY`).
   - Trigger a clean redeployment.
4. **Purge Commit History (If committed)**:
   - Use `git filter-repo` or BFG Repo-Cleaner if a key was committed to Git history.
   - Force push cleaned commits to remote `origin main`.

---

## 3. Incident Severity Triage Matrix

| Severity Level | Trigger Condition | Response SLA | Mitigation Action |
| :--- | :--- | :--- | :--- |
| **SEV-1 (Critical)** | Database corruption, Auth bypass, Active key breach | Immediate (<15 mins) | Revoke keys, restore DB snapshot, restrict backend CORS |
| **SEV-2 (High)** | Plant.id or OpenWeatherMap API down | < 1 Hour | System automatically falls back to baseline knowledge without crashing |
| **SEV-3 (Medium)**| Non-fatal frontend component error | < 4 Hours | React ErrorBoundary provides 1-tap "Clear Cache & Reset Session" |
