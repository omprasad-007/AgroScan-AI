import cv2
import numpy as np
from typing import Tuple

class ImagePreprocessor:
    """
    OpenCV preprocessing pipeline for leaf images:
    - Resize to 224x224 (MobileNetV2 / EfficientNet input size)
    - Normalize pixel values to [0, 1]
    - Background isolation via HSV color range mask
    """

    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size

    def preprocess_image(self, img_path: str) -> np.ndarray:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Could not load image at {img_path}")
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize
        resized = cv2.resize(img_rgb, self.target_size)
        
        # Normalize
        normalized = resized.astype(np.float32) / 255.0
        return normalized

    def segment_leaf_area(self, img_bgr: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        lower_green = np.array([15, 20, 20])
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        segmented = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)
        return segmented
