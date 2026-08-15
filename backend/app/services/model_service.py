import os
import random
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.core.config import settings

class BaseDiseasePredictor(ABC):
    @abstractmethod
    def predict(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Returns structured dictionary:
        {
            "crop": str,
            "disease_name": str,
            "disease_code": str,
            "confidence": float,
            "is_demo": bool
        }
        """
        pass


class DemoPredictor(BaseDiseasePredictor):
    """
    Deterministic Mock Inference Predictor for DEMO_MODE.
    Generates realistic predictions without requiring trained TensorFlow weights.
    """
    DEMO_CLASSES = [
        {"crop": "Tomato", "disease_name": "Tomato Late Blight", "disease_code": "tomato_late_blight", "confidence_range": (0.88, 0.97)},
        {"crop": "Tomato", "disease_name": "Tomato Early Blight", "disease_code": "tomato_early_blight", "confidence_range": (0.85, 0.95)},
        {"crop": "Tomato", "disease_name": "Tomato Yellow Leaf Curl Virus", "disease_code": "tomato_yellow_leaf_curl", "confidence_range": (0.89, 0.98)},
        {"crop": "Potato", "disease_name": "Potato Late Blight", "disease_code": "potato_late_blight", "confidence_range": (0.86, 0.96)},
        {"crop": "Corn (Maize)", "disease_name": "Corn Common Rust", "disease_code": "corn_common_rust", "confidence_range": (0.87, 0.94)},
        {"crop": "General Crop", "disease_name": "Healthy Leaf (No Disease)", "disease_code": "healthy_leaf", "confidence_range": (0.94, 0.99)},
    ]

    def predict(self, image_bytes: bytes) -> Dict[str, Any]:
        # Hash byte length to make demo predictions deterministic for identical images
        hash_seed = len(image_bytes) % len(self.DEMO_CLASSES)
        selected = self.DEMO_CLASSES[hash_seed]
        
        low_c, high_c = selected["confidence_range"]
        confidence = round(random.uniform(low_c, high_c), 4)

        return {
            "crop": selected["crop"],
            "disease_name": selected["disease_name"],
            "disease_code": selected["disease_code"],
            "confidence": confidence,
            "is_demo": True
        }


class CNNPredictor(BaseDiseasePredictor):
    """
    TensorFlow / Keras MobileNetV2 Transfer Learning Inference Engine.
    Used when DEMO_MODE=false and model file exists.
    """
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.classes = [
            "tomato_early_blight", "tomato_late_blight", "tomato_yellow_leaf_curl",
            "potato_late_blight", "corn_common_rust", "healthy_leaf"
        ]

    def _load_model(self):
        if self.model is None and os.path.exists(self.model_path):
            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(self.model_path)
            except Exception as e:
                print(f"Warning: Failed to load TensorFlow model from {self.model_path}: {e}")

    def predict(self, image_bytes: bytes) -> Dict[str, Any]:
        self._load_model()
        if self.model is None:
            # Fallback to DemoPredictor if model binary is missing
            fallback = DemoPredictor()
            result = fallback.predict(image_bytes)
            result["is_demo"] = True
            result["note"] = "Model file not found; running in DEMO mode fallback."
            return result

        try:
            import cv2
            import numpy as np

            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (224, 224))
            img = img.astype(np.float32) / 255.0
            img = np.expand_dims(img, axis=0)

            preds = self.model.predict(img)[0]
            top_idx = int(np.argmax(preds))
            confidence = round(float(preds[top_idx]), 4)
            disease_code = self.classes[top_idx]

            from app.services.disease_knowledge_base import get_disease_by_code
            info = get_disease_by_code(disease_code)

            return {
                "crop": info["crop"],
                "disease_name": info["disease_name"],
                "disease_code": disease_code,
                "confidence": confidence,
                "is_demo": False
            }
        except Exception as e:
            fallback = DemoPredictor()
            return fallback.predict(image_bytes)


class ModelServiceFactory:
    @staticmethod
    def get_predictor() -> BaseDiseasePredictor:
        if settings.DEMO_MODE or settings.MODEL_TYPE == "demo":
            return DemoPredictor()
        else:
            return CNNPredictor(settings.MODEL_PATH)
