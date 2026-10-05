from typing import Tuple, Optional
from app.services.leaf_validator import LeafValidator

class PlantDetector:
    """
    Stage 1 Plant & Leaf-Only Detection Engine.
    Powered by LeafValidator for computer-vision based leaf and non-plant verification.
    """

    @classmethod
    def verify_plant_image(cls, image_bytes: bytes) -> Tuple[Optional[bool], str, str]:
        """
        Returns (is_plant: Optional[bool], status: str, message: str)
        - Non-plant / non-leaf: (False, status_code, message)
        - Plant & Leaf: (True, "PLANT_IMAGE", "Leaf image validated successfully.")
        - Fail-Safe: (None, "VALIDATION_UNAVAILABLE", "We couldn't verify the image. Please try again.")
        """
        try:
            val_res = LeafValidator.validate_leaf_image(image_bytes)
            if not val_res.usable_for_diagnosis:
                return False, val_res.status_code, val_res.message_en
            return True, "PLANT_IMAGE", val_res.message_en
        except Exception as e:
            return None, "VALIDATION_UNAVAILABLE", "We couldn't verify the image. Please try again."

