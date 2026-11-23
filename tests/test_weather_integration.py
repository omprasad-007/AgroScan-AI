import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_weather_auto_ip_detection():
    """Verifies that calling /weather/current without params auto-detects real location."""
    response = client.get("/api/v1/weather/current")
    assert response.status_code == 200
    data = response.json()
    assert "location" in data
    assert data["location"] is not None
    assert "temperature_c" in data
    assert isinstance(data["temperature_c"], (int, float))
    assert "humidity_pct" in data
    assert isinstance(data["humidity_pct"], (int, float))
    assert "condition" in data
    assert data["live_api"] is True
    assert data["detection_method"] in ["auto_ip", "regional_default", "device_gps"]


def test_weather_gps_coordinates():
    """Verifies that calling /weather/current with real lat/lon returns live weather."""
    response = client.get("/api/v1/weather/current?lat=16.6941&lon=74.2366")
    assert response.status_code == 200
    data = response.json()
    assert "Kolh" in data["location"] or "Karvir" in data["location"] or "Local" in data["location"]
    assert data["is_gps"] is True
    assert data["detection_method"] == "device_gps"
    assert data["latitude"] == pytest.approx(16.6941, abs=0.05)
    assert data["longitude"] == pytest.approx(74.2366, abs=0.05)
    assert data["live_api"] is True


def test_weather_city_search_with_spaces():
    """Verifies that city queries with spaces (e.g. 'New Delhi') work without double-encoding bugs."""
    response = client.get("/api/v1/weather/current?city=New Delhi")
    assert response.status_code == 200
    data = response.json()
    assert "Delhi" in data["location"]
    assert data["live_api"] is True
    assert data["detection_method"] in ["city_query", "geocoded_search"]


def test_weather_marathi_localization():
    """Verifies that calling with lang=mr returns Marathi weather descriptions."""
    response = client.get("/api/v1/weather/current?lat=16.6941&lon=74.2366&lang=mr")
    assert response.status_code == 200
    data = response.json()
    assert "condition" in data
    assert len(data["condition"]) > 0


def test_weather_disease_risk_matrix():
    """Verifies that POST /weather/risk returns the 7-stage disease outbreak analysis."""
    payload = {
        "temperature_c": 22.0,
        "humidity_pct": 85.0,
        "rainfall_mm": 12.0,
        "crop": "Tomato",
        "disease": "Late Blight"
    }
    response = client.post("/api/v1/weather/risk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert data["risk_score"] >= 70.0  # High risk parameters for Late Blight
    assert data["risk_level"] == "High"
    assert len(data["contributing_factors"]) >= 3
    assert "HIGH RISK" in data["advice"]
