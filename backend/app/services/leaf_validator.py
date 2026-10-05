import io
try:
    import cv2
except ImportError:
    cv2 = None  # OpenCV not available, will raise error at runtime
import numpy as np
import logging
from typing import Dict, Any, Tuple, Optional, List
from pydantic import BaseModel, Field
from PIL import Image
from app.core.config import settings

logger = logging.getLogger("agroscan")

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
    Advanced Multi-Stage Computer Vision & AI Leaf-Only Image Validation Gate.
    
    Pipeline Stages:
    1. Byte integrity & PIL Header Verification
    2. Computer Vision Image Quality Assessment (Resolution, Blur, Lighting, Contrast, Glare)
    3. Non-Leaf Rejection Engine (Faces, Documents, Soil, Buildings, Vehicles, Flowers-only)
    4. Botanical Leaf & Foliage Verification (Vegetation Spectral Indices, Morphological Contours, Venation Texture)
    5. Final Decision & Structured Diagnostic Gate
    """

    # Load OpenCV Pre-trained Haar Cascade for Human Face Detection
    _face_cascade = None

    @classmethod
    def _get_face_cascade(cls):
        if cv2 is None:
            logger.warning('OpenCV (cv2) is not installed; face cascade cannot be loaded.')
            return None
        if cls._face_cascade is None:
            try:
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                cls._face_cascade = cv2.CascadeClassifier(cascade_path)
            except Exception as e:
                logger.warning(f"Failed to load OpenCV face cascade: {e}")
        return cls._face_cascade

    @classmethod
    def evaluate_image_quality(cls, cv_img: np.ndarray) -> ImageQualityResult:
    """Calculate image quality metrics.
    
    If OpenCV is not available, returns a default failing result so callers can handle gracefully.
    """
    if cv2 is None:
        logger.warning('OpenCV (cv2) is not installed; image quality assessment cannot be performed.')
        return ImageQualityResult(
            resolution_ok=False,
            width=0,
            height=0,
            blur_score=0.0,
            laplacian_variance=0.0,
            brightness_ok=False,
            mean_brightness=0.0,
            contrast_score=0.0,
            glare_ratio=0.0,
            quality_score=0.0,
            is_acceptable=False,
            issues=["OpenCV not installed"]
        )
    # Original implementation below
    h, w = cv_img.shape[:2]
    issues = []
    # 1. Resolution Check
    min_dim = min(h, w)
    resolution_ok = (h >= 100 and w >= 100)
    if not resolution_ok:
        issues.append("Image resolution is too low (< 100px).")
    # 2. Brightness & Extreme Lighting Check
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    mean_brightness = float(np.mean(gray))
    brightness_ok = (15.0 <= mean_brightness <= 245.0)
    if mean_brightness < 15.0:
        issues.append("Image is too dark / underexposed.")
    elif mean_brightness > 245.0:
        issues.append("Image is severely overexposed / washed out.")
    # 3. Contrast & Dynamic Range
    std_contrast = float(np.std(gray))
    contrast_score = min(1.0, std_contrast / 45.0)
    # 4. Glare / Reflection Ratio (pixels with brightness > 250)
    glare_pixels = np.count_nonzero(gray > 250)
    glare_ratio = float(glare_pixels / (h * w))
    if glare_ratio > 0.35:
        issues.append("Excessive reflective glare or white background.")
    # 5. Sharpness / Blur via Laplacian Variance
    laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    blur_score = min(1.0, laplacian_var / 80.0)
    if laplacian_var < 8.0:
        issues.append("Image is too blurry / out of focus.")
    # Composite quality score
    res_factor = 1.0 if min_dim >= 250 else (min_dim / 250.0)
    bright_factor = 1.0 - (abs(mean_brightness - 128.0) / 128.0) * 0.5
    quality_score = round(
        float(0.40 * blur_score + 0.30 * bright_factor + 0.15 * contrast_score + 0.15 * res_factor),
        3,
    )
    quality_threshold = getattr(settings, "IMAGE_QUALITY_THRESHOLD", 0.60)
    is_acceptable = (
        resolution_ok and brightness_ok and laplacian_var >= 8.0 and quality_score >= (quality_threshold * 0.5)
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
        issues=issues,
    )
        """
        Calculates image quality metrics: resolution, blur, luminance, glare, and contrast.
        """
        h, w = cv_img.shape[:2]
        issues = []
        
        # 1. Resolution Check
        min_dim = min(h, w)
        resolution_ok = (h >= 100 and w >= 100)
        if not resolution_ok:
            issues.append("Image resolution is too low (< 100px).")

        # 2. Brightness & Extreme Lighting Check
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        mean_brightness = float(np.mean(gray))
        brightness_ok = (15.0 <= mean_brightness <= 245.0)
        
        if mean_brightness < 15.0:
            issues.append("Image is too dark / underexposed.")
        elif mean_brightness > 245.0:
            issues.append("Image is severely overexposed / washed out.")

        # 3. Contrast & Dynamic Range
        std_contrast = float(np.std(gray))
        contrast_score = min(1.0, std_contrast / 45.0)

        # 4. Glare / Reflection Ratio (pixels with brightness > 250)
        glare_pixels = np.count_nonzero(gray > 250)
        glare_ratio = float(glare_pixels / (h * w))
        if glare_ratio > 0.35:
            issues.append("Excessive reflective glare or white background.")

        # 5. Sharpness / Blur via Laplacian Variance
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        # Sigmoid-normalized blur score: < 15 is blurry, 50+ is crisp
        blur_score = min(1.0, laplacian_var / 80.0)
        if laplacian_var < 8.0:
            issues.append("Image is too blurry / out of focus.")

        # Calculate composite quality score (0.0 to 1.0)
        res_factor = 1.0 if min_dim >= 250 else (min_dim / 250.0)
        bright_factor = 1.0 - (abs(mean_brightness - 128.0) / 128.0) * 0.5
        quality_score = round(
            float(0.40 * blur_score + 0.30 * bright_factor + 0.15 * contrast_score + 0.15 * res_factor),
            3
        )
        
        quality_threshold = getattr(settings, "IMAGE_QUALITY_THRESHOLD", 0.60)
        is_acceptable = (
            resolution_ok and 
            brightness_ok and 
            laplacian_var >= 8.0 and 
            quality_score >= (quality_threshold * 0.5)
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
        if cv2 is None:
            raise ImportError('OpenCV (cv2) is required for leaf validation but is not installed.')
        """
        Executes strict Leaf-Only vision validation.
        Determines: is_plant, is_leaf, leaf_confidence, image_quality, usable_for_diagnosis.
        """
        if not image_bytes or len(image_bytes) < 150:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.0,
                image_quality=0.0,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics={},
                status_code="EMPTY_OR_CORRUPT_IMAGE",
                rejection_reason="The uploaded file is empty or corrupted.",
                message_en="No clear leaf was detected in this image. Please capture a close, well-lit photo of a plant leaf.",
                message_mr="या प्रतिमेत स्पष्टपणे पान आढळले नाही. कृपया वनस्पतीच्या पानाचा जवळून आणि स्पष्ट फोटो काढा."
            )

        # 1. PIL Image Verification
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
                status_code="INVALID_IMAGE_PAYLOAD",
                rejection_reason=f"Invalid image format or corrupted byte stream: {e}",
                message_en="Invalid image format. Please capture or upload a valid JPEG, PNG, or WEBP leaf photo.",
                message_mr="अवैध प्रतिमा स्वरूप. कृपया पानाचा वैध JPEG, PNG किंवा WEBP फोटो अपलोड करा."
            )

        # 2. Decode with OpenCV
        np_arr = np.frombuffer(image_bytes, np.uint8)
        cv_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if cv_img is None:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.0,
                image_quality=0.0,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics={},
                status_code="DECODE_FAILED",
                rejection_reason="Could not decode image bytes into RGB matrix.",
                message_en="Unable to process the image. Please scan a clear photo of a plant leaf.",
                message_mr="प्रतिमा प्रक्रिया करता आली नाही. कृपया पानाचा स्पष्ट फोटो काढा."
            )

        # 3. Assess Image Quality
        quality = cls.evaluate_image_quality(cv_img)
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
                message_en=f"Image is not clear enough for disease analysis ({issue_str}). Please capture a sharper, well-lit photo of the leaf.",
                message_mr="रोगाचे अचूक निदान करण्यासाठी फोटो पुरेसा स्पष्ट नाही. कृपया पानाचा स्पष्ट, स्थिर व चांगल्या प्रकाशातील फोटो काढा."
            )

        h, w = cv_img.shape[:2]
        total_pixels = h * w
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
        b, g, r = cv2.split(cv_img.astype(np.float32))

        # 4. REJECTION DETECTORS

        # A. Face / Selfie Detection
        face_cascade = cls._get_face_cascade()
        if face_cascade is not None:
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
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
                    message_en="No clear leaf was detected. A person or face was detected. Please capture a close, well-lit photo of a plant leaf.",
                    message_mr="प्रतिमेत व्यक्तीचा चेहरा आढळला आहे. रोग निदानासाठी कृपया वनस्पतीचे पान स्कॅन करा."
                )

        # B. Skin-Tone Mask Analysis
        lower_skin1 = np.array([0, 25, 50], dtype=np.uint8)
        upper_skin1 = np.array([25, 180, 255], dtype=np.uint8)
        lower_skin2 = np.array([165, 25, 50], dtype=np.uint8)
        upper_skin2 = np.array([180, 180, 255], dtype=np.uint8)
        skin_mask = cv2.bitwise_or(
            cv2.inRange(hsv, lower_skin1, upper_skin1),
            cv2.inRange(hsv, lower_skin2, upper_skin2)
        )
        skin_ratio = float(np.count_nonzero(skin_mask) / total_pixels)

        # C. Document / White Paper / Screen Detector
        white_mask = cv2.inRange(gray, 220, 255)
        white_ratio = float(np.count_nonzero(white_mask) / total_pixels)
        
        # Edge straightness / Hough lines check (documents, screens, walls, buildings)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=int(min(h, w) * 0.4), maxLineGap=10)
        long_line_count = len(lines) if lines is not None else 0

        # D. Soil / Brown Earth Dominance Mask
        lower_soil = np.array([10, 50, 30], dtype=np.uint8)
        upper_soil = np.array([24, 255, 180], dtype=np.uint8)
        soil_mask = cv2.inRange(hsv, lower_soil, upper_soil)
        soil_ratio = float(np.count_nonzero(soil_mask) / total_pixels)

        # E. Flower Petal Mask (Red/Pink/Magenta/Bright Yellow floral blooms)
        lower_flower1 = np.array([0, 120, 100], dtype=np.uint8)
        upper_flower1 = np.array([12, 255, 255], dtype=np.uint8)
        lower_flower2 = np.array([145, 80, 100], dtype=np.uint8)
        upper_flower2 = np.array([179, 255, 255], dtype=np.uint8)
        flower_mask = cv2.bitwise_or(
            cv2.inRange(hsv, lower_flower1, upper_flower1),
            cv2.inRange(hsv, lower_flower2, upper_flower2)
        )
        flower_ratio = float(np.count_nonzero(flower_mask) / total_pixels)

        # F. Sky / Blue Landscape Mask
        lower_sky = np.array([95, 40, 90], dtype=np.uint8)
        upper_sky = np.array([135, 255, 255], dtype=np.uint8)
        sky_mask = cv2.inRange(hsv, lower_sky, upper_sky)
        sky_ratio = float(np.count_nonzero(sky_mask) / total_pixels)

        # 5. BOTANICAL LEAF & VEGETATION ANALYSIS

        # Vegetation Spectral Indices:
        # Excess Green: ExG = 2G - R - B
        exg = 2.0 * g - r - b
        exg_veg_mask = (exg > 10.0).astype(np.uint8)
        exg_ratio = float(np.count_nonzero(exg_veg_mask) / total_pixels)

        # Foliage HSV spectrum (Green, Olive, Chartreuse, Yellow-Green, Chlorotic Leaf Spots)
        lower_foliage = np.array([26, 30, 25], dtype=np.uint8)
        upper_foliage = np.array([92, 255, 255], dtype=np.uint8)
        foliage_mask = cv2.inRange(hsv, lower_foliage, upper_foliage)
        foliage_ratio = float(np.count_nonzero(foliage_mask) / total_pixels)

        # Diseased / Necrotic Lesion Hue Mask (Blight brown, rust orange, yellow halos on leaf)
        lower_lesion = np.array([14, 40, 25], dtype=np.uint8)
        upper_lesion = np.array([27, 255, 240], dtype=np.uint8)
        lesion_mask = cv2.inRange(hsv, lower_lesion, upper_lesion)
        lesion_ratio = float(np.count_nonzero(lesion_mask) / total_pixels)

        # Total combined vegetative & plant leaf canopy
        combined_leaf_mask = cv2.bitwise_or(foliage_mask, exg_veg_mask * 255)
        leaf_coverage_ratio = float(np.count_nonzero(combined_leaf_mask) / total_pixels)

        # Leaf Structural & Organic Texture via Contours
        contours, _ = cv2.findContours(combined_leaf_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_contour_area = 0.0
        organic_leaf_count = 0
        if contours:
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > (total_pixels * 0.03):
                    max_contour_area = max(max_contour_area, area)
                    # Check contour solidity and organic curvature
                    hull = cv2.convexHull(cnt)
                    hull_area = cv2.contourArea(hull)
                    if hull_area > 0:
                        solidity = area / hull_area
                        if 0.35 <= solidity <= 0.98:
                            organic_leaf_count += 1

        primary_leaf_ratio = max_contour_area / total_pixels

        # 6. DECISION HEURISTICS & REJECTIONS

        # Case A: Heavy Skin-Tone / Human Selfie
        if skin_ratio > 0.22 and leaf_coverage_ratio < 0.20:
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
                message_en="No clear leaf was detected in this image. Please capture a close, well-lit photo of a plant leaf.",
                message_mr="या प्रतिमेत स्पष्टपणे पान आढळले नाही. कृपया वनस्पतीच्या पानाचा जवळून आणि स्पष्ट फोटो काढा."
            )

        # Case B: Document / Screenshot / White Page
        if white_ratio > 0.55 and leaf_coverage_ratio < 0.12:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.01,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="DOCUMENT_DETECTED",
                rejection_reason="Document, screenshot, or white paper detected.",
                message_en="The uploaded image appears to be a document or screenshot. Please capture an actual plant leaf photo.",
                message_mr="अपलोड केलेली प्रतिमा दस्तऐवज किंवा स्क्रीनशॉट वाटत आहे. कृपया पिकाच्या पानाचा खरा फोटो काढा."
            )

        # Case C: Urban Architecture / Building / Straight Structural Grid
        if long_line_count >= 8 and leaf_coverage_ratio < 0.12:
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
                message_en="No leaf was detected (building or structure recognized). Please point the camera at a plant leaf.",
                message_mr="इमारत किंवा इतर वस्तू आढळली आहे. कृपया कॅमेरा वनस्पतीच्या पानावर धरा."
            )

        # Case D: Soil-Only / Mud Without Leaves
        if soil_ratio > 0.60 and leaf_coverage_ratio < 0.08:
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
                message_en="No leaf detected. Only soil or ground is visible. Please capture the plant leaf showing symptoms.",
                message_mr="केवळ माती किंवा जमीन दिसत आहे. कृपया लक्षणे दिसणारे पिकाचे पान स्कॅन करा."
            )

        # Case E: Flower / Fruit Only Without Visible Leaf
        if flower_ratio > 0.35 and leaf_coverage_ratio < 0.08:
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
                message_en="Leaf not detected. AgroScan's disease scanner currently requires a visible leaf. Please capture the affected leaf.",
                message_mr="अ‍ॅग्रोस्कॅन रोग स्कॅनरसाठी पानाची आवश्यकता आहे. कृपया प्रादुर्भाव झालेले पान स्कॅन करा."
            )

        # Case F: Sky / Open Landscape
        if sky_ratio > 0.45 and leaf_coverage_ratio < 0.10:
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
                message_en="No leaf detected. The image is too far or shows sky/landscape. Please get closer to the leaf.",
                message_mr="पान स्पष्ट दिसत नाही. कृपया पानाजवळ जाऊन क्लोज-अप फोटो काढा."
            )

        # Case G: Overall Non-Plant / Random Object
        if leaf_coverage_ratio < 0.10 and (foliage_ratio + lesion_ratio) < 0.08:
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
                message_en="No clear leaf was detected in this image. Please capture a close, well-lit photo of a plant leaf.",
                message_mr="या प्रतिमेत स्पष्टपणे पान आढळले नाही. कृपया वनस्पतीच्या पानाचा जवळून आणि स्पष्ट फोटो काढा."
            )

        # 7. VALID LEAF CONFIRMATION & SCORING
        # Leaf Confidence calculation based on organic leaf contour, vegetation index, and foliage coverage
        conf_coverage = min(1.0, leaf_coverage_ratio / 0.30)
        conf_contour = 0.90 if organic_leaf_count > 0 else (0.75 if primary_leaf_ratio > 0.15 else 0.60)
        conf_spectral = min(1.0, (exg_ratio + foliage_ratio) / 0.25)
        
        leaf_confidence = round(
            float(0.40 * conf_coverage + 0.35 * conf_spectral + 0.25 * conf_contour),
            3
        )

        leaf_thresh = getattr(settings, "LEAF_VALIDATION_THRESHOLD", 0.70)
        is_leaf_valid = (leaf_confidence >= (leaf_thresh * 0.75) and leaf_coverage_ratio >= 0.08)

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
                message_en="Plant detected, but no clear leaf blade is visible. Please move closer and capture a single leaf.",
                message_mr="वनस्पती आढळली, परंतु स्पष्ट पान दिसले नाही. कृपया पानाजवळ जाऊन स्पष्ट फोटो काढा."
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
