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

REJECTION_REASONS: Dict[str, str] = {
    "HUMAN_DETECTED": "No plant leaf detected. A person or human was detected in this photo.",
    "FACE_DETECTED": "Human face detected in image. AgroScan AI requires a clear photograph of a plant leaf.",
    "NON_LEAF_SELFIE": "Selfie or portrait detected instead of plant foliage. Please capture a photo of a plant leaf.",
    "ANIMAL_DETECTED": "No plant leaf detected. An animal or pet was detected in this image. AgroScan AI requires an affected plant leaf.",
    "OBJECT_DETECTED": "No plant leaf detected. An artificial object, vehicle, furniture, or indoor scene was detected.",
    "BUILDING_DETECTED": "Building, architectural structure, or geometric object detected.",
    "DOCUMENT_DETECTED": "The uploaded image appears to be a document, screenshot, or white page.",
    "SOIL_ONLY_IMAGE": "Soil or bare ground detected without clear leaf evidence.",
    "FLOWER_WITHOUT_LEAF": "Flower bloom or fruit detected without visible leaf foliage.",
    "SKY_LANDSCAPE_DETECTED": "Sky or wide landscape detected without close leaf view.",
    "INSUFFICIENT_IMAGE_QUALITY": "The image is too blurry or poor quality for disease analysis.",
    "LEAF_UNCLEAR": "Plant vegetation detected, but no distinct, clear leaf blade is discernible.",
    "NON_PLANT_IMAGE": "No recognizable plant or leaf structure detected in visual spectrum."
}


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
      cloud environments where OpenCV binary libraries might not be bundled.
    - Multi-stage discrimination:
      1. Image integrity, sharpness, exposure, contrast, and resolution.
      2. Deep learning object classification (MobileNetV2 ImageNet) for animal, human, and object rejection.
      3. Universal skin tone and human facial/portrait geometry detection.
      4. Mammalian fur, coat color, and directional texture detection.
      5. Center-focus subject isolation: rejects animals, humans, and objects posed on grass or outdoors.
      6. Contiguous lesion verification: lesions must be embedded on genuine chlorophyll leaf blade tissue.
      7. Rejection of documents, screens, buildings, bare soil, sky, and flowers without leaves.
      8. Botanical chlorophyll spectrum and organic leaf blade structural confidence verification.
    """

    _face_cascade = None
    _mobilenet_model = None
    _mobilenet_preprocess = None
    _mobilenet_cats = None
    _mobilenet_init_attempted = False

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
    def _get_deep_classifier(cls):
        """Lazy-loads MobileNetV2 with ImageNet weights for zero-shot object/animal discrimination."""
        if cls._mobilenet_init_attempted:
            return cls._mobilenet_model, cls._mobilenet_preprocess, cls._mobilenet_cats
        cls._mobilenet_init_attempted = True
        try:
            import torchvision.models as tv_models
            from torchvision.models import MobileNet_V2_Weights
            weights = MobileNet_V2_Weights.DEFAULT
            model = tv_models.mobilenet_v2(weights=weights)
            model.eval()
            cls._mobilenet_model = model
            cls._mobilenet_preprocess = weights.transforms()
            cls._mobilenet_cats = weights.meta.get("categories", [])
            logger.info("MobileNetV2 ImageNet deep classifier loaded for non-plant validation.")
        except Exception as e:
            logger.debug(f"MobileNetV2 deep classifier unavailable: {e}")
            cls._mobilenet_model = None
            cls._mobilenet_preprocess = None
            cls._mobilenet_cats = None
        return cls._mobilenet_model, cls._mobilenet_preprocess, cls._mobilenet_cats

    @classmethod
    def _evaluate_deep_learning_subject(cls, pil_img: Image.Image) -> Optional[Tuple[str, str, float]]:
        """
        Runs pretrained ImageNet classifier to detect out-of-distribution non-plant subjects:
        Animals (classes 0..397: dogs, cats, cows, horses, birds, wildlife),
        Humans (clothing, accessories, divers, suits),
        Vehicles, Electronics, Furniture, Household items.
        Returns: Optional[Tuple[status_code, detected_entity_name, confidence]]
        """
        model, preprocess, cats = cls._get_deep_classifier()
        if model is None or preprocess is None or not cats:
            return None
        try:
            import torch
            batch = preprocess(pil_img).unsqueeze(0)
            with torch.no_grad():
                logits = model(batch).squeeze(0)
                probs = torch.softmax(logits, dim=0)

            top5_prob, top5_idx = torch.topk(probs, 5)
            top_cat_id = int(top5_idx[0].item())
            top_prob = float(top5_prob[0].item())
            top_name = cats[top_cat_id]

            # Classes 0 to 397 in ImageNet are ANIMALS
            animal_prob = float(probs[:398].sum().item())
            if top_cat_id < 398 and (top_prob >= 0.22 or animal_prob >= 0.60):
                clean_animal = top_name.replace("_", " ").title()
                return ("ANIMAL_DETECTED", clean_animal, max(top_prob, animal_prob))
            
            if animal_prob >= 0.65:
                top_animal_name = cats[top_cat_id] if top_cat_id < 398 else "Animal"
                return ("ANIMAL_DETECTED", top_animal_name.replace("_", " ").title(), animal_prob)

            # Check for human clothing / accessories / personas
            human_garments = [
                "jersey", "sweatshirt", "suit", "gown", "jean", "kimono", "lab coat", 
                "fur coat", "cloak", "scuba diver", "sunglasses", "wig", "mask", "groom",
                "cardigan", "trench coat", "pajamas", "bulletproof vest", "apron", "brassiere",
                "swimming trunks", "bikini", "sarong", "sombrero", "cowboy hat"
            ]
            if any(g in top_name.lower() for g in human_garments) and top_prob >= 0.20:
                return ("NON_LEAF_SELFIE", top_name.replace("_", " ").title(), top_prob)

            # Check for vehicles, furniture, electronics, man-made objects
            object_keywords = [
                "car", "automobile", "truck", "bus", "motorcycle", "bicycle", "airplane",
                "laptop", "computer", "cellular telephone", "cellphone", "screen", "monitor",
                "desk", "chair", "sofa", "couch", "table", "refrigerator", "microwave",
                "shoe", "boot", "sandal", "sneaker", "backpack", "wallet", "watch",
                "coffee mug", "water bottle", "plate", "fork", "knife", "spoon"
            ]
            if any(k in top_name.lower() for k in object_keywords) and top_prob >= 0.25:
                return ("BUILDING_DETECTED", top_name.replace("_", " ").title(), top_prob)

            return None
        except Exception as e:
            logger.debug(f"Deep learning subject evaluation error: {e}")
            return None

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
        if glare_ratio > 0.50:
            issues.append("Excessive reflective glare or white background.")

        # 5. Sharpness via Laplacian Variance
        laplacian_var = cls._calculate_laplacian_variance(gray)
        blur_score = min(1.0, laplacian_var / 50.0)
        if laplacian_var < 4.0:
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
            and laplacian_var >= 4.0
            and quality_score >= (quality_threshold * 0.3)
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
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # Step 3: Deep Learning Subject Evaluation (ImageNet MobileNetV2)
        deep_res = cls._evaluate_deep_learning_subject(pil_img)
        if deep_res is not None:
            deep_status, entity_name, conf = deep_res
            logger.info(f"Deep learning subject gate flagged: {deep_status} - {entity_name} ({conf:.2f})")
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.02,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code=deep_status,
                rejection_reason=f"{entity_name} detected instead of a plant leaf ({deep_status}).",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # Step 4: Color Space & Channel Decomposition
        r = np_rgb[:, :, 0]
        g = np_rgb[:, :, 1]
        b = np_rgb[:, :, 2]
        gray = 0.299 * r + 0.587 * g + 0.114 * b

        # Excess Green Spectral Index: ExG = 2G - R - B
        exg = 2.0 * g - r - b

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

        # YCbCr for Universal Skin-Tone Detection
        cb = 128.0 - 0.168736 * r - 0.331264 * g + 0.5 * b
        cr = 128.0 + 0.5 * r - 0.418688 * g - 0.081312 * b

        # Central Focus Box (center 36% to 49% of image area where subject is framed)
        cy1, cy2 = int(0.18 * h), int(0.82 * h)
        cx1, cx2 = int(0.18 * w), int(0.82 * w)

        # Gradients, straight lines & texture metrics
        diff_x = np.abs(gray[:, 1:] - gray[:, :-1])
        diff_y = np.abs(gray[1:, :] - gray[:-1, :])
        straight_edges_x = np.mean(diff_x > 30.0)
        straight_edges_y = np.mean(diff_y > 30.0)
        grid_line_metric = float(straight_edges_x + straight_edges_y)
        texture_energy = float(np.mean(diff_x) + np.mean(diff_y))
        mean_r_minus_g = float(np.mean(r - g))

        white_mask = (gray > 215.0)
        white_ratio = float(np.mean(white_mask))

        # ------------------------------------------------------------------
        # Step 5: BOTANICAL FOLIAGE & CONNECTED BLADE EXTRACTION
        # ------------------------------------------------------------------
        # True chlorophyll plant foliage spectrum:
        # Green hue between 38° and 175°, saturation >= 0.15, positive ExG or dominant green channel
        foliage_green_mask = (
            (hue >= 38.0) & (hue <= 175.0) &
            (sat >= 0.15) & (val >= 20.0) &
            ((exg >= 3.5) | ((g > r + 3.0) & (g > b + 3.0)))
        )
        green_foliage_ratio = float(np.mean(foliage_green_mask))
        center_green_ratio = float(np.mean(foliage_green_mask[cy1:cy2, cx1:cx2]))

        # Necrotic / chlorotic lesion mask on leaf (blight brown, chlorotic halo, rust yellowing, powdery coating)
        lesion_raw_mask = (
            (
                (hue >= 15.0) & (hue <= 55.0) &
                (sat >= 0.12) & (val >= 20.0) & (val <= 230.0) &
                (r >= b * 0.90)
            ) |
            (
                # Pale fungal/mildew dust on leaf surface
                (sat <= 0.28) & (val >= 100.0) & (val <= 245.0) &
                (np.abs(r - g) < 30.0) & (np.abs(g - b) < 30.0)
            )
        )

        # Crucial Contiguity Constraint:
        # Lesions MUST be physically attached to or contiguous with green leaf blade tissue!
        # An animal's fur or a person's clothes in front of grass has NO internal chlorophyll.
        if cv2 is not None and green_foliage_ratio >= 0.02:
            kernel_size = max(5, int(min(h, w) * 0.07))
            if kernel_size % 2 == 0:
                kernel_size += 1
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            green_dilated = cv2.dilate(foliage_green_mask.astype(np.uint8), kernel).astype(bool)
            valid_lesion_mask = lesion_raw_mask & green_dilated
        else:
            # Fallback if cv2 unavailable: only allow lesions if green foliage is substantial
            valid_lesion_mask = lesion_raw_mask if green_foliage_ratio >= 0.15 else (lesion_raw_mask & foliage_green_mask)

        # Combined leaf coverage:
        if green_foliage_ratio >= 0.025:
            combined_leaf_mask = foliage_green_mask | valid_lesion_mask
        else:
            combined_leaf_mask = foliage_green_mask

        leaf_coverage_ratio = float(np.mean(combined_leaf_mask))
        center_leaf_ratio = float(np.mean(combined_leaf_mask[cy1:cy2, cx1:cx2]))

        # ------------------------------------------------------------------
        # Step 6: NON-LEAF REJECTION DETECTORS
        # ------------------------------------------------------------------

        # A. Animal Fur & Mammal Melanin Detector (Dogs, Cats, Cows, Horses, Sheep, Pets)
        # Mammal hair/coat contains eumelanin and pheomelanin (warm brown/tan, dark, or cream/white)
        # Melanin pigments have R >= G > B and negative/zero excess green (ExG <= 2.0)
        fur_mask = (
            (
                (exg <= 2.0) & (r >= g * 0.90) & (r > b + 8.0) &
                (hue >= 8.0) & (hue <= 48.0) & (sat >= 0.14)
            ) |
            (
                # Dark fur / black coat
                (val < 42.0) & (sat < 0.35)
            )
        )
        fur_ratio_center = float(np.mean(fur_mask[cy1:cy2, cx1:cx2]))
        fur_ratio_total = float(np.mean(fur_mask))

        is_animal_signature = (
            (fur_ratio_center >= 0.22 and center_green_ratio < 0.20)
            or (fur_ratio_total >= 0.25 and green_foliage_ratio < 0.08)
            or (texture_energy >= 12.0 and mean_r_minus_g >= 30.0 and green_foliage_ratio < 0.08)
        )

        if is_animal_signature:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.02,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="ANIMAL_DETECTED",
                rejection_reason="Animal or pet coat detected. AgroScan AI requires an affected plant leaf.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # B. Human Face & Skin Tone & Portrait Detector
        face_detected = False
        if cv2 is not None:
            face_cascade = cls._get_face_cascade()
            if face_cascade is not None:
                try:
                    gray_u8 = np.clip(gray, 0, 255).astype(np.uint8)
                    faces = face_cascade.detectMultiScale(gray_u8, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
                    if len(faces) > 0:
                        face_detected = True
                except Exception as e:
                    logger.debug(f"OpenCV face detection skipped: {e}")

        # Universal Skin Tone Mask (YCbCr + HSV)
        skin_mask = (
            (cb >= 77.0) & (cb <= 127.0) &
            (cr >= 133.0) & (cr <= 173.0) &
            (val >= 40.0) & (sat >= 0.12) & (sat <= 0.85)
        )
        skin_ratio_total = float(np.mean(skin_mask))
        skin_ratio_center = float(np.mean(skin_mask[cy1:cy2, cx1:cx2]))

        if face_detected or (skin_ratio_center >= 0.06) or (skin_ratio_total >= 0.08) or (skin_ratio_total >= 0.04 and center_green_ratio <= 0.15):
            stat = "FACE_DETECTED" if face_detected else "NON_LEAF_SELFIE"
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.01,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code=stat,
                rejection_reason="Human face, skin, or person detected. AgroScan AI requires a plant leaf photograph.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # C. Document / Screen / Paper / Book Detector
        if white_ratio > 0.40 and green_foliage_ratio < 0.08:
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

        # D. Urban Architecture / Building / Geometric Structural Grid / Vehicles
        if grid_line_metric > 0.05 and green_foliage_ratio < 0.08:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.02,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="BUILDING_DETECTED",
                rejection_reason="Building, room, vehicle, or geometric structural object detected.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # E. Bare Soil / Mud / Dirt
        soil_mask = (r > b + 25.0) & (g > b + 10.0) & (exg < 10.0) & (r > g * 0.9)
        soil_ratio = float(np.mean(soil_mask))
        if soil_ratio > 0.30 and green_foliage_ratio < 0.08:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.04,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="SOIL_ONLY_IMAGE",
                rejection_reason="Soil or bare ground detected without clear leaf evidence.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # F. Flower Bloom Without Visible Leaf
        flower_mask = (
            ((hue >= 310.0) | (hue <= 15.0) | ((hue >= 20.0) & (hue <= 48.0))) &
            (sat >= 0.45) & (val >= 90.0) & (g < r * 0.85)
        )
        flower_ratio = float(np.mean(flower_mask))
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

        # G. Sky / Open Landscape
        sky_mask = (b > g + 15.0) & (b > r + 30.0) & (val > 100.0)
        sky_ratio = float(np.mean(sky_mask))
        if sky_ratio > 0.35 and green_foliage_ratio < 0.08:
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.03,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code="SKY_LANDSCAPE_DETECTED",
                rejection_reason="Sky or wide landscape detected without close leaf view.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # H. Non-Plant Foreground Object with Outdoor Grass / Background Environment
        # If green exists in the image, but the central subject is completely non-green/non-leaf
        if green_foliage_ratio >= 0.10 and center_green_ratio < 0.10 and center_leaf_ratio < 0.12:
            rej_code = "ANIMAL_DETECTED" if fur_ratio_center > 0.15 else "BUILDING_DETECTED"
            return LeafValidationResult(
                is_plant=False,
                is_leaf=False,
                leaf_confidence=0.04,
                image_quality=quality.quality_score,
                usable_for_diagnosis=False,
                leaf_visibility=0.0,
                quality_metrics=quality_metrics_dict,
                status_code=rej_code,
                rejection_reason="A non-plant subject or animal was detected with green background vegetation.",
                message_en=STANDARD_REJECTION_EN,
                message_mr=STANDARD_REJECTION_MR
            )

        # I. Overall Non-Plant / Random Object / Vehicle
        if leaf_coverage_ratio < 0.07 and green_foliage_ratio < 0.03:
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
        # Step 7: LEAF CONFIDENCE CALCULATION & BOTANICAL VERIFICATION
        # ------------------------------------------------------------------
        # Leaf Structural Venation & Organic Texture
        leaf_pixels = gray[combined_leaf_mask]
        leaf_texture_std = float(np.std(leaf_pixels)) if len(leaf_pixels) > 50 else 0.0
        organic_texture_score = min(1.0, leaf_texture_std / 35.0) if (10.0 <= leaf_texture_std <= 70.0) else 0.4

        conf_coverage = min(1.0, leaf_coverage_ratio / 0.18)
        conf_center = min(1.0, center_leaf_ratio / 0.15)
        conf_spectral = min(1.0, green_foliage_ratio / 0.10)
        conf_texture = organic_texture_score

        leaf_confidence = round(
            float(0.30 * conf_coverage + 0.30 * conf_center + 0.25 * conf_spectral + 0.15 * conf_texture),
            3
        )

        # Require genuine leaf confidence, positive chlorophyll presence, and central leaf visibility
        is_leaf_valid = (
            leaf_confidence >= 0.20
            and (green_foliage_ratio >= 0.025 or center_green_ratio >= 0.03)
            and (center_leaf_ratio >= 0.10 or leaf_coverage_ratio >= 0.08)
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
                rejection_reason="Plant vegetation detected, but no distinct, clear leaf blade is discernible.",
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
