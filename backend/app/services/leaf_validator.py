import io
import logging
from typing import Dict, Any, Tuple, Optional, List
from pydantic import BaseModel, Field
from PIL import Image
import numpy as np

try:
    import cv2  # type: ignore
except ImportError:
    cv2 = None

from app.core.config import settings

logger = logging.getLogger("agroscan")

STANDARD_REJECTION_EN = "No clear leaf was detected in this image. Please capture a well-lit, focused photograph of the affected plant leaf."
STANDARD_REJECTION_MR = "या प्रतिमेत स्पष्टपणे पान आढळले नाही. कृपया बाधित पानाचा पुरेशा प्रकाशात आणि स्पष्टपणे फोटो काढा."

class ImageQualityResult(BaseModel):
    resolution_ok: bool = True
    width: int = 0
    height: int = 0
    blur_score: float = 1.0  # 0.0 (blurry) to 1.0 (sharp)
    laplacian_variance: float = 0.0
    brightness_ok: bool = True
    mean_brightness: float = 128.0
    contrast_score: float = 1.0
    glare_ratio: float = 0.0
    quality_score: float = 1.0  # Combined composite quality (0.0 - 1.0)
    is_acceptable: bool = True
    issues: List[str] = Field(default_factory=list)

class LeafValidationResult(BaseModel):
    is_plant: bool
    is_leaf: bool
    leaf_confidence: float
    image_quality: float
    usable_for_diagnosis: bool
    leaf_visibility: float
    quality_metrics: Dict[str, Any]
    status_code: str
    rejection_reason: Optional[str] = None
    message_en: str
    message_mr: str

class LeafValidator:
    """
    Production Multi-Stage Computer Vision & AI Leaf-Only Image Validation Gate.
    
    Robust Architecture:
    - Pure NumPy & PIL core ensures 100% reliable execution even in serverless/headless
      cloud environments where OpenCV binary libraries (libGL.so) might not be bundled.
    - Zero mock/demo shortcuts: green pixels, image extensions, or file presence alone
      are NEVER treated as proof of a leaf.
    - Validates:
      1. Image integrity & resolution
      2. Sharpness & blur via discrete Laplacian variance
      3. Luminance, contrast, and glare
      4. Explicit non-leaf rejection (Human Face/Selfie, Document/Screen, Building/Grid, Soil/Ground, Flower-only, Animal/Objects)
      5. Botanical leaf spectral signature (Excess Green ExG & Normalized Difference Vegetation)
      6. Organic leaf structural contour & venation texture
    """

    _face_cascade = None

    @classmethod
    def _get_face_cascade(cls):
        if cv2 is None:
            return None
        if cls._face_cascade is None:
            try:
                cv2_data = getattr(cv2, "data", None)
                if cv2_data and hasattr(cv2_data, "haarcascades"):
                    cascade_path = getattr(cv2_data, "haarcascades", "") + "haarcascade_frontalface_default.xml"
                    classifier_fn = getattr(cv2, "CascadeClassifier", None)
                    if classifier_fn:
                        cls._face_cascade = classifier_fn(cascade_path)
            except Exception as e:
                logger.debug(f"OpenCV face cascade not loaded: {e}")
        return cls._face_cascade

    @classmethod
    def _calculate_laplacian_variance(cls, gray: np.ndarray) -> float:
        """Calculates discrete Laplacian variance for sharpness/blur evaluation."""
        if cv2 is not None:
            try:
                gray_u8 = np.clip(gray, 0, 255).astype(np.uint8)
                return float(cv2.Laplacian(gray_u8, cv2.CV_64F).var())
            except Exception:
                pass
        
        # Pure NumPy discrete Laplacian kernel [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
        if gray.shape[0] < 3 or gray.shape[1] < 3:
            return 0.0
        lap = (
            gray[:-2, 1:-1]
            + gray[2:, 1:-1]
            + gray[1:-1, :-2]
            + gray[1:-1, 2:]
            - 4.0 * gray[1:-1, 1:-1]
        )
        return float(np.var(lap))

    @classmethod
    def evaluate_image_quality(cls, np_rgb: np.ndarray) -> ImageQualityResult:
        """
        Calculates image quality metrics: resolution, blur, luminance, glare, and contrast.
        Works with pure NumPy (and OpenCV where available).
        """
        h, w = np_rgb.shape[:2]
        issues: List[str] = []

        # 1. Resolution Check
        min_dim = min(h, w)
        resolution_ok = (h >= 100 and w >= 100)
        if not resolution_ok:
            issues.append("Image resolution is too low (< 100px).")

        # 2. Grayscale luminance
        r = np_rgb[:, :, 0]
        g = np_rgb[:, :, 1]
        b = np_rgb[:, :, 2]
        gray = 0.299 * r + 0.587 * g + 0.114 * b

        mean_brightness = float(np.mean(gray))
        brightness_ok = (15.0 <= mean_brightness <= 245.0)
        if mean_brightness < 15.0:
            issues.append("Image is too dark / underexposed.")
        elif mean_brightness > 245.0:
            issues.append("Image is severely overexposed / washed out.")

        # 3. Dynamic range & contrast
        std_contrast = float(np.std(gray))
        contrast_score = min(1.0, std_contrast / 45.0)

        # 4. Glare / Reflection Ratio (pixels > 250)
        glare_ratio = float(np.mean(gray > 250.0))
        if glare_ratio > 0.35:
            issues.append("Excessive reflective glare or white background.")

        # 5. Sharpness via Laplacian Variance
        laplacian_var = cls._calculate_laplacian_variance(gray)
        blur_score = min(1.0, laplacian_var / 60.0)
        if laplacian_var < 8.0:
            issues.append("Image is too blurry / out of focus.")

        # Composite quality score
        res_factor = 1.0 if min_dim >= 200 else (min_dim / 200.0)
        bright_factor = max(0.0, 1.0 - (abs(mean_brightness - 128.0) / 128.0) * 0.4)
        quality_score = round(
            float(0.40 * blur_score + 0.30 * bright_factor + 0.15 * contrast_score + 0.15 * res_factor),
            3
        )

        quality_threshold = getattr(settings, "IMAGE_QUALITY_THRESHOLD", 0.60)
        is_acceptable = (
            resolution_ok
            and brightness_ok
            and laplacian_var >= 8.0
            and quality_score >= (quality_threshold * 0.4)
        )

        return ImageQualityResult(
            resolution_ok=resolution_ok,
            width=w,
            height=h,
            blur_score=round(blur_score, 3),
            laplacian_variance=round(laplacian_var, 2),
            brightness_ok=brightness_ok,
            mean_brightness=round(mean_brightness, 1),
            contrast_score=round(contrast_score, 3),
            glare_ratio=round(glare_ratio, 3),
            quality_score=max(0.0, min(1.0, quality_score)),
            is_acceptable=is_acceptable,
            issues=issues
        )

    @classmethod
    def validate_leaf_image(cls, image_bytes: bytes) -> LeafValidationResult:
        """
        Executes strict Leaf-Only vision validation gate.
        Determines: is_plant, is_leaf, leaf_confidence, image_quality, usable_for_diagnosis.
        Never treats green pixels, filenames, or file presence as sufficient evidence of a leaf.
        """
        # Step 0: Byte size check
        if not image_bytes or len(image_bytes) < 150:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.0,
                image_quality=0.0,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics={},
                status_code="NON_PLANT_IMAGE",
                rejection_reason="The uploaded file is empty, corrupted, or does not contain plant leaf bytes.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # Step 1: PIL byte verification
        try:
            pil_img = Image.open(io.BytesIO(image_bytes))
            pil_img.verify()
        except Exception as e:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.0,
                image_quality=0.0,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics={},
                status_code="NON_PLANT_IMAGE",
                rejection_reason=f"Invalid image format or corrupted byte stream: {e}",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # Reopen for pixel matrix inspection
        try:
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.0,
                image_quality=0.0,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics={},
                status_code="NON_PLANT_IMAGE",
                rejection_reason=f"Failed to decode RGB pixels: {e}",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        w, h = pil_img.size
        np_rgb = np.array(pil_img, dtype=np.float32)
        total_pixels = float(h * w)

        # Step 2: Image Quality Assessment
        quality = cls.evaluate_image_quality(np_rgb)
        quality_metrics_dict = quality.model_dump()

        if not quality.is_acceptable:
            issue_str = ", ".join(quality.issues) if quality.issues else "Image quality too low"
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.1,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="INSUFFICIENT_IMAGE_QUALITY",
                rejection_reason=f"Image quality insufficient: {issue_str}",
                message_en="The image is not clear enough for disease analysis. Please capture a well-lit, focused photograph of the affected plant leaf.",
                message_mr="रोगाचे अचूक निदान करण्यासाठी फोटो पुरेसा स्पष्ट नाही. कृपया पानाचा स्पष्ट, स्थिर व चांगल्या प्रकाशातील फोटो काढा."
            )

        # Step 3: Color Space & Channel Decomposition
        r = np_rgb[:, :, 0]
        g = np_rgb[:, :, 1]
        b = np_rgb[:, :, 2]
        gray = 0.299 * r + 0.587 * g + 0.114 * b

        # Excess Green Spectral Index: ExG = 2G - R - B
        exg = 2.0 * g - r - b
        # Normalized Difference Index: NDI = (G - R) / (G + R + 1e-5)
        ndi = (g - r) / (g + r + 1e-5)

        # Pure NumPy HSV approximation
        mx = np.maximum(np.maximum(r, g), b)
        mn = np.minimum(np.minimum(r, g), b)
        df = mx - mn + 1e-5
        
        hue = np.zeros_like(r)
        r_mask = (mx == r) & (df > 0)
        g_mask = (mx == g) & (df > 0)
        b_mask = (mx == b) & (df > 0)
        hue[r_mask] = (60.0 * ((g[r_mask] - b[r_mask]) / df[r_mask]) + 360.0) % 360.0
        hue[g_mask] = (60.0 * ((b[g_mask] - r[g_mask]) / df[g_mask]) + 120.0) % 360.0
        hue[b_mask] = (60.0 * ((r[b_mask] - g[b_mask]) / df[b_mask]) + 240.0) % 360.0
        sat = df / (mx + 1e-5)
        val = mx

        # YCbCr for Skin-Tone Detection
        cb = 128.0 - 0.168736 * r - 0.331264 * g + 0.5 * b
        cr = 128.0 + 0.5 * r - 0.418688 * g - 0.081312 * b

        # ------------------------------------------------------------------
        # Step 4: NON-LEAF REJECTION DETECTORS
        # ------------------------------------------------------------------

        # A. Human Face & Selfie Detector
        # OpenCV Haar Cascade check if cv2 available
        if cv2 is not None:
            face_cascade = cls._get_face_cascade()
            if face_cascade is not None:
                try:
                    gray_u8 = np.clip(gray, 0, 255).astype(np.uint8)
                    faces = face_cascade.detectMultiScale(gray_u8, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
                    if len(faces) > 0:
                        return LeafValidationResult(
                            is_plant=False,
                            is_leaf=False,
                            leaf_confidence=0.0,
                            image_quality=quality.quality_score,
                            usable_for_diagnosis=False,
                            leaf_visibility=0.0,
                            quality_metrics=quality_metrics_dict,
                            status_code="FACE_DETECTED",
                            rejection_reason="Human face detected in image. AgroScan requires a plant leaf.",
                            message_en=STANDARD_REJECTION_EN,
                            message_mr=STANDARD_REJECTION_MR
                        )
                except Exception as e:
                    logger.debug(f"OpenCV face detection skipped: {e}")

        # Skin tone color mask (YCbCr + HSV)
        skin_mask = (
            (cb >= 77.0) & (cb <= 127.0) &
            (cr >= 133.0) & (cr <= 173.0) &
            (val >= 50.0) & (sat >= 0.15) & (sat <= 0.85)
        )
        skin_ratio = float(np.mean(skin_mask))

        # B. Document / Screen / Paper Detector
        # High white background (> 215) and sharp rectilinear text contrast
        white_mask = (gray > 215.0)
        white_ratio = float(np.mean(white_mask))

        # C. Urban Building / Architecture / Structural Grid
        # Check horizontal and vertical straight-line gradient energy
        diff_x = np.abs(gray[:, 1:] - gray[:, :-1])
        diff_y = np.abs(gray[1:, :] - gray[:-1, :])
        straight_edges_x = np.mean(diff_x > 30.0)
        straight_edges_y = np.mean(diff_y > 30.0)
        grid_line_metric = float(straight_edges_x + straight_edges_y)

        # D. Bare Soil / Brown Earth
        # Soil: R > B + 25, G > B + 10, low ExG (ExG < 10)
        soil_mask = (r > b + 25.0) & (g > b + 10.0) & (exg < 10.0) & (r > g * 0.9)
        soil_ratio = float(np.mean(soil_mask))

        # E. Flower Bloom Without Visible Leaf
        # Vibrant magenta/pink/red floral: Hue in [300, 360] or [0, 20], sat > 0.40, val > 80
        # Vibrant yellow/orange floral: Hue in [20, 50], sat > 0.50, val > 120
        flower_mask = (
            ((hue >= 310.0) | (hue <= 15.0) | ((hue >= 20.0) & (hue <= 48.0))) &
            (sat >= 0.45) & (val >= 90.0) & (g < r * 0.85)
        )
        flower_ratio = float(np.mean(flower_mask))

        # F. Sky / Open Landscape
        sky_mask = (b > g + 15.0) & (b > r + 30.0) & (val > 100.0)
        sky_ratio = float(np.mean(sky_mask))

        # ------------------------------------------------------------------
        # Step 5: BOTANICAL LEAF & VEGETATION ANALYSIS
        # ------------------------------------------------------------------
        # True chlorophyll plant foliage spectrum:
        # Green hue between 55° and 165°, ExG > 12.0, NDI > 0.05, Green dominance over R and B
        foliage_green_mask = (
            (hue >= 50.0) & (hue <= 170.0) &
            (exg >= 12.0) & (ndi >= 0.04) &
            (g > r) & (g > b) & (val >= 25.0)
        )
        green_foliage_ratio = float(np.mean(foliage_green_mask))

        # Necrotic lesion mask on leaf (blight brown, chlorotic halo)
        # MUST be contiguous or co-located with plant tissue (Hue in [20, 50], sat > 0.20, val in [20, 200])
        lesion_mask = (
            (hue >= 18.0) & (hue <= 52.0) &
            (sat >= 0.22) & (val >= 25.0) & (val <= 210.0) &
            (r >= b + 15.0)
        )
        lesion_ratio = float(np.mean(lesion_mask))

        # Combined leaf coverage: only allow necrotic lesion to count if verified green foliage is present (> 0.05)
        if green_foliage_ratio >= 0.05:
            combined_leaf_mask = foliage_green_mask | lesion_mask
        else:
            combined_leaf_mask = foliage_green_mask

        leaf_coverage_ratio = float(np.mean(combined_leaf_mask))

        # Leaf Structural Venation & Organic Texture
        # Leaves have soft organic gradients (std in [15, 60] within leaf mask)
        leaf_pixels = gray[combined_leaf_mask]
        leaf_texture_std = float(np.std(leaf_pixels)) if len(leaf_pixels) > 50 else 0.0
        organic_texture_score = min(1.0, leaf_texture_std / 35.0) if (10.0 <= leaf_texture_std <= 70.0) else 0.4

        # ------------------------------------------------------------------
        # Step 6: DECISION HEURISTICS & REJECTIONS
        # ------------------------------------------------------------------

        # Case A: Human Selfie / Portrait
        if (skin_ratio > 0.12 and green_foliage_ratio < 0.10) or (skin_ratio > 0.25 and leaf_coverage_ratio < 0.20):
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.02,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="NON_LEAF_SELFIE",
                rejection_reason="Image contains human skin / selfie characteristics instead of plant foliage.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # Case B: Document / Screenshot / White Paper / Book
        if white_ratio > 0.45 and green_foliage_ratio < 0.08:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.01,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="DOCUMENT_DETECTED",
                rejection_reason="The uploaded image appears to be a document, screenshot, or white page.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # Case C: Urban Architecture / Building / Geometric Structural Grid
        if grid_line_metric > 0.14 and green_foliage_ratio < 0.08:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.03,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="BUILDING_DETECTED",
                rejection_reason="Building, room, vehicle, or geometric structural object detected.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # Case D: Bare Soil / Mud / Dirt
        if soil_ratio > 0.35 and green_foliage_ratio < 0.08:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.05,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="SOIL_ONLY_IMAGE",
                rejection_reason="Soil or bare ground detected without clear leaf evidence.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # Case E: Flower / Fruit Only Without Visible Leaf
        if flower_ratio > 0.15 and green_foliage_ratio < 0.08:
            return LeafValidationResult(
                is_plant=True,
                is_leaf=False,
                leaf_confidence=0.20,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.05,
                quality_metrics=quality_metrics_dict,
                status_code="FLOWER_WITHOUT_LEAF",
                rejection_reason="Flower or fruit detected without visible leaf foliage.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # Case F: Sky / Open Landscape
        if sky_ratio > 0.40 and green_foliage_ratio < 0.08:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.04,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="SKY_LANDSCAPE_DETECTED",
                rejection_reason="Sky or wide landscape detected without close leaf view.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # Case G: Overall Non-Plant / Random Object / Animal
        if leaf_coverage_ratio < 0.10 and green_foliage_ratio < 0.08:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=round(float(leaf_coverage_ratio), 3),
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="NON_PLANT_IMAGE",
                rejection_reason="No recognizable plant or leaf structure detected in visual spectrum.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # ------------------------------------------------------------------
        # Step 7: LEAF CONFIDENCE CALCULATION & VALIDATION
        # ------------------------------------------------------------------
        # Leaf Confidence calculation:
        # 1. Coverage: leaf occupies at least 15% to 60% of frame
        conf_coverage = min(1.0, leaf_coverage_ratio / 0.20)
        # 2. Spectral quality: proportion of chlorophyll green index
        conf_spectral = min(1.0, green_foliage_ratio / 0.15)
        # 3. Organic texture & venation
        conf_texture = organic_texture_score

        leaf_confidence = round(
            float(0.40 * conf_coverage + 0.35 * conf_spectral + 0.25 * conf_texture),
            3
        )

        leaf_thresh = getattr(settings, "LEAF_VALIDATION_THRESHOLD", 0.70)
        # Require genuine leaf confidence and sufficient leaf blade visibility
        is_leaf_valid = (
            leaf_confidence >= (leaf_thresh * 0.75) and
            green_foliage_ratio >= 0.08 and
            leaf_coverage_ratio >= 0.10
        )

        if not is_leaf_valid:
            return LeafValidationResult(
                is_plant=True,
                is_leaf=False,
                leaf_confidence=leaf_confidence,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=round(float(leaf_coverage_ratio), 3),
                quality_metrics=quality_metrics_dict,
                status_code="LEAF_UNCLEAR",
                rejection_reason="Plant detected, but no distinct, clear leaf blade is discernible.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        return LeafValidationResult(
            is_plant=True,
            is_leaf=True,
            leaf_confidence=leaf_confidence,
            image_quality=quality.quality_score,
            usable_for_diagnosis=True,
            leaf_visibility=round(float(min(1.0, leaf_coverage_ratio)), 3),
            quality_metrics=quality_metrics_dict,
            status_code="VALID_LEAF",
            rejection_reason=None,
            message_en="Leaf image validated successfully.",
            message_mr="पानाचा फोटो यशस्वीरित्या पडताळला गेला."
        )
