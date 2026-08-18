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
    is_plant, status, reason = PlantDetector.verify_plant_image(blank_bytes)
    assert is_plant is False
    assert status == "NON_PLANT_IMAGE"
    assert "You have not scanned a leaf or plant." in reason

def test_validate_image_endpoint():
    # Test non-plant image validation endpoint
    response = client.post(
        "/api/v1/predictions/validate-image",
        files={"file": ("selfie.jpg", b"NON_PLANT_SELFIE_BYTES", "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_plant"] is False
    assert data["status"] == "NON_PLANT_IMAGE"
    assert "You have not scanned a leaf or plant." in data["message"]

def test_plant_search_catalog():
    response = client.get("/api/v1/plants/search?q=mango")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Mango"
    assert data[0]["scientific_name"] == "Mangifera indica"

def test_geocoding_search_and_reverse():
    # Test geocoding open search
    search_res = client.get("/api/v1/geocoding/search?q=kagal")
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert len(search_data) >= 1

    # Test reverse geocoding
    rev_res = client.get("/api/v1/geocoding/reverse?lat=16.5889&lon=74.3150")
    assert rev_res.status_code == 200
    rev_data = rev_res.json()
    assert "village" in rev_data
    assert rev_data["source"] == "GPS"

def test_chat_multi_turn_distinct_answers():
    # Login
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai", "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Turn 1: Danger/Toxicity question
    res1 = client.post("/api/v1/chat", json={
        "message": "is mango anthracnose fungal disease dangerous to humans or to eat?",
        "manual_plant": "Mango",
        "language": "en"
    }, headers=headers)
    assert res1.status_code == 200
    ans1 = res1.json()["content"]
    session_id = res1.json()["session_id"]
    assert len(ans1) > 20
    assert "dangerous" in ans1.lower() or "safety" in ans1.lower() or "human" in ans1.lower() or "consume" in ans1.lower() or "eat" in ans1.lower() or "harmful" in ans1.lower()

    # Turn 2: Treatment question (building on session)
    res2 = client.post("/api/v1/chat", json={
        "message": "how do I treat this mango disease?",
        "session_id": session_id,
        "manual_plant": "Mango",
        "language": "en"
    }, headers=headers)
    assert res2.status_code == 200
    ans2 = res2.json()["content"]
    assert len(ans2) > 20
    assert "treatment" in ans2.lower() or "spray" in ans2.lower() or "organic" in ans2.lower() or "copper" in ans2.lower() or "neem" in ans2.lower()
    # Ensure Turn 1 and Turn 2 are distinct
    assert ans1 != ans2

    # Turn 3: Spread / Contagion question
    res3 = client.post("/api/v1/chat", json={
        "message": "will this spread to my other mango trees?",
        "session_id": session_id,
        "manual_plant": "Mango",
        "language": "en"
    }, headers=headers)
    assert res3.status_code == 200
    ans3 = res3.json()["content"]
    assert len(ans3) > 20
    assert "spread" in ans3.lower() or "neighbor" in ans3.lower() or "prune" in ans3.lower() or "spore" in ans3.lower() or "transmission" in ans3.lower()
    # All 3 answers must be distinct and specific to their questions
    assert ans3 != ans1
    assert ans3 != ans2

def test_chat_non_agricultural_question():
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai", "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.post("/api/v1/chat", json={
        "message": "what is 2+2?",
        "language": "en"
    }, headers=headers)
    assert res.status_code == 200
    ans = res.json()["content"]
    assert "4" in ans

def test_chat_context_reset_new_crop():
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai", "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Start Rice session
    res = client.post("/api/v1/chat", json={
        "message": "What is the best irrigation method?",
        "manual_plant": "Rice",
        "language": "en"
    }, headers=headers)
    assert res.status_code == 200
    ans = res.json()["content"]
    assert "Rice" in ans or "rice" in ans.lower()
    assert "Mango" not in ans

def test_reverse_geocoding_distinct_locations():
    # Test Location 1: Kolhapur coordinates
    res1 = client.get("/api/v1/geocoding/reverse?lat=16.5889&lon=74.3150")
    assert res1.status_code == 200
    data1 = res1.json()

    # Test Location 2: Bangalore coordinates
    res2 = client.get("/api/v1/geocoding/reverse?lat=12.9716&lon=77.5946")
    assert res2.status_code == 200
    data2 = res2.json()

    # Verify that the two distinct physical coordinates return different location results
    assert data1["latitude"] != data2["latitude"]
    assert data1["district"] != data2["district"] or data1["village"] != data2["village"]

def test_weather_by_coordinates():
    res = client.get("/api/v1/weather/current?lat=18.5204&lon=73.8567")
    assert res.status_code == 200
    data = res.json()
    assert "temperature_c" in data
    assert "humidity_pct" in data
    assert "latitude" in data

def test_user_profile_location_persistence():
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai", "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Update profile location
    patch_res = client.patch("/api/v1/user/profile", json={
        "village": "Baramati",
        "district": "Pune",
        "state": "Maharashtra",
        "pincode": "413102"
    }, headers=headers)
    assert patch_res.status_code == 200, f"Error detail: {patch_res.json()}"
    patched = patch_res.json()
    assert patched["village"] == "Baramati"
    assert patched["district"] == "Pune"

    # Fetch /auth/me and confirm persisted
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["village"] == "Baramati"



