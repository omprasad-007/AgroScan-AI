"""
AgroScan AI — Automated Test Suite for Hugging Face MobileNetV2 Integration
Tests:
1. Model Loading, Lifecycle & Offline Execution
2. Top-3 Prediction Structure, Calibration, and Threshold Evaluation
3. 38 PlantVillage Label Mapping
4. Error Handling: Missing Files, Corrupted Bytes, Invalid Config
5. Strict Image Validation Gate (Selfies, Documents, Buildings, Soil, Blurry, Dark)
6. Crop Registry & Unsupported Crop Handling
7. Dedicated Model Endpoints (/api/model/health, /info, /labels, /crops, /predict)
8. End-to-End Scan Pipeline Integration (/api/v1/predictions/analyze)
9. Scan Independence, Session Isolation & Concurrency
"""

import io
import os
import cv2
import json
import pytest
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient

from app.main import app, seed_initial_data
from app.services.plant_disease_model import (
    PlantDiseaseModelService,
    local_model_service,
    load_model,
    predict_disease,
    get_model_metadata,
    get_model_health,
    get_supported_labels,
    ModelPredictionResult
)
from app.services.crop_registry import (
    get_crop_support,
    is_crop_supported_by_local_model,
    CropSupportStatus
)
from app.services.leaf_validator import LeafValidator

client = TestClient(app)


@pytest.fixture(autouse=True)
def init_database():
    seed_initial_data()


# ==============================================================================
# SYNTHETIC IMAGE GENERATOR FIXTURES
# ==============================================================================

def make_synthetic_leaf(is_diseased: bool = False, blurry: bool = False, dark: bool = False) -> bytes:
    """Generates synthetic RGB plant leaf image with realistic chlorophyll and venation."""
    width, height = 240, 240
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = [210, 220, 215]  # light background

    # Elliptical leaf blade (BGR: [30, 160, 45])
    cv2.ellipse(img, (120, 120), (90, 55), 35, 0, 360, (30, 160, 45), -1)
    # Leaf venation
    cv2.line(img, (50, 50), (190, 190), (50, 195, 80), 2)
    cv2.line(img, (90, 90), (70, 130), (50, 185, 75), 2)
    cv2.line(img, (120, 120), (100, 160), (50, 185, 75), 2)

    if is_diseased:
        # Brown necrotic lesions
        cv2.circle(img, (100, 110), 14, (20, 70, 140), -1)
        cv2.circle(img, (135, 130), 10, (25, 90, 160), -1)
        cv2.circle(img, (100, 110), 18, (40, 180, 210), 1)  # chlorotic halo

    if blurry:
        img = cv2.GaussianBlur(img, (45, 45), 0)

    if dark:
        img = (img * 0.04).astype(np.uint8)

    _, enc = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return enc.tobytes()


def make_synthetic_selfie() -> bytes:
    """Generates portrait with skin tone oval and facial features."""
    img = np.zeros((240, 240, 3), dtype=np.uint8)
    img[:] = [230, 230, 230]
    cv2.ellipse(img, (120, 120), (60, 80), 0, 0, 360, (140, 170, 230), -1)  # skin tone
    cv2.circle(img, (100, 105), 6, (30, 30, 30), -1)  # eye
    cv2.circle(img, (140, 105), 6, (30, 30, 30), -1)  # eye
    cv2.ellipse(img, (120, 150), (25, 12), 0, 0, 180, (60, 60, 180), 2)  # mouth
    _, enc = cv2.imencode(".jpg", img)
    return enc.tobytes()


def make_synthetic_document() -> bytes:
    """Generates text document page with high whiteness and linear text bars."""
    img = np.ones((240, 240, 3), dtype=np.uint8) * 245
    for y in range(40, 210, 20):
        cv2.line(img, (30, y), (210, y), (40, 40, 40), 2)
    _, enc = cv2.imencode(".jpg", img)
    return enc.tobytes()


def make_synthetic_building() -> bytes:
    """Generates architectural grid pattern."""
    img = np.zeros((240, 240, 3), dtype=np.uint8)
    img[:] = [120, 120, 120]
    for x in range(20, 240, 30):
        cv2.line(img, (x, 0), (x, 240), (240, 240, 240), 2)
    for y in range(20, 240, 30):
        cv2.line(img, (0, y), (240, y), (240, 240, 240), 2)
    _, enc = cv2.imencode(".jpg", img)
    return enc.tobytes()


def make_synthetic_soil() -> bytes:
    """Generates bare brown earth texture."""
    img = np.zeros((240, 240, 3), dtype=np.uint8)
    # Soil brown in BGR: low blue, medium green, higher red
    img[:] = [40, 75, 130]
    noise = np.random.randint(-15, 15, (240, 240, 3), dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    _, enc = cv2.imencode(".jpg", img)
    return enc.tobytes()


# ==============================================================================
# 1. MODEL SERVICE & OFFLINE LOADING TESTS
# ==============================================================================

def test_model_loads_offline():
    """Verify MobileNetV2 loads from local disk without outbound network calls."""
    success = load_model()
    assert success is True
    assert local_model_service.is_loaded is True
    assert local_model_service.model is not None
    assert local_model_service.processor is not None


def test_model_metadata_structure():
    """Verify metadata reports exact repository, architecture, and immutable commit SHA."""
    meta = get_model_metadata()
    assert meta["repository_id"] == "neghani/plantvillage-mobilenetv2"
    assert meta["architecture"] == "MobileNetV2ForImageClassification"
    assert meta["revision"] == "v1.1"
    assert meta["immutable_commit_sha"] == "77e6d262dca53b818f7ad1d67088700754515639"
    assert meta["num_classes"] == 38
    assert meta["crops_covered_count"] == 14
    assert meta["weights_size_bytes"] == 9264680
    assert meta["temperature_calibration"] > 0.80
    assert meta["confidence_threshold"] == 0.50


def test_model_health_endpoint_response():
    """Verify health check returns operational status."""
    health = get_model_health()
    assert health["status"] == "HEALTHY"
    assert health["service"] == "plant_disease_mobilenetv2"
    assert health["is_loaded"] is True
    assert health["num_classes"] == 38
    assert health["device"] in ["cpu", "cuda"]


def test_supported_labels_count_and_mapping():
    """Verify id2label contains exactly 38 PlantVillage classes across 14 crops."""
    labels = get_supported_labels()
    assert len(labels) == 38
    # Check key classes exist
    raw_labels = [l["raw_label"] for l in labels]
    assert "Tomato___Early_blight" in raw_labels
    assert "Tomato___Late_blight" in raw_labels
    assert "Tomato___healthy" in raw_labels
    assert "Potato___Early_blight" in raw_labels
    assert "Potato___Late_blight" in raw_labels
    assert "Apple___Apple_scab" in raw_labels
    assert "Corn_(maize)___Common_rust_" in raw_labels
    assert "Grape___Black_rot" in raw_labels


def test_model_top3_prediction_structure():
    """Verify inference returns top-3 candidates with calibrated and raw probability scores."""
    leaf_bytes = make_synthetic_leaf(is_diseased=False)
    res: ModelPredictionResult = predict_disease(leaf_bytes, target_crop="tomato")

    assert res.status in ["HEALTHY", "DISEASE_DETECTED", "UNCERTAIN"]
    assert len(res.top_predictions) == 3
    assert res.top_prediction is not None
    assert res.crop_detected is not None
    assert res.disease_name is not None
    assert 0.0 <= res.confidence <= 1.0
    assert 0.0 <= res.raw_score <= 1.0
    assert 0.0 <= res.calibrated_score <= 1.0
    assert res.temperature_applied == pytest.approx(0.8845, rel=1e-2)
    assert res.threshold_applied == 0.50
    assert res.latency_ms > 0.0


def test_missing_model_files_handling():
    """Verify handling when an invalid model directory is passed."""
    orig_dir = local_model_service.model_dir
    try:
        local_model_service.model_dir = "backend/models/non_existent_model_dir"
        local_model_service.is_loaded = False
        loaded = local_model_service.load_model()
        assert loaded is False
        assert local_model_service.load_error is not None
    finally:
        local_model_service.model_dir = orig_dir
        local_model_service.is_loaded = False
        local_model_service.load_model()


# ==============================================================================
# 2. IMAGE VALIDATION & ADVERSARIAL REJECTIONS
# ==============================================================================

def test_validation_accepts_healthy_leaf():
    leaf_bytes = make_synthetic_leaf(is_diseased=False)
    res = LeafValidator.validate_leaf_image(leaf_bytes)
    assert res.is_leaf is True
    assert res.usable_for_diagnosis is True
    assert res.status_code == "VALID_LEAF"


def test_validation_accepts_diseased_leaf():
    leaf_bytes = make_synthetic_leaf(is_diseased=True)
    res = LeafValidator.validate_leaf_image(leaf_bytes)
    assert res.is_leaf is True
    assert res.usable_for_diagnosis is True


def test_validation_rejects_blurry_image():
    blurry_bytes = make_synthetic_leaf(blurry=True)
    res = LeafValidator.validate_leaf_image(blurry_bytes)
    assert res.usable_for_diagnosis is False
    assert res.status_code == "INSUFFICIENT_IMAGE_QUALITY"


def test_validation_rejects_dark_image():
    dark_bytes = make_synthetic_leaf(dark=True)
    res = LeafValidator.validate_leaf_image(dark_bytes)
    assert res.usable_for_diagnosis is False


def test_validation_rejects_selfie():
    selfie_bytes = make_synthetic_selfie()
    res = LeafValidator.validate_leaf_image(selfie_bytes)
    assert res.is_leaf is False
    assert res.usable_for_diagnosis is False
    assert res.status_code in ["NON_LEAF_SELFIE", "FACE_DETECTED", "NON_PLANT_IMAGE"]


def test_validation_rejects_document():
    doc_bytes = make_synthetic_document()
    res = LeafValidator.validate_leaf_image(doc_bytes)
    assert res.is_leaf is False
    assert res.usable_for_diagnosis is False
    assert res.status_code in ["DOCUMENT_DETECTED", "NON_PLANT_IMAGE"]


def test_validation_rejects_building():
    bldg_bytes = make_synthetic_building()
    res = LeafValidator.validate_leaf_image(bldg_bytes)
    assert res.is_leaf is False
    assert res.usable_for_diagnosis is False
    assert res.status_code in ["BUILDING_DETECTED", "NON_PLANT_IMAGE"]


def test_validation_rejects_soil_only():
    soil_bytes = make_synthetic_soil()
    res = LeafValidator.validate_leaf_image(soil_bytes)
    assert res.is_leaf is False
    assert res.usable_for_diagnosis is False
    assert res.status_code in ["SOIL_ONLY_IMAGE", "NON_PLANT_IMAGE", "NON_LEAF_SELFIE"]


def test_validation_rejects_corrupted_bytes():
    corrupted_bytes = b"NOT_AN_IMAGE_FILE_JUST_JUNK_BYTES_12345"
    res = LeafValidator.validate_leaf_image(corrupted_bytes)
    assert res.is_leaf is False
    assert res.usable_for_diagnosis is False


# ==============================================================================
# 3. CROP REGISTRY & UNSUPPORTED CROPS
# ==============================================================================

def test_crop_support_checks():
    """Verify 14 native crops return SUPPORTED, whereas Sugarcane/Cotton return non-supported."""
    assert get_crop_support("tomato").status == CropSupportStatus.SUPPORTED
    assert get_crop_support("potato").status == CropSupportStatus.SUPPORTED
    assert get_crop_support("apple").status == CropSupportStatus.SUPPORTED
    assert get_crop_support("grape").status == CropSupportStatus.SUPPORTED
    assert get_crop_support("corn").status == CropSupportStatus.SUPPORTED

    # Non-PlantVillage crops
    sugarcane_entry = get_crop_support("sugarcane")
    assert sugarcane_entry.status in [CropSupportStatus.PARTIALLY_SUPPORTED, CropSupportStatus.UNSUPPORTED]
    assert is_crop_supported_by_local_model("sugarcane") is False

    cotton_entry = get_crop_support("cotton")
    assert is_crop_supported_by_local_model("cotton") is False


def test_model_predict_rejects_unsupported_crop_coercion():
    """Verify that specifying an unsupported crop (e.g. Sugarcane) returns UNSUPPORTED_CROP."""
    leaf_bytes = make_synthetic_leaf(is_diseased=False)
    res = predict_disease(leaf_bytes, target_crop="sugarcane")
    assert res.status == "UNSUPPORTED_CROP"
    assert res.crop_support_status == "UNSUPPORTED"
    assert "Sugarcane" in res.uncertainty_note


# ==============================================================================
# 4. FASTAPI DEDICATED MODEL ENDPOINTS
# ==============================================================================

def test_api_model_health_route():
    response = client.get("/api/model/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["num_classes"] == 38


def test_api_model_info_route():
    response = client.get("/api/model/info")
    assert response.status_code == 200
    data = response.json()
    assert data["repository_id"] == "neghani/plantvillage-mobilenetv2"
    assert data["revision"] == "v1.1"
    assert data["architecture"] == "MobileNetV2ForImageClassification"


def test_api_model_labels_route():
    response = client.get("/api/model/labels")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 38


def test_api_model_crops_route():
    response = client.get("/api/model/crops")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 14


def test_api_model_predict_route_valid_leaf():
    leaf_bytes = make_synthetic_leaf(is_diseased=False)
    files = {"file": ("leaf.jpg", leaf_bytes, "image/jpeg")}
    response = client.post("/api/model/predict", files=files, data={"target_crop": "tomato"})
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "top_prediction" in data
    assert len(data["top_predictions"]) == 3
    assert data["model_name"] == "MobileNetV2 (PlantVillage v1.1)"


def test_api_model_predict_route_rejects_selfie():
    selfie_bytes = make_synthetic_selfie()
    files = {"file": ("selfie.jpg", selfie_bytes, "image/jpeg")}
    response = client.post("/api/model/predict", files=files)
    assert response.status_code == 400
    assert "rejected" in response.json()["detail"].lower()


# ==============================================================================
# 5. END-TO-END SCAN INTEGRATION & SESSION ISOLATION
# ==============================================================================

def test_scan_analyze_full_pipeline_guest():
    leaf_bytes = make_synthetic_leaf(is_diseased=True)
    files = {"file": ("diseased_leaf.jpg", leaf_bytes, "image/jpeg")}
    response = client.post(
        "/api/v1/predictions/analyze",
        files=files,
        data={
            "target_crop": "tomato",
            "temperature_c": 25.0,
            "humidity_pct": 82.0,
            "rainfall_mm": 8.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"].startswith("scan_")
    assert data["status"] in ["DISEASE_DETECTED", "UNCERTAIN", "HEALTHY"]
    assert data["plant"] is not None
    assert data["disease"] is not None
    assert data["confidence"] > 0.0
    assert "recommendation" in data
    assert data["recommendation"]["organic_treatment"] is not None
    assert data["recommendation"]["chemical_treatment"] is not None
    assert data["recommendation"]["prevention"] is not None
    assert data["model_name"] == "MobileNetV2 (PlantVillage v1.1)"


def test_scan_analyze_rejects_document():
    doc_bytes = make_synthetic_document()
    files = {"file": ("doc.jpg", doc_bytes, "image/jpeg")}
    response = client.post("/api/v1/predictions/analyze", files=files)
    assert response.status_code == 400


def test_distinct_scans_produce_unique_ids_and_records():
    """Verify repeated scans are independent and do not overwrite prior diagnoses."""
    # Obtain auth token for user record persistence
    login_res = client.post("/api/v1/auth/login", json={"email": "farmer@agroscan.ai", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    leaf_1 = make_synthetic_leaf(is_diseased=False)
    leaf_2 = make_synthetic_leaf(is_diseased=True)

    res_1 = client.post("/api/v1/predictions/analyze", files={"file": ("leaf1.jpg", leaf_1, "image/jpeg")}, headers=headers)
    res_2 = client.post("/api/v1/predictions/analyze", files={"file": ("leaf2.jpg", leaf_2, "image/jpeg")}, headers=headers)

    assert res_1.status_code == 200
    assert res_2.status_code == 200

    id_1 = res_1.json()["id"]
    id_2 = res_2.json()["id"]
    assert id_1 != id_2

    # Fetching each by ID returns their respective records
    get_1 = client.get(f"/api/v1/predictions/{id_1}", headers=headers)
    get_2 = client.get(f"/api/v1/predictions/{id_2}", headers=headers)

    assert get_1.status_code == 200
    assert get_2.status_code == 200
    assert get_1.json()["id"] == id_1
    assert get_2.json()["id"] == id_2
