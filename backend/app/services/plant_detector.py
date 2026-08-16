import cv2
import numpy as np
from typing import Tuple, Optional

class PlantDetector:
    """
    OpenCV based Stage 1 Plant Detection & Fail-Safe Validation Engine.
    Evaluates whether an uploaded image contains plant foliage (leaves, stems, flowers, crops, trees)
    or non-plant content (selfies, human faces, bodies, animals, buildings, vehicles, food, documents, laptops, phones, blank images).
    """

    @classmethod
    def verify_plant_image(cls, image_bytes: bytes) -> Tuple[Optional[bool], str, str]:
        """
        Returns (is_plant: Optional[bool], status: str, message: str)
        - Non-plant: (False, "NON_PLANT_IMAGE", "You have not scanned a leaf or plant. Please scan a clear photo of a leaf or plant.")
        - Plant: (True, "PLANT_IMAGE", "Plant image validated successfully.")
        - Fail-Safe: (None, "VALIDATION_UNAVAILABLE", "We couldn't verify the image. Please try again.")
        """
        if not image_bytes or len(image_bytes) < 100:
            return False, "NON_PLANT_IMAGE", "You have not scanned a leaf or plant. Please scan a clear photo of a leaf or plant."

        try:
            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if img is None:
                return False, "NON_PLANT_IMAGE", "You have not scanned a leaf or plant. Please scan a clear photo of a leaf or plant."

            h, w, c = img.shape
            total_pixels = h * w

            # Convert BGR to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # 1. Vegetation HSV Color Mask (Green + Yellowish-Green + Brown Leaf Lesions)
            lower_green = np.array([15, 25, 25])
            upper_green = np.array([85, 255, 255])
            green_mask = cv2.inRange(hsv, lower_green, upper_green)

            # 2. Skin-tone mask (Human faces, hands, selfies, body photos)
            lower_skin1 = np.array([0, 30, 60])
            upper_skin1 = np.array([20, 150, 255])
            lower_skin2 = np.array([160, 30, 60])
            upper_skin2 = np.array([180, 150, 255])
            skin_mask1 = cv2.inRange(hsv, lower_skin1, upper_skin1)
            skin_mask2 = cv2.inRange(hsv, lower_skin2, upper_skin2)
            skin_mask = cv2.bitwise_or(skin_mask1, skin_mask2)

            green_pixels = np.count_nonzero(green_mask)
            skin_pixels = np.count_nonzero(skin_mask)

            green_ratio = green_pixels / total_pixels
            skin_ratio = skin_pixels / total_pixels

            # Decision Logic:
            # Rejection 1: Skin-tone ratio > 25% (Human face / selfie / body photo)
            if skin_ratio > 0.25 and green_ratio < 0.20:
                return False, "NON_PLANT_IMAGE", "You have not scanned a leaf or plant. Please scan a clear photo of a leaf or plant."

            # Rejection 2: Vegetation ratio < 6% (Laptop, phone, building, car, animal, food, document, screenshot, blank)
            if green_ratio < 0.06:
                return False, "NON_PLANT_IMAGE", "You have not scanned a leaf or plant. Please scan a clear photo of a leaf or plant."

            # Valid plant foliage/crop image
            return True, "PLANT_IMAGE", "Plant image validated successfully."

        except Exception as e:
            # Rule Fail-Safe: Never assume an image is a plant when validation encounters an error
            return None, "VALIDATION_UNAVAILABLE", "We couldn't verify the image. Please try again."
