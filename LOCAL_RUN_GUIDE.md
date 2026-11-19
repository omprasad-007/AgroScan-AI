# AgroScan AI — Local Run & Development Guide
**Operating System:** Windows 11 64-bit | **Hardware:** Intel Core i5 / 8 GB RAM / Dell Latitude 5420

---

## 1. Prerequisites

Before starting the application, ensure you have:
1. **Python 3.10+ (Python 3.14 recommended):** Available in `.venv`
2. **Node.js 18+ & npm:** For running Vite frontend
3. **Local Model Files:** Present in `backend/models/plantvillage-mobilenetv2/`

---

## 2. Running the Backend (FastAPI)

### Step 1: Open PowerShell or Command Prompt
Navigate to the root project directory:
```powershell
cd "d:\Projects\AgroScan AI"
```

### Step 2: Activate the Virtual Environment
```powershell
# PowerShell:
.\.venv\Scripts\Activate.ps1

# Or Command Prompt (cmd.exe):
.\.venv\Scripts\activate.bat
```

> [!NOTE]
> If PowerShell displays a `PSSecurityException` regarding script execution, run:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### Step 3: Verify Model Files
Ensure model files exist before booting:
```powershell
Get-ChildItem backend\models\plantvillage-mobilenetv2
```
Expected output includes `model.safetensors`, `config.json`, `preprocessor_config.json`, `calibration.json`, and `threshold.json`.

### Step 4: Start the FastAPI Server
```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
You will see output indicating startup:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
[AgroScan AI] Application startup complete. Database connected.
INFO:     Application startup complete.
```

### Step 5: Verify Backend Health
Open a second terminal window and test:
```powershell
curl http://127.0.0.1:8000/api/model/health
```
Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu",
  "label_count": 38,
  "calibration_temperature": 0.8845188130635788,
  "uncertainty_threshold": 0.5
}
```

Interactive Swagger API documentation is available in your browser at:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 3. Running the Frontend (React + Vite)

### Step 1: Open a New Terminal
Navigate to the `frontend/` directory:
```powershell
cd "d:\Projects\AgroScan AI\frontend"
```

### Step 2: Install Node Dependencies (if needed)
```powershell
npm install
```

### Step 3: Start the Vite Development Server
```powershell
npm run dev
```
Output:
```
  VITE v5.4.14  ready in 450 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Step 4: Open AgroScan AI in Your Browser
Visit **[http://localhost:5173](http://localhost:5173)**.

---

## 4. Testing MobileNetV2 Inference Locally

### Option A: Via AgroScan AI Web UI
1. Navigate to **[http://localhost:5173/scan](http://localhost:5173/scan)** in your browser.
2. Select or drag-and-drop a plant leaf image (e.g. Tomato or Apple leaf).
3. Select the crop type (e.g. `Tomato`).
4. Click **Diagnose Plant**.
5. Inspect the result on `ResultPage`:
   - Note the **MobileNetV2 (PlantVillage v1.1)** badge.
   - Observe the calibrated confidence score.
   - Inspect the Top-3 differential predictions.
   - Toggle language to Marathi (मराठी) using the top navigation bar to verify bilingual rendering.

### Option B: Via Command Line (Direct API)
```powershell
# Using curl in PowerShell or CMD:
curl -X POST http://127.0.0.1:8000/api/model/predict `
  -F "file=@tests/sample_leaf.jpg" `
  -F "crop_name=Tomato"
```

---

## 5. Running Automated Tests

Run the full automated test suite anytime using pytest:

```powershell
# Run the complete test suite (78 tests):
.\.venv\Scripts\python.exe -m pytest tests/

# Run only the MobileNetV2 integration suite (26 tests):
.\.venv\Scripts\python.exe -m pytest tests/test_mobilenet_model_integration.py -v
```

---

## 6. Common Troubleshooting on Windows 11

### 1. Port 8000 or 5173 Already in Use
If another process holds port 8000:
```powershell
# Find the PID holding port 8000:
netstat -ano | findstr :8000

# Stop the process by PID:
taskkill /PID <PID> /F
```

### 2. PowerShell Script Execution Disabled
If running `.venv\Scripts\activate` fails with `cannot be loaded because running scripts is disabled`:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Or run commands directly via python executable without activation:
```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload
```

### 3. Model Files Missing
If the backend logs `Model files not found in backend/models/plantvillage-mobilenetv2`:
Ensure `backend/models/plantvillage-mobilenetv2/model.safetensors` exists. Do not manually extract or rename files; verify with `backend/models/model_manifest.json`.

### 4. Database Locked or Busy
The local SQLite database is at `agroscan.db`. If SQLite reports database locked, ensure no lingering python instances are running:
```powershell
taskkill /IM python.exe /F
```
