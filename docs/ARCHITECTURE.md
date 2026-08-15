# AgroScan AI — Architecture Specification

## Overview
**AgroScan AI** is a smart agriculture platform designed for plant disease detection, severity analysis, weather-based disease risk forecasting, and AI-assisted agronomy guidance.

## Core Stack
- **Frontend**: React, Vite, Tailwind CSS, React Router DOM, Axios, Recharts
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL, PyJWT, Passlib
- **Data Science / ML**: OpenCV, NumPy, Pandas, TensorFlow/Keras, BaseDiseasePredictor (Factory Pattern)
- **AI Assistant**: Google Gemini API via Backend Proxy
- **Mode**: `DEMO_MODE` supported for seamless UI/UX testing prior to model training.

## Directory Structure
```
AgroScan AI/
├── frontend/     # React + Vite + Tailwind CSS
├── backend/      # FastAPI REST API + SQLAlchemy ORM
├── ml/           # Model pipeline, preprocessors & predictors
├── database/     # Alembic migrations & seed data
├── docs/         # System architecture & API docs
└── tests/        # Pytest unit & integration test suites
```

## System Workflow
1. **Dashboard**: Summary metrics, recent scan history, weather risk widget.
2. **Scan Leaf**: Image uploader / camera capture / sample leaf picker (Demo Mode).
3. **AI Analysis**: OpenCV image pre-processing & lesion contour area segmentation.
4. **Disease Identification**: Model prediction with confidence percentage.
5. **Severity Analysis**: Quantitative leaf damage % estimation.
6. **Weather Risk**: Temp & humidity matrix disease risk evaluation.
7. **Treatment & Assistant**: Organic/chemical remedies & interactive Gemini AI agronomy advisor.
8. **History & Analytics**: Time-series outbreak tracking with Recharts.
