import pytest
from fastapi.testclient import TestClient
from app.main import app, seed_initial_data

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    seed_initial_data()

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "demo_mode" in data

def test_login_demo_user():
    response = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "farmer@agroscan.ai"

def test_weather_risk_simulation():
    response = client.post("/api/v1/weather/risk", json={
        "temperature_c": 26.5,
        "humidity_pct": 85.0,
        "rainfall_mm": 12.0,
        "crop": "Tomato",
        "disease": "Late Blight"
    })
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert data["risk_level"] in ["Low", "Medium", "High", "Critical"]
    assert len(data["contributing_factors"]) > 0

def test_authenticated_dashboard_analytics():
    # Login first
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai",
        "password": "password123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    response = client.get("/api/v1/analytics/dashboard", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.json()
    assert "total_predictions" in data
    assert "disease_distribution" in data
    assert "severity_distribution" in data
