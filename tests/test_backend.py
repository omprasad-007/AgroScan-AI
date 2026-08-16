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

def test_firebase_login_privilege_escalation_prevented():
    response = client.post("/api/v1/auth/firebase-login", json={
        "email": "attacker_admin@agroscan.ai",
        "full_name": "Attacker Admin User",
        "city": "Pune"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "farmer"

def test_security_headers():
    response = client.get("/api/v1/health")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"

def test_corrupt_image_upload_shield():
    # Login first
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai",
        "password": "password123"
    })
    token = login_res.json()["access_token"]

    corrupt_bytes = b"NOT_A_REAL_IMAGE_FILE_HEADER"
    response = client.post(
        "/api/v1/predictions/analyze",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("fake.jpg", corrupt_bytes, "image/jpeg")}
    )
    assert response.status_code == 400
    assert "Please capture a clearer image" in response.json()["detail"]

def test_pbkdf2_password_hashing_security():
    from app.core.security import get_password_hash, verify_password
    pwd = "super_secure_farmer_password_2026"
    hashed = get_password_hash(pwd)
    assert hashed.startswith("pbkdf2_sha256$")
    assert verify_password(pwd, hashed) is True
    assert verify_password("wrong_pass", hashed) is False

def test_idor_protection_recommendation():
    # Login as farmer
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai",
        "password": "password123"
    })
    token = login_res.json()["access_token"]

    # Attempt to query non-existent or other user's prediction ID
    response = client.get(
        "/api/v1/recommendations/invalid_or_unauthorized_pred_id",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404

def test_plant_verification_detector():
    from app.services.plant_detector import PlantDetector
    # Blank/non-vegetation bytes
    blank_bytes = b"NON_PLANT_BYTES_TEST"
    is_plant, conf, reason = PlantDetector.verify_plant_image(blank_bytes)
    assert is_plant is False
    assert "Invalid image" in reason or "doesn't appear" in reason


