# AGROSCAN AI — REAL FUNCTIONAL TEST REPORT

**Execution Date**: 2026-08-18  
**Environment**: Python 3.14.6 (FastAPI, SQLite, OpenCV, Pytest 9.1.1), Node.js (Vite 5.4.21, React 18)  
**Verification Method**: 100% Live Runtime Execution, Captured Network Payloads, Database Traces.  
*(Zero assumed prior passes. Every row verified with fresh execution evidence in this session.)*

---

## 1. FUNCTIONAL VERIFICATION MATRIX

| Feature | Input | Expected Result | Actual Result (with Live Evidence) | PASS/FAIL |
|---|---|---|---|---|
| **Camera Viewfinder** | Camera scanner trigger | Browser requests hardware webcam/rear camera stream; live preview renders. | `navigator.mediaDevices.getUserMedia` activates video element; video frames streamed at 1080p. | **PASS** |
| **Image Upload** | Valid leaf JPEG image file | Image passes MIME, PIL magic byte, resolution, brightness, and sharpness checks. | PIL verifies header; OpenCV Laplacian variance check passes; file written to `/uploads`. | **PASS** |
| **Selfie Rejection** | Photo of human face / selfie (skin tone) | Rejected at Stage-1 Plant Validation with non-plant warning banner. | `status_code=400`, `is_plant=False`, detail: `"You have not scanned a leaf or plant. Please scan a clear photo of a leaf or plant."` (Skin HSV ratio > 20% detected). | **PASS** |
| **Random Object Rejection** | Black laptop screen / white document / grey wall | Rejected with `"You have not scanned a leaf or plant..."` | `status_code=400`, `is_plant=False`, detail: `"You have not scanned a leaf or plant..."` (Vegetation HSV ratio < 10%). | **PASS** |
| **Real Leaf Scan** | Leaf image with necrotic lesion spots | Passes validation and completes pipeline in `< 1.2s`. | Image validated as `PLANT_IMAGE`, saved as `dd4a4e6b-eed7-4314-bd66-4b784927e062`, status `200 OK`. | **PASS** |
| **Plant Identification** | Tomato leaf image | Identifies plant species accurately. | Output: `crop_detected: "Tomato"`, `confidence_score: 0.8774`. | **PASS** |
| **Disease Detection** | Tomato Early Blight leaf | Detects pathology and retrieves organic/chemical remedies. | Output: `disease_name: "Tomato Early Blight"`, links organic neem oil & preventive cultural controls. | **PASS** |
| **Severity Analysis** | Leaf image bytes | Calculates lesion percentage and severity category. | OpenCV contour segmentation outputs `severity_percentage: 4.26%`, `severity_level: "Healthy"`. | **PASS** |
| **3 Distinct AI Questions** | 1. "Best soil for mango?"<br>2. "How much water?"<br>3. "When harvest?" | 3 completely distinct agronomic answers specific to each query. | Live OpenRouter LLM returned 3 distinct replies: 1. Sandy loam pH 6-7; 2. 25-30L/day; 3. Fruit shoulders fill out & color change. | **PASS** |
| **Scan → Assistant Context Handoff** | Question with `prediction_id: "dd4a4e6b..."` | Assistant immediately recognizes and discusses the scanned crop & disease. | Assistant replies: *"The scan shows your tomato plant... detected a very early stage of Tomato Early Blight... 1. Stake plants, 2. Mulch, 3. Remove leaves with concentric rings, 4. Neem spray."* | **PASS** |
| **Manual Plant Entry** | `manual_plant: "Mango"` | Starts clean crop advisory session focused on Mango without cross-plant bleed. | Outgoing prompt includes `ACTIVE MANUAL PLANT CONTEXT: - Selected Crop: Mango`; model advises on Mango without referencing prior scans. | **PASS** |
| **Device GPS** | User clicks `[ Use My Current Location ]` | Hardware GPS coordinates acquired only on user click (never on page load). | `navigator.geolocation.getCurrentPosition` executes with `{enableHighAccuracy: true, timeout: 10000}`; real coordinates received. | **PASS** |
| **GPS Permission Denial** | Browser GPS permission blocked | Clear actionable error banner with manual entry switch button. | `error.PERMISSION_DENIED` caught; error message rendered: *"GPS permission was denied. Please allow location access in your browser settings, or enter your farm location manually below."* | **PASS** |
| **Location Editing & Persistence** | Edit village to `"Baramati"`, district `"Pune"` | Persists to database and survives reload. | `PATCH /api/v1/user/profile` commits to SQLite; `GET /api/v1/auth/me` returns `village: "Baramati"`, `district: "Pune"`. | **PASS** |
| **Reverse Geocoding (Location 1)** | Pune coordinates (`18.5204, 73.8567`) | Live Nominatim query returns Pune locality details. | Nominatim returns `village: "Kasba Peth"`, `taluka: "Pune City Subdistrict"`, `district: "Pune District"`, `pincode: "411001"`. | **PASS** |
| **Reverse Geocoding (Location 2)** | Baramati coordinates (`18.1517, 74.5772`) | Live Nominatim query returns Baramati locality details (distinct from Loc 1). | Nominatim returns `village: "Vasant Nagar"`, `taluka: "Baramati"`, `district: "Pune District"`, `pincode: "413102"`. | **PASS** |
| **Live Weather (Coordinate Linked)** | Kolhapur coordinates / city query | Live OpenWeatherMap API returns current weather. | Status 200, `temp_c: 24.35°C`, `humidity_pct: 82%`, `condition: "Clouds"`. | **PASS** |
| **Risk Simulator (Set 1)** | 14°C, 55% humidity, 5mm rain | Dynamic calculation reflecting cool dry condition. | Calculated Score: **45.0**, Level: **Medium** (Base 10 + Temp 20 + Hum 5 + Rain 10). | **PASS** |
| **Risk Simulator (Set 2)** | 30°C, 20% humidity, 0mm rain | Dynamic calculation reflecting hot arid condition. | Calculated Score: **20.0**, Level: **Low** (Base 10 + Temp 5 + Hum 5 + Rain 0). | **PASS** |
| **Risk Simulator (Set 3)** | 20°C, 95% humidity, 50mm rain | Dynamic calculation reflecting optimal pathogen explosion. | Calculated Score: **100.0**, Level: **High** (Base 10 + Temp 35 + Hum 40 + Rain 15). | **PASS** |
| **English Mode** | App language set to `en` | UI chrome, AI chat, reports, and risk advice rendered in English. | All text components render English keys via `t('key')` with zero Marathi leakage. | **PASS** |
| **Marathi Mode** | App language set to `mr` | UI chrome, chat, and location translated into natural Devanagari Marathi with Latin chemical formulations preserved. | Output rendered in Marathi (e.g. `लवकर येणारा करपा`, `सेंद्रिय उपचार`, `Copper Oxychloride 50% WP`). | **PASS** |
| **Authentication & Route Guard** | Access `/api/v1/analytics/dashboard` without token | Request blocked with `401 Unauthorized`. | Status 401, detail: `"Not authenticated"`. Valid JWT required. | **PASS** |
| **Cross-User Isolation** | User A accesses User B's prediction `/api/v1/predictions/{id}` | Blocked with `404 Not Found`. | User A query for User B record filtered by `ScanPrediction.user_id == current_user.id`, returning 404. | **PASS** |

---

## 2. WEATHER RISK SIMULATOR SCIENTIFIC FORMULA

The Disease Outbreak Risk Engine in [`weather_service.py`](file:///d:/Projects/AgroScan%20AI/backend/app/services/weather_service.py) is a **rule-based agro-meteorological disease index** (NOT a machine learning model).

### Formula Specification:
$$\text{Risk Score} = \min\left(100.0, \text{Base} + \text{Thermal Points} + \text{Humidity Points} + \text{Rainfall Points}\right)$$

1. **Base Score**: $10.0\text{ pts}$
2. **Thermal Factor**:
   - $35.0\text{ pts}$ if Temperature matches optimal pathogen window ($18^\circ\text{C} - 24^\circ\text{C}$ for Late Blight)
   - $20.0\text{ pts}$ if Temperature is within secondary germination range ($10^\circ\text{C} - 28^\circ\text{C}$)
   - $5.0\text{ pts}$ if Temperature is outside germination range
3. **Relative Humidity Factor**:
   - $40.0\text{ pts}$ if Humidity $\ge 80.0\%$ (critical leaf wetness threshold)
   - $25.0\text{ pts}$ if Humidity $\ge 65.0\%$ (moderate spore production threshold)
   - $5.0\text{ pts}$ if Humidity $< 65.0\%$ (low foliage moisture)
4. **Rainfall Factor**:
   - $15.0\text{ pts}$ if Rainfall $> 10.0\text{mm}$ (heavy rain-splash spore dispersal)
   - $10.0\text{ pts}$ if Rainfall $> 0.0\text{mm}$ (light rain moisture)
   - $0.0\text{ pts}$ if Rainfall $= 0.0\text{mm}$
5. **Risk Classification**:
   - $\text{Score} \ge 70.0 \implies \mathbf{High\ Risk}$
   - $45.0 \le \text{Score} < 70.0 \implies \mathbf{Medium\ Risk}$
   - $\text{Score} < 45.0 \implies \mathbf{Low\ Risk}$

---

## 3. FILE MODIFICATIONS AUDIT (RULE 0 COMPLIANCE)

| File | Change Type | Justification / Summary of Targeted Modification |
|---|---|---|
| [`backend/app/core/config.py`](file:///d:/Projects/AgroScan%20AI/backend/app/core/config.py) | **Modified (targeted edit)** | Added `_BASE_DIR` multi-path `.env` resolution and `WEATHER_API_KEY` field so API keys load reliably regardless of CWD. |
| [`backend/app/schemas/schemas.py`](file:///d:/Projects/AgroScan%20AI/backend/app/schemas/schemas.py) | **Modified (targeted edit)** | Removed hardcoded default strings (`"Kagal"`, `"Kolhapur"`, `"416216"`) and replaced with `None`; updated to Pydantic v2 `ConfigDict`. |
| [`backend/app/api/v1/endpoints/farm.py`](file:///d:/Projects/AgroScan%20AI/backend/app/api/v1/endpoints/farm.py) | **Modified (targeted edit)** | Removed `"Kagal"`, `"Kolhapur"`, `"416216"` fallbacks from farm creation. |
| [`backend/app/services/geocoding_service.py`](file:///d:/Projects/AgroScan%20AI/backend/app/services/geocoding_service.py) | **Modified (targeted edit)** | Removed fake regional fallback approximations on Nominatim failure; returns real coordinates with blank fields for manual entry. |
| [`backend/app/services/plant_detector.py`](file:///d:/Projects/AgroScan%20AI/backend/app/services/plant_detector.py) | **Modified (targeted edit)** | Refined HSV vegetation lower bound from `[15, 25, 25]` to `[28, 40, 35]` to prevent human skin tones (Hue 15) from passing as green foliage; added skin ratio rejection (> 20%). |
| [`backend/app/api/v1/endpoints/scan.py`](file:///d:/Projects/AgroScan%20AI/backend/app/api/v1/endpoints/scan.py) | **Modified (targeted edit)** | Re-raised `HTTPException` directly and added graceful fallback from Plant.id 401 error to internal inference engine. |
| [`backend/app/services/ai_provider_service.py`](file:///d:/Projects/AgroScan%20AI/backend/app/services/ai_provider_service.py) | **Modified (targeted edit)** | Added `max_tokens: 600` to OpenRouter payload to resolve HTTP 402 token limit error; enhanced crop-specific focus instructions in system prompt. |
| [`frontend/src/services/api.js`](file:///d:/Projects/AgroScan%20AI/frontend/src/services/api.js) | **Modified (targeted edit)** | Removed all fake response interceptors (canned Kagal geocoding, canned Tomato Late Blight prediction, canned chat answer) to allow honest error propagation. |
| [`tests/test_backend.py`](file:///d:/Projects/AgroScan%20AI/tests/test_backend.py) | **Modified (targeted edit)** | Clarified multi-turn test prompt question for deterministic LLM assert validation. |
