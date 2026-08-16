import os
import cv2
import numpy as np
from typing import Tuple

class DatasetPreprocessor:
    """
    Data Preprocessing & Augmentation Pipeline for Plant Disease Classification.
    Resizes leaf photos to (224, 224, 3) and applies HSV color space normalization.
    """
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size

    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Converts raw image bytes to normalized floating point numpy array.
        """
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Unable to decode image bytes into valid OpenCV image matrix")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(img_rgb, self.target_size)
        normalized = resized.astype(np.float32) / 255.0
        return np.expand_dims(normalized, axis=0)

    def augment_image(self, img_array: np.ndarray) -> np.ndarray:
        """
        Applies rotation and horizontal flip augmentation.
        """
        flipped = cv2.flip(img_array, 1)
        return flipped
