# AgroScan AI — Smart Plant Disease Detection & Crop Health Monitoring System

**AgroScan AI** is an end-to-end data science and smart agriculture application designed to solve manual disease identification, delayed outbreak detection, incorrect pesticide selection, lack of leaf lesion severity analysis, and weather-based risk forecasting.

---

## Key Features

1. **AI Disease Diagnostics**: Pre-processes leaf photos using OpenCV and classifies plant pathologies with confidence percentages.
2. **DEMO_MODE Support**: Includes a deterministic mock inference engine (`DEMO_MODE=true`) for instant frontend & backend evaluation prior to full model training.
3. **OpenCV Severity Analyzer**: Estimates leaf lesion area percentage and classifies damage (`Healthy`, `Mild`, `Moderate`, `Severe`).
4. **Weather Risk Engine**: Evaluates ambient temperature, humidity, and rainfall matrix to compute disease transmission risk.
5. **Vetted Recommendation Engine**: Sourced strictly from a verified disease knowledge base; prevents LLM hallucination of chemical dosages.
6. **Gemini AI Agronomist**: Context-aware assistant proxying Google Gemini API for natural language crop advice.
7. **Recharts Data Science Dashboard**: Displays disease prevalence distributions, severity breakdowns, and monthly outbreak trends.
8. **Multilingual i18n**: English and Marathi language toggle support.
9. **Stitch UI/UX Integration**: Fully connected with Stitch design tokens, mobile-optimized screens, and UI component mapping.

---

## Tech Stack

- **Frontend**: React 18, Vite 5, Tailwind CSS 3, React Router v6, Axios, Recharts, Lucide Icons
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL / SQLite, PyJWT, Passlib (Bcrypt)
- **Data Science & ML**: OpenCV, NumPy, Pandas, Scikit-learn, TensorFlow / Keras (MobileNetV2 Transfer Learning)
- **AI Assistant**: Google Gemini API (`google-generativeai`)

---

## Quick Start & Installation Instructions

### 1. Backend Setup & Run

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# (Optional) Set your Gemini API Key in .env
# GEMINI_API_KEY=your_actual_key_here

# Run FastAPI Development Server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The FastAPI backend will run on `http://localhost:8000`. Interactive API docs (Swagger) are available at `http://localhost:8000/docs`.

### 2. Frontend Setup & Run

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Run Vite Development Server
npm run dev
```

The React frontend will run on `http://localhost:3000`.

---

## Demo Login Credentials

- **Default Farmer Account**: `farmer@agroscan.ai` | Password: `password123`
- **Default Admin Account**: `admin@agroscan.ai` | Password: `admin123`

---

## Running Tests

```bash
# Run pytest backend test suite from root
PYTHONPATH=backend pytest tests/
```

---

## Project Directory Structure

```
AgroScan AI/
├── .agents/            # Stitch MCP config & local UI/UX design asset bundle
├── backend/            # FastAPI app, SQLAlchemy models, security, services & endpoints
├── frontend/           # React + Vite + Tailwind CSS + Recharts + i18n
├── ml/                 # Preprocessing, MobileNetV2 transfer learning & inference factory
├── docs/               # System architecture & Stitch UI/UX design mapping specifications
└── tests/              # Pytest backend API integration tests
```

