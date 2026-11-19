"""
AgroScan AI — Hugging Face Local Model Inference Service
Executes deep learning inference on local CPU/CUDA hardware with lazy loading,
temperature calibration, canonical label parsing, and execution telemetry.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image
from app.core.config import settings
from app.services.ai.image_preprocessor import ImagePreprocessor
from app.services.ai.model_registry import ModelRegistry, ModelInitializationError
from app.services.ai.confidence_calibrator import ConfidenceCalibrator

logger = logging.getLogger("agroscan.ai.hf_inference")


class HuggingFaceInferenceService:
    """
    Local-First Hugging Face Vision Inference Service.
    Runs PlantVillage MobileNetV2 and DINOv2 models locally with zero external network calls.
    """

    @classmethod
    def parse_plantvillage_label(cls, raw_label: str) -> Tuple[str, str, str, bool]:
        """
        Parses standard PlantVillage 38-class labels formatted as `<Crop>___<Condition>`.
        Returns: (crop_name, disease_name, canonical_code, is_healthy)
        """
        parts = raw_label.split("___")
        if len(parts) == 2:
            raw_crop, raw_disease = parts
        else:
            raw_crop, raw_disease = "General Plant", raw_label

        # Clean crop name
        crop = raw_crop.replace("_", " ").replace("(", "").replace(")", "").strip().title()
        if "Corn" in crop or "Maize" in crop:
            crop = "Corn (Maize)"
        elif "Pepper" in crop:
            crop = "Bell Pepper"

        # Clean disease name
        disease_clean = raw_disease.replace("_", " ").strip()
        is_healthy = "healthy" in disease_clean.lower()

        if is_healthy:
            disease_name = "Healthy Leaf (No Disease Detected)"
            code = "healthy_leaf"
        else:
            disease_name = f"{crop} {disease_clean}".title() if not disease_clean.lower().startswith(crop.lower()) else disease_clean.title()
            # Generate snake_case canonical code
            code = f"{crop.lower().split()[0]}_{disease_clean.lower()}".replace(" ", "_").replace("-", "_").replace("__", "_")

        return crop, disease_name, code, is_healthy

    @classmethod
    def predict(
        cls,
        image_bytes: bytes,
        model_id: Optional[str] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Executes local neural network prediction on the supplied leaf image.
        Returns normalized predictions, calibrated confidence, and inference duration.
        """
        t0 = time.time()
        chosen_model_id = model_id or getattr(settings, "DEFAULT_LOCAL_MODEL", "neghani/plantvillage-mobilenetv2")

        # 1. Preprocess image
        pil_image, _, meta = ImagePreprocessor.decode_and_validate(image_bytes)

        # 2. Retrieve model & processor
        model, processor, device = ModelRegistry.load_model(chosen_model_id)

        # 3. Prepare tensor input
        try:
            inputs = processor(images=pil_image, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}
        except Exception as proc_err:
            logger.warning(f"Processor transform fallback to standard tensor: {proc_err}")
            tensor = ImagePreprocessor.prepare_inference_tensor(pil_image).to(device)
            inputs = {"pixel_values": tensor}

        # 4. Execute forward pass with inference mode
        import torch
        with torch.inference_mode():
            outputs = model(**inputs)
            logits = outputs.logits

        # 5. Apply temperature scaling calibration
        raw_probs = torch.softmax(logits, dim=-1)
        raw_probs_np = raw_probs.squeeze(0).cpu().numpy()
        probs = ConfidenceCalibrator.apply_temperature_scaling(logits)
        probs_np = probs.squeeze(0).cpu().numpy()

        latency_ms = round((time.time() - t0) * 1000.0, 1)
        ModelRegistry.record_inference_metric(chosen_model_id, latency_ms)

        # 6. Retrieve id2label dictionary
        id2label = getattr(model.config, "id2label", {})
        if not id2label:
            id2label = {i: f"class_{i}" for i in range(len(probs_np))}

        # 7. Extract top-K candidates
        top_indices = probs_np.argsort()[-top_k:][::-1]
        candidates: List[Dict[str, Any]] = []

        for idx in top_indices:
            raw_label = str(id2label.get(idx, id2label.get(str(idx), f"class_{idx}")))
            crop, disease_name, code, is_healthy = cls.parse_plantvillage_label(raw_label)
            conf = round(float(probs_np[idx]), 4)
            raw_c = round(float(raw_probs_np[idx]), 4)
            candidates.append({
                "crop": crop,
                "disease_name": disease_name,
                "disease_code": code,
                "confidence": conf,
                "calibrated_score": conf,
                "raw_score": raw_c,
                "is_healthy": is_healthy,
                "raw_label": raw_label,
                "rank": len(candidates) + 1
            })

        top_pred = candidates[0]

        return {
            "status": "success",
            "provider_name": "AgroScan Local Hugging Face Engine",
            "model_id": chosen_model_id,
            "model_name": "MobileNetV2 (PlantVillage v1.1)",
            "model_revision": "v1.1",
            "commit_sha": "77e6d262dca53b818f7ad1d67088700754515639",
            "device": str(device),
            "crop": top_pred["crop"],
            "disease_name": top_pred["disease_name"],
            "disease_code": top_pred["disease_code"],
            "confidence": top_pred["confidence"],
            "calibrated_score": top_pred["calibrated_score"],
            "raw_score": top_pred["raw_score"],
            "is_healthy": top_pred["is_healthy"],
            "confidence_interpretation": ConfidenceCalibrator.interpret_confidence(top_pred["confidence"]),
            "top_candidates": candidates,
            "latency_ms": latency_ms
        }
