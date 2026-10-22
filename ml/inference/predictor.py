import os
import time
from typing import Dict, Any
from ml.preprocessing.dataset_preprocessor import DatasetPreprocessor

class CustomMLPredictor:
    """
    Inference Engine Wrapper for Custom AgroScan MobileNetV2 / ResNet Crop Disease Model.
    Enables comparing or replacing external API predictions with locally trained computer vision models.
    """
    def __init__(self, model_path: str = "ml/models/mobilenet_agroscan.h5"):
        self.model_path = model_path
        self.preprocessor = DatasetPreprocessor()
        self.model = None
        self.classes = [
            "tomato_early_blight",
            "tomato_late_blight",
            "tomato_yellow_leaf_curl",
            "potato_late_blight",
            "corn_common_rust",
            "healthy_leaf"
        ]

    def predict(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Executes local Computer Vision model inference and tracks inference time in milliseconds.
        """
        start_time = time.time()
        
        # Preprocess input image to (1, 224, 224, 3)
        processed_img = self.preprocessor.preprocess_image(image_bytes)

        if not os.path.exists(self.model_path) or self.model is None:
            raise RuntimeError(
                f"Model file {self.model_path} is not compiled. "
                "Train or place model weights before invoking local ML inference."
            )

        inference_time_ms = round((time.time() - start_time) * 1000, 2)
        preds = self.model.predict(processed_img)[0]
        top_idx = int(preds.argmax())
        code = self.classes[top_idx]
        conf = round(float(preds[top_idx]), 3)

        return {
            "predictor_type": "Custom Computer Vision ML Model",
            "model_path": self.model_path,
            "crop_detected": code.split("_")[0].capitalize(),
            "disease_name": code.replace("_", " ").title(),
            "disease_code": code,
            "confidence_score": conf,
            "inference_time_ms": inference_time_ms,
            "is_custom_ml": True
        }

