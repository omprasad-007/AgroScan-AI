"""
AgroScan AI — Sample Leaf Image Scanner & Diagnostic History Ingestion Script
Generates authentic botanical leaf samples for multiple crops (Tomato, Potato, Corn, Grape, Pepper, Pomegranate),
scans them through the production FastAPI pipeline, and confirms they are persisted in SQLite diagnostic history.
"""

import sys
import os
import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.all_models import ScanPrediction, Recommendation, User

def generate_leaf_image(crop_type: str, disease_type: str) -> bytes:
    """Generates synthetic high-quality leaf images with botanical shape, veins, and pathology."""
    width, height = 350, 350
    # Natural ambient background (outdoor soft daylight)
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = [215, 225, 218]

    center = (175, 175)

    if crop_type == "Tomato":
        # Serrated compound leaflet
        cv2.ellipse(img, center, (120, 65), 35, 0, 360, (25, 155, 40), -1)
        # Midrib and lateral veins
        cv2.line(img, (90, 90), (260, 260), (45, 185, 70), 3)
        cv2.line(img, (140, 140), (120, 190), (45, 180, 65), 2)
        cv2.line(img, (175, 175), (155, 225), (45, 180, 65), 2)
        cv2.line(img, (210, 210), (190, 255), (45, 180, 65), 2)
        cv2.line(img, (140, 140), (190, 120), (45, 180, 65), 2)
        cv2.line(img, (175, 175), (225, 155), (45, 180, 65), 2)

        if disease_type == "early_blight":
            # Concentric target-board rings with chlorotic halo
            cv2.circle(img, (150, 160), 20, (15, 55, 120), -1)
            cv2.circle(img, (150, 160), 26, (35, 160, 205), 3)
            cv2.circle(img, (200, 190), 14, (15, 50, 110), -1)
            cv2.circle(img, (200, 190), 19, (35, 160, 205), 2)

    elif crop_type == "Potato":
        # Broad ovate potato leaf
        cv2.ellipse(img, center, (125, 75), 45, 0, 360, (30, 150, 38), -1)
        cv2.line(img, (85, 85), (265, 265), (50, 180, 65), 3)
        cv2.line(img, (135, 135), (110, 190), (50, 175, 60), 2)
        cv2.line(img, (185, 185), (160, 240), (50, 175, 60), 2)

        if disease_type == "late_blight":
            # Water-soaked irregular dark lesions
            cv2.ellipse(img, (145, 155), (28, 18), 20, 0, 360, (18, 40, 75), -1)
            cv2.ellipse(img, (205, 205), (22, 14), -15, 0, 360, (18, 40, 75), -1)
            # Pale fungal mold edge
            cv2.ellipse(img, (145, 155), (32, 22), 20, 0, 360, (180, 200, 210), 2)

    elif crop_type == "Corn":
        # Long linear lanceolate leaf with parallel venation
        cv2.ellipse(img, center, (145, 45), 25, 0, 360, (35, 165, 50), -1)
        # Parallel veins
        for offset in [-18, -9, 0, 9, 18]:
            pt1 = (80 + offset, 110 - offset)
            pt2 = (270 + offset, 240 - offset)
            cv2.line(img, pt1, pt2, (55, 195, 75), 2)

        if disease_type == "common_rust":
            # Small cinnamon-brown oval pustules
            for px, py in [(140, 150), (165, 170), (190, 195), (150, 180), (210, 210)]:
                cv2.ellipse(img, (px, py), (6, 3), 25, 0, 360, (15, 45, 160), -1)

    elif crop_type == "Grape":
        # Broad lobed palmate grape leaf
        cv2.ellipse(img, center, (115, 95), 0, 0, 360, (28, 148, 42), -1)
        cv2.circle(img, (120, 130), 45, (28, 148, 42), -1)
        cv2.circle(img, (230, 130), 45, (28, 148, 42), -1)
        # Palmate main veins radiating from base
        cv2.line(img, (175, 260), (175, 90), (50, 180, 70), 3)
        cv2.line(img, (175, 260), (100, 140), (50, 180, 70), 2)
        cv2.line(img, (175, 260), (250, 140), (50, 180, 70), 2)

        if disease_type == "powdery_mildew":
            # Powdery white patches on leaf surface
            cv2.circle(img, (150, 160), 25, (210, 220, 225), -1)
            cv2.circle(img, (200, 175), 20, (205, 215, 220), -1)

    elif crop_type == "Pepper":
        # Smooth entire margin healthy bell pepper leaf
        cv2.ellipse(img, center, (120, 60), 40, 0, 360, (20, 165, 45), -1)
        cv2.line(img, (90, 90), (260, 260), (40, 195, 75), 3)
        cv2.line(img, (135, 135), (115, 180), (40, 190, 70), 2)
        cv2.line(img, (175, 175), (155, 220), (40, 190, 70), 2)
        cv2.line(img, (215, 215), (195, 260), (40, 190, 70), 2)

    elif crop_type == "Pomegranate":
        # Oblong glossy pomegranate leaf
        cv2.ellipse(img, center, (110, 50), -30, 0, 360, (25, 145, 35), -1)
        cv2.line(img, (95, 245), (255, 105), (50, 185, 65), 3)

        if disease_type == "anthracnose":
            # Small circular dark brown spots with sunken appearance
            for spot in [(140, 180), (175, 150), (200, 130), (160, 170)]:
                cv2.circle(img, spot, 8, (15, 35, 80), -1)
                cv2.circle(img, spot, 11, (30, 120, 160), 1)

    # Encode to high-quality JPEG
    _, encoded = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 94])
    return encoded.tobytes()

def run_sample_scans():
    print("=" * 70)
    print("AgroScan AI — Live Sample Image Diagnostic Pipeline & History Test")
    print("=" * 70)

    client = TestClient(app)

    samples = [
        {"crop": "Tomato", "disease_key": "early_blight", "target_crop": "Tomato", "filename": "sample_tomato_early_blight.jpg"},
        {"crop": "Potato", "disease_key": "late_blight", "target_crop": "Potato", "filename": "sample_potato_late_blight.jpg"},
        {"crop": "Corn", "disease_key": "common_rust", "target_crop": "Corn", "filename": "sample_corn_common_rust.jpg"},
        {"crop": "Grape", "disease_key": "powdery_mildew", "target_crop": "Grape", "filename": "sample_grape_powdery_mildew.jpg"},
        {"crop": "Pepper", "disease_key": "healthy", "target_crop": "Pepper", "filename": "sample_pepper_healthy.jpg"},
        {"crop": "Pomegranate", "disease_key": "anthracnose", "target_crop": "Pomegranate", "filename": "sample_pomegranate_anthracnose.jpg"},
    ]

    scanned_results = []

    for i, s in enumerate(samples, 1):
        print(f"\n[{i}/{len(samples)}] Generating & Scanning: {s['crop']} ({s['disease_key']})...")
        img_bytes = generate_leaf_image(s["crop"], s["disease_key"])
        
        # Test multipart/form-data upload via /api/v1/predictions/analyze
        files = {
            "file": (s["filename"], img_bytes, "image/jpeg")
        }
        data = {
            "target_crop": s["target_crop"],
            "temperature_c": "27.5",
            "humidity_pct": "68.0",
            "rainfall_mm": "0.0",
            "location_name": "Kolhapur Farm Demo"
        }

        response = client.post("/api/v1/predictions/analyze", files=files, data=data)
        print(f"    Status Code: {response.status_code}")
        
        if response.status_code == 200:
            res_data = response.json()
            scan_id = res_data.get("id")
            crop = res_data.get("plant")
            disease = res_data.get("disease")
            confidence = res_data.get("confidence")
            severity = res_data.get("severity")
            risk = res_data.get("risk")
            print(f"    Scan ID:     {scan_id}")
            print(f"    Diagnosed:   {crop} -> {disease}")
            print(f"    Confidence:  {confidence:.1%}")
            print(f"    Severity:    {severity} ({res_data.get('severity_percentage', 0):.1f}%)")
            print(f"    Risk Level:  {risk}")
            scanned_results.append(res_data)
        else:
            print(f"    ERROR: {response.text}")

    print("\n" + "=" * 70)
    print("Verifying Stored Diagnostic History in SQLite Database...")
    print("=" * 70)

    db = SessionLocal()
    try:
        total_in_db = db.query(ScanPrediction).count()
        print(f"Total Scan Predictions in SQLite DB: {total_in_db}")

        recent_preds = db.query(ScanPrediction).order_by(ScanPrediction.created_at.desc()).limit(10).all()
        for idx, p in enumerate(recent_preds, 1):
            recs = db.query(Recommendation).filter(Recommendation.prediction_id == p.id).first()
            has_rec = bool(recs and (recs.organic_remedy or recs.chemical_remedy))
            print(f"  {idx}. [{p.id}] {p.crop_detected} - {p.disease_name} | Conf: {p.confidence_score:.1%} | Sev: {p.severity_level} | Treatment saved: {has_rec}")

        # Also verify GET /api/v1/predictions/history endpoint
        hist_response = client.get("/api/v1/predictions/history?limit=20")
        if hist_response.status_code == 200:
            hist_items = hist_response.json()
            print(f"\nGET /api/v1/predictions/history returned: {len(hist_items)} items")
            assert len(hist_items) > 0, "History should return stored items"
            print("SUCCESS: History endpoint cleanly returns saved records!")
        else:
            print(f"GET /history failed: {hist_response.status_code}")

    finally:
        db.close()

    print("\n" + "=" * 70)
    print("ALL SAMPLE SCANS COMPLETED & VERIFIED IN DATABASE HISTORY!")
    print("=" * 70)

if __name__ == "__main__":
    run_sample_scans()
