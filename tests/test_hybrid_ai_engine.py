"""
AgroScan AI — Hybrid Intelligence Engine Automated Test Suite
Tests Image Preprocessing, Crop Registry, Confidence Calibration,
Local Hugging Face Label Parsing, Model Registry, Result Normalization,
Orchestrator Workflows, and Data Authorization Isolation.
"""

import io
import pytest
import numpy as np
from PIL import Image, ImageDraw
import torch
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.all_models import User, ScanPrediction, Recommendation
from app.core.security import get_password_hash, create_access_token
from app.services.ai.image_preprocessor import ImagePreprocessor, ImagePreprocessingError
from app.services.ai.crop_registry import CropRegistry, CropSupportStatus
from app.services.ai.confidence_calibrator import ConfidenceCalibrator
from app.services.ai.hf_inference_service import HuggingFaceInferenceService
from app.services.ai.model_registry import ModelRegistry
from app.services.ai.result_normalizer import ResultNormalizer
from app.services.ai.orchestrator import orchestrator


# --- Synthetic Test Fixtures (100% Privacy-Safe & Reproducible) ---

def create_synthetic_leaf_bytes(width=256, height=256, diseased=False):
    """Generates synthetic green leaf texture with chlorophyll spectrum and veins."""
    img = Image.new("RGB", (width, height), color=(25, 30, 20))
    draw = ImageDraw.Draw(img)
    # Draw organic leaf blade
    draw.polygon(
        [(width // 2, 20), (width - 30, height // 2), (width // 2, height - 20), (30, height // 2)],
        fill=(35, 155, 45)
    )
    # Draw central and lateral venation
    draw.line([(width // 2, 20), (width // 2, height - 20)], fill=(70, 190, 80), width=4)
    draw.line([(width // 2, 70), (width - 50, 110)], fill=(65, 180, 75), width=2)
    draw.line([(width // 2, 120), (50, 160)], fill=(65, 180, 75), width=2)

    if diseased:
        # Necrotic blight lesions (brown / yellow chlorotic halos)
        draw.ellipse([width // 2 + 10, height // 2 - 20, width // 2 + 50, height // 2 + 20], fill=(110, 65, 20))
        draw.ellipse([width // 2 - 40, height // 2 + 10, width // 2 - 15, height // 2 + 35], fill=(130, 85, 25))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def create_synthetic_selfie_bytes():
    """Generates synthetic human portrait with skin-tone centroid."""
    img = Image.new("RGB", (256, 256), color=(40, 45, 50))
    draw = ImageDraw.Draw(img)
    # Skin tone oval in YCbCr / HSV skin locus
    draw.ellipse([60, 40, 196, 210], fill=(225, 175, 140))
    # Hair
    draw.rectangle([50, 20, 206, 70], fill=(30, 20, 15))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def create_synthetic_blurry_leaf_bytes():
    """Generates heavily blurred leaf image with low Laplacian variance."""
    arr = np.full((256, 256, 3), [40, 120, 50], dtype=np.uint8)
    img = Image.fromarray(arr)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


# --- Unit Tests: Image Preprocessor ---

def test_image_preprocessor_valid_leaf():
    leaf_bytes = create_synthetic_leaf_bytes()
    pil_img, np_rgb, meta = ImagePreprocessor.decode_and_validate(leaf_bytes)
    assert pil_img is not None
    assert np_rgb.shape == (256, 256, 3)
    assert meta["width"] == 256
    assert meta["height"] == 256
    assert meta["channels"] == 3


def test_image_preprocessor_empty_or_truncated():
    with pytest.raises(ImagePreprocessingError):
        ImagePreprocessor.decode_and_validate(b"short_bytes")


def test_image_preprocessor_low_resolution():
    tiny_img = Image.new("RGB", (64, 64), color=(0, 255, 0))
    buf = io.BytesIO()
    tiny_img.save(buf, format="JPEG")
    with pytest.raises(ImagePreprocessingError, match="below minimum"):
        ImagePreprocessor.decode_and_validate(buf.getvalue())


def test_image_preprocessor_tensor_generation():
    leaf_bytes = create_synthetic_leaf_bytes()
    pil_img, _, _ = ImagePreprocessor.decode_and_validate(leaf_bytes)
    tensor = ImagePreprocessor.prepare_inference_tensor(pil_img, target_size=(224, 224))
    assert tensor.shape == (1, 3, 224, 224)
    assert tensor.dtype == torch.float32


# --- Unit Tests: Crop Registry ---

def test_crop_registry_supported_crops():
    status, profile = CropRegistry.check_support("tomato")
    assert status == CropSupportStatus.SUPPORTED
    assert profile is not None
    assert profile.common_name == "Tomato"
    assert "neghani/plantvillage-mobilenetv2" in profile.supported_model_ids

    status, profile = CropRegistry.check_support("potato")
    assert status == CropSupportStatus.SUPPORTED

    status, profile = CropRegistry.check_support("corn")
    assert status == CropSupportStatus.SUPPORTED


def test_crop_registry_partially_supported_crops():
    status, profile = CropRegistry.check_support("mango")
    assert status == CropSupportStatus.PARTIALLY_SUPPORTED
    assert profile.common_name == "Mango"
    assert profile.limitations is not None

    status, profile = CropRegistry.check_support("cotton")
    assert status == CropSupportStatus.PARTIALLY_SUPPORTED

    status, profile = CropRegistry.check_support("rice")
    assert status == CropSupportStatus.PARTIALLY_SUPPORTED


def test_crop_registry_unsupported_crop():
    status, profile = CropRegistry.check_support("tea")
    assert status == CropSupportStatus.UNSUPPORTED
    assert profile is not None
    assert profile.common_name == "Tea"

    status, profile = CropRegistry.check_support("coffee")
    assert status == CropSupportStatus.UNSUPPORTED


def test_crop_registry_unknown_crop():
    status, profile = CropRegistry.check_support("plastic_chair")
    assert status == CropSupportStatus.UNKNOWN_CROP
    assert profile is None


def test_crop_registry_aliases():
    status, profile = CropRegistry.check_support("tamatar")
    assert status == CropSupportStatus.SUPPORTED
    assert profile.id == "tomato"

    status, profile = CropRegistry.check_support("aloo")
    assert status == CropSupportStatus.SUPPORTED
    assert profile.id == "potato"

    status, profile = CropRegistry.check_support("maize")
    assert status == CropSupportStatus.SUPPORTED
    assert profile.id == "corn"


# --- Unit Tests: Confidence Calibration ---

def test_confidence_calibration_temperature_scaling():
    # Simulated logits for 3 classes
    logits = torch.tensor([[4.0, 1.0, 0.5]])
    scaled_probs = ConfidenceCalibrator.apply_temperature_scaling(logits, temperature=0.8845)
    assert scaled_probs.shape == (1, 3)
    assert torch.isclose(scaled_probs.sum(), torch.tensor(1.0))
    # Top class probability should be sharpened
    assert float(scaled_probs[0, 0]) > 0.85


def test_confidence_calibration_interpretation():
    assert ConfidenceCalibrator.interpret_confidence(0.85) == "HIGH_CONFIDENCE"
    assert ConfidenceCalibrator.interpret_confidence(0.60) == "MODERATE_CONFIDENCE"
    assert ConfidenceCalibrator.interpret_confidence(0.35) == "LOW_CONFIDENCE_UNCERTAIN"


def test_model_agreement_evaluation():
    # Case 1: Unanimous agreement
    preds = [
        {"status": "success", "disease_code": "tomato_early_blight", "confidence": 0.90, "is_healthy": False},
        {"status": "success", "disease_code": "tomato_early_blight", "confidence": 0.88, "is_healthy": False}
    ]
    status, score, note = ConfidenceCalibrator.evaluate_model_agreement(preds)
    assert status == "UNANIMOUS"
    assert score == 1.0
    assert note is None

    # Case 2: Conflicting assessment (healthy vs diseased)
    conflicting = [
        {"status": "success", "disease_code": "healthy_leaf", "confidence": 0.92, "is_healthy": True},
        {"status": "success", "disease_code": "tomato_early_blight", "confidence": 0.85, "is_healthy": False}
    ]
    status, score, note = ConfidenceCalibrator.evaluate_model_agreement(conflicting)
    assert status == "CONFLICTING"
    assert "disagreement" in note.lower()


# --- Unit Tests: Local Model Label Parser ---

def test_plantvillage_label_parser():
    crop, disease, code, is_healthy = HuggingFaceInferenceService.parse_plantvillage_label("Tomato___Tomato_Yellow_Leaf_Curl_Virus")
    assert crop == "Tomato"
    assert "Yellow Leaf Curl" in disease
    assert is_healthy is False
    assert "yellow_leaf_curl" in code

    crop, disease, code, is_healthy = HuggingFaceInferenceService.parse_plantvillage_label("Apple___healthy")
    assert crop == "Apple"
    assert is_healthy is True
    assert code == "healthy_leaf"


# --- Unit Tests: Model Registry Health ---

def test_model_registry_health_status():
    health = ModelRegistry.get_health_status()
    assert len(health) >= 2
    model_ids = [m["model_id"] for m in health]
    assert "neghani/plantvillage-mobilenetv2" in model_ids
    assert "rodynaemad/plant-disease-dinov2-small" in model_ids


# --- Unit Tests: Result Normalizer ---

def test_result_normalizer_schema_compliance():
    norm = ResultNormalizer.normalize_diagnosis(
        scan_id="scan_test_001",
        status="DISEASE_DETECTED",
        image_validation={"status_code": "VALID_LEAF", "is_leaf": True, "leaf_confidence": 0.92},
        plant_name="Tomato",
        scientific_name="Solanum lycopersicum",
        crop_profile=CropRegistry.get_crop("tomato"),
        disease_name="Tomato Early Blight",
        disease_code="tomato_early_blight",
        confidence=0.885,
        is_healthy=False,
        model_predictions=[{"model_id": "neghani/plantvillage-mobilenetv2", "confidence": 0.885}],
        provider_predictions=[],
        agreement_status="SINGLE_SOURCE",
        consensus_score=0.885
    )
    assert norm["scan_id"] == "scan_test_001"
    assert norm["status"] == "DISEASE_DETECTED"
    assert norm["crop_support_status"] == "SUPPORTED"
    assert norm["disease_category"] == "Fungal Blight"
    assert "organic_treatment" in norm["recommendation"]
    assert "chemical_treatment" in norm["recommendation"]
    assert "disclaimer" in norm["recommendation"]
    assert len(norm["recommended_next_steps"]) >= 2


# --- Integration Tests: Orchestrator Workflows ---

def test_orchestrator_rejects_selfie():
    import asyncio
    selfie_bytes = create_synthetic_selfie_bytes()
    res = asyncio.run(orchestrator.orchestrate_scan(
        image_bytes=selfie_bytes,
        scan_id="scan_selfie_01",
        target_crop="tomato"
    ))
    assert res["status"] in ["INVALID_IMAGE", "POOR_IMAGE_QUALITY"]
    assert res["usable_for_diagnosis"] is False
    assert "leaf" in res["message"].lower() or "पान" in res["message"]


def test_orchestrator_unsupported_crop():
    import asyncio
    leaf_bytes = create_synthetic_leaf_bytes()
    res = asyncio.run(orchestrator.orchestrate_scan(
        image_bytes=leaf_bytes,
        scan_id="scan_unsupported_01",
        target_crop="tea"
    ))
    assert res["status"] == "UNSUPPORTED_CROP"
    assert res["crop_support_status"] == "UNSUPPORTED"
    assert res["plant"] == "Tea"
    # Never fabricates a fake disease
    assert res["disease_code"] == "unsupported_crop"


# --- API Integration & Security Authorization Tests ---

def test_delete_authorization_protection():
    client = TestClient(app)
    db = SessionLocal()

    try:
        # Create user A and user B
        user_a = db.query(User).filter(User.email == "user_a_test@agroscan.ai").first()
        if not user_a:
            user_a = User(email="user_a_test@agroscan.ai", full_name="User A", hashed_password=get_password_hash("pass123"))
            db.add(user_a)
            db.commit()
            db.refresh(user_a)

        user_b = db.query(User).filter(User.email == "user_b_test@agroscan.ai").first()
        if not user_b:
            user_b = User(email="user_b_test@agroscan.ai", full_name="User B", hashed_password=get_password_hash("pass123"))
            db.add(user_b)
            db.commit()
            db.refresh(user_b)

        # Create scan owned by user A
        scan_a = ScanPrediction(
            id="scan_owned_by_a",
            user_id=user_a.id,
            image_path="/uploads/test_a.jpg",
            crop_detected="Tomato",
            disease_name="Tomato Early Blight",
            disease_code="tomato_early_blight",
            confidence_score=0.90
        )
        db.merge(scan_a)
        db.commit()

        # Token for user B
        token_b = create_access_token({"sub": user_b.id, "email": user_b.email, "role": "farmer"})

        # User B attempts to delete User A's scan -> MUST return 403 Forbidden
        res_forbidden = client.delete(
            "/api/v1/predictions/scan_owned_by_a",
            headers={"Authorization": f"Bearer {token_b}"}
        )
        assert res_forbidden.status_code == 403
        assert "permission" in res_forbidden.json()["detail"].lower()

        # Unauthenticated guest attempts to delete User A's scan -> MUST return 403 Forbidden
        res_guest = client.delete("/api/v1/predictions/scan_owned_by_a")
        assert res_guest.status_code == 403

        # User A deletes their own scan -> SUCCESS
        token_a = create_access_token({"sub": user_a.id, "email": user_a.email, "role": "farmer"})
        res_success = client.delete(
            "/api/v1/predictions/scan_owned_by_a",
            headers={"Authorization": f"Bearer {token_a}"}
        )
        assert res_success.status_code == 200
        assert res_success.json()["status"] == "success"

    finally:
        db.close()
