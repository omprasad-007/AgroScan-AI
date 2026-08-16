import cv2
import numpy as np
from typing import Dict, Any

class SeverityService:
    """
    OpenCV-based Preliminary Lesion Severity Analyzer.
    Categorizes lesion percentage into: Healthy, Low, Mild, Moderate, Severe, Critical.
    """
    @staticmethod
    def evaluate_severity(image_bytes: bytes) -> Dict[str, Any]:
        try:
            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if img is None:
                return {
                    "severity_percentage": 0.0,
                    "severity_level": "Healthy",
                    "affected_area_cm2": 0.0,
                    "assessment_type": "Preliminary severity assessment"
                }

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_leaf = np.array([10, 20, 20])
            upper_leaf = np.array([85, 255, 255])
            leaf_mask = cv2.inRange(hsv, lower_leaf, upper_leaf)

            lower_brown = np.array([0, 40, 20])
            upper_brown = np.array([25, 255, 180])
            brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, dark_mask = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)

            lesion_mask = cv2.bitwise_or(brown_mask, dark_mask)
            lesion_on_leaf = cv2.bitwise_and(lesion_mask, lesion_mask, mask=leaf_mask)

            total_leaf_pixels = np.count_nonzero(leaf_mask)
            lesion_pixels = np.count_nonzero(lesion_on_leaf)

            if total_leaf_pixels == 0:
                severity_pct = 12.0
            else:
                severity_pct = round(float((lesion_pixels / total_leaf_pixels) * 100.0), 2)
                severity_pct = max(0.0, min(95.0, severity_pct))

            if severity_pct < 2.0:
                level = "Healthy"
            elif severity_pct < 8.0:
                level = "Low"
            elif severity_pct < 18.0:
                level = "Mild"
            elif severity_pct < 35.0:
                level = "Moderate"
            elif severity_pct < 60.0:
                level = "Severe"
            else:
                level = "Critical"

            affected_cm2 = round((severity_pct / 100.0) * 50.0, 2)

            return {
                "severity_percentage": severity_pct,
                "severity_level": level,
                "affected_area_cm2": affected_cm2,
                "assessment_type": "Preliminary severity assessment",
                "note": "Calculated via OpenCV HSV color space segmentation. Prepared for custom ML severity model."
            }
        except Exception as e:
            return {
                "severity_percentage": 10.0,
                "severity_level": "Mild",
                "affected_area_cm2": 5.0,
                "assessment_type": "Preliminary severity assessment",
                "note": f"Fallback estimation: {str(e)}"
            }
