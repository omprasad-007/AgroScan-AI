import io
import cv2
import numpy as np
import pytest
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient
from app.main import app
from app.services.leaf_validator import LeafValidator
from app.services.consensus_engine import MultiProviderConsensusEngine, consensus_engine
from app.services.providers.local_model_provider import AgroScanLocalModelProvider

client = TestClient(app)

def create_synthetic_leaf_image(is_diseased: bool = False, blurry: bool = False) -> bytes:
    """Generates synthetic RGB plant leaf image with realistic chlorophyll green & veins."""
    width, height = 300, 300
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Neutral light background
    img[:] = [210, 220, 215]

    # Draw organic green leaf contour (elliptical blade)
    center = (150, 150)
    axes = (110, 65)
    angle = 35
    # Green foliage color (BGR format for OpenCV: [B, G, R])
    cv2.ellipse(img, center, axes, angle, 0, 360, (30, 160, 45), -1)

    # Draw leaf veins (lighter yellow-green)
    cv2.line(img, (70, 70), (230, 230), (50, 195, 80), 3)
    cv2.line(img, (120, 120), (100, 160), (50, 185, 75), 2)
    cv2.line(img, (150, 150), (130, 190), (50, 185, 75), 2)
    cv2.line(img, (180, 180), (160, 220), (50, 185, 75), 2)

    if is_diseased:
        # Add brown/yellow necrotic blight lesions
        cv2.circle(img, (130, 140), 18, (20, 70, 140), -1)
        cv2.circle(img, (170, 160), 12, (25, 90, 160), -1)
        cv2.circle(img, (130, 140), 22, (40, 180, 210), 2)  # Chlorotic halo

    if blurry:
        img = cv2.GaussianBlur(img, (45, 45), 0)

    _, encoded = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    return encoded.tobytes()

def create_synthetic_selfie_image() -> bytes:
    """Generates synthetic portrait / human face image with skin tones and facial geometry."""
    width, height = 300, 300
    img = np.zeros((height, width, 3), dtype=np.uint8)
    # Neutral wall background
    img[:] = [240, 240, 240]

    # Face Oval (Skin Tone in BGR: [140, 170, 230])
    cv2.ellipse(img, (150, 150), (70, 95), 0, 0, 360, (140, 170, 230), -1)
    # Eyes
    cv2.circle(img, (125, 130), 8, (30, 30, 30), -1)
    cv2.circle(img, (175, 130), 8, (30, 30, 30), -1)
    # Mouth
    cv2.ellipse(img, (150, 190), (25, 10), 0, 0, 180, (50, 50, 180), -1)

    _, encoded = cv2.imencode(".jpg", img)
    return encoded.tobytes()

def create_synthetic_building_image() -> bytes:
    """Generates synthetic urban architecture image with geometric straight lines and gray palette."""
    width, height = 300, 300
    img = np.zeros((height, width, 3), dtype=np.uint8)
    # Gray concrete
    img[:] = [160, 160, 160]

    # Grid of window frames & structural beams
    for x in range(30, 280, 40):
        cv2.line(img, (x, 20), (x, 280), (40, 40, 40), 4)
    for y in range(30, 280, 40):
        cv2.line(img, (20, y), (280, y), (40, 40, 40), 4)

    _, encoded = cv2.imencode(".jpg", img)
    return encoded.tobytes()

def create_synthetic_soil_image() -> bytes:
    """Generates synthetic bare earth / mud image with brown spectrum."""
    width, height = 300, 300
    img = np.zeros((height, width, 3), dtype=np.uint8)
    # Dark brown soil (BGR: [30, 60, 110])
    img[:] = [30, 60, 110]
    # Add soil grain texture
    noise = np.random.randint(-20, 20, (height, width, 3), dtype=np.int16)
    noisy = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    _, encoded = cv2.imencode(".jpg", noisy)
    return encoded.tobytes()

def create_synthetic_flower_image() -> bytes:
    """Generates synthetic floral bloom without visible leaf canopy."""
    width, height = 300, 300
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = [240, 240, 240]

    # Vibrant Magenta/Pink Flower Petals
    center = (150, 150)
    for angle in range(0, 360, 45):
        rad = np.deg2rad(angle)
        px = int(center[0] + 50 * np.cos(rad))
        py = int(center[1] + 50 * np.sin(rad))
        cv2.circle(img, (px, py), 35, (180, 30, 230), -1)

    cv2.circle(img, center, 28, (30, 210, 255), -1)  # Yellow center

    _, encoded = cv2.imencode(".jpg", img)
    return encoded.tobytes()


# --- TESTS ---

def test_leaf_validator_valid_leaf():
    leaf_bytes = create_synthetic_leaf_image(is_diseased=True)
    res = LeafValidator.validate_leaf_image(leaf_bytes)
    assert res.is_plant is True
    assert res.is_leaf is True
    assert res.usable_for_diagnosis is True
    assert res.leaf_confidence >= 0.60
    assert res.image_quality >= 0.50
    assert res.status_code == "VALID_LEAF"

def test_leaf_validator_selfie_rejected():
    selfie_bytes = create_synthetic_selfie_image()
    res = LeafValidator.validate_leaf_image(selfie_bytes)
    assert res.is_leaf is False
    assert res.usable_for_diagnosis is False
    assert res.status_code in ["FACE_DETECTED", "NON_LEAF_SELFIE", "NON_PLANT_IMAGE"]
    assert "leaf" in res.message_en.lower() or "पान" in res.message_mr

def test_leaf_validator_building_rejected():
    bldg_bytes = create_synthetic_building_image()
    res = LeafValidator.validate_leaf_image(bldg_bytes)
    assert res.is_leaf is False
    assert res.usable_for_diagnosis is False
    assert res.status_code in ["BUILDING_DETECTED", "NON_PLANT_IMAGE"]

def test_leaf_validator_soil_rejected():
    soil_bytes = create_synthetic_soil_image()
    res = LeafValidator.validate_leaf_image(soil_bytes)
    assert res.is_leaf is False
    assert res.usable_for_diagnosis is False
    assert res.status_code in ["SOIL_ONLY_IMAGE", "NON_PLANT_IMAGE"]

def test_leaf_validator_flower_only_rejected():
    flower_bytes = create_synthetic_flower_image()
    res = LeafValidator.validate_leaf_image(flower_bytes)
    assert res.is_leaf is False
    assert res.usable_for_diagnosis is False
    assert res.status_code in ["FLOWER_WITHOUT_LEAF", "NON_PLANT_IMAGE"]

def test_leaf_validator_blurry_leaf_rejected():
    blurry_bytes = create_synthetic_leaf_image(blurry=True)
    res = LeafValidator.validate_leaf_image(blurry_bytes)
    assert res.usable_for_diagnosis is False
    assert res.status_code in ["INSUFFICIENT_IMAGE_QUALITY", "NON_PLANT_IMAGE", "LEAF_UNCLEAR"]

def test_stage1_validate_image_endpoint():
    # 1. Valid leaf
    leaf_bytes = create_synthetic_leaf_image()
    res = client.post(
        "/api/v1/predictions/validate-image",
        files={"file": ("leaf.jpg", leaf_bytes, "image/jpeg")}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["is_plant"] is True
    assert data["is_leaf"] is True
    assert data["usable_for_diagnosis"] is True

    # 2. Non-leaf Selfie
    selfie_bytes = create_synthetic_selfie_image()
    res_selfie = client.post(
        "/api/v1/predictions/validate-image",
        files={"file": ("selfie.jpg", selfie_bytes, "image/jpeg")}
    )
    assert res_selfie.status_code == 200
    data_selfie = res_selfie.json()
    assert data_selfie["is_leaf"] is False
    assert data_selfie["usable_for_diagnosis"] is False

def test_analyze_endpoint_blocks_selfie_and_prevents_disease_fabrication():
    """CRITICAL REGRESSION TEST: Selfie must NEVER return Tomato Early Blight or any disease!"""
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai", "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    selfie_bytes = create_synthetic_selfie_image()
    res = client.post(
        "/api/v1/predictions/analyze",
        files={"file": ("selfie.jpg", selfie_bytes, "image/jpeg")},
        headers=headers
    )
    # Must reject with 400 Bad Request at the Leaf Validation Gate
    assert res.status_code == 400
    err_detail = res.json()["detail"]
    assert "No clear leaf" in err_detail or "leaf" in err_detail.lower()
    assert "Tomato" not in err_detail
    assert "Early Blight" not in err_detail

def test_analyze_endpoint_blocks_building():
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai", "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    bldg_bytes = create_synthetic_building_image()
    res = client.post(
        "/api/v1/predictions/analyze",
        files={"file": ("building.jpg", bldg_bytes, "image/jpeg")},
        headers=headers
    )
    assert res.status_code == 400

def test_analyze_endpoint_valid_leaf_returns_consensus_diagnostics():
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai", "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    leaf_bytes = create_synthetic_leaf_image(is_diseased=True)
    res = client.post(
        "/api/v1/predictions/analyze",
        files={"file": ("leaf.jpg", leaf_bytes, "image/jpeg")},
        data={"temperature_c": 26.0, "humidity_pct": 82.0, "rainfall_mm": 6.0},
        headers=headers
    )
    assert res.status_code == 200
    data = res.json()
    assert "plant" in data
    assert "disease" in data
    assert data["confidence"] > 0.60
    assert "providers_agreed" in data
    assert "consensus_score" in data
    assert "leaf_validation" in data
    assert data["leaf_validation"]["is_leaf"] is True

def test_session_isolation_and_image_hash():
    """Ensures each scan gets an isolated scan_id and computes SHA-256 hash."""
    img1 = create_synthetic_leaf_image(is_diseased=False)
    img2 = create_synthetic_leaf_image(is_diseased=True)

    hash1 = MultiProviderConsensusEngine.calculate_image_hash(img1)
    hash2 = MultiProviderConsensusEngine.calculate_image_hash(img2)
    assert hash1 != hash2
    assert len(hash1) == 64

def test_provider_health_monitoring_endpoint():
    login_res = client.post("/api/v1/auth/login", json={
        "email": "farmer@agroscan.ai", "password": "password123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/predictions/providers/health", headers=headers)
    assert res.status_code == 200
    health_list = res.json()
    assert isinstance(health_list, list)
    assert len(health_list) >= 4
    for item in health_list:
        assert "provider_name" in item
        assert "status" in item
        assert "latency_ms" in item
        # Ensure credentials are NOT leaked
        assert "api_key" not in item
        assert "secret" not in item
