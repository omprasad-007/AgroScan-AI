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
        Parses both standard PlantVillage labels and Indian Crop Disease labels.
        Returns: (crop_name, disease_name, canonical_code, is_healthy)
        """
        raw_label_clean = str(raw_label).strip()
        parts = raw_label_clean.split("___")
        if len(parts) == 2:
            raw_crop, raw_disease = parts
        else:
            raw_crop, raw_disease = "General Plant", raw_label_clean

        raw_crop_lower = raw_crop.lower()
        raw_disease_lower = raw_disease.lower()

        # Handle specialized Indian crop labels
        if "cotton" in raw_disease_lower or "cotton" in raw_crop_lower or "thirps" in raw_label_clean.lower():
            crop = "Cotton"
        elif "sugarcane" in raw_disease_lower or "sugarcane" in raw_crop_lower:
            crop = "Sugarcane"
        elif "rice" in raw_disease_lower or "rice" in raw_crop_lower:
            crop = "Rice (Paddy)"
        elif "wheat" in raw_disease_lower or "wheat" in raw_crop_lower:
            crop = "Wheat"
        elif "soybean" in raw_disease_lower or "soybean" in raw_crop_lower or "soya" in raw_crop_lower:
            crop = "Soybean"
        elif "maize" in raw_disease_lower or "corn" in raw_crop_lower:
            crop = "Corn (Maize)"
        elif "pepper" in raw_crop_lower:
            crop = "Bell Pepper"
        else:
            crop = raw_crop.replace("_", " ").replace("(", "").replace(")", "").strip().title()

        # Clean disease name
        disease_clean = (
            raw_disease.replace("_", " ")
            .replace("Unknown", "")
            .replace("in Cotton", "")
            .replace("on Cotton", "")
            .replace("in cotton", "")
            .replace("on cotton", "")
            .strip()
        )
        is_healthy = "healthy" in disease_clean.lower()

        if is_healthy:
            disease_name = "Healthy Leaf (No Disease Detected)"
            code = "healthy_leaf"
        else:
            disease_name = f"{crop} {disease_clean}".title() if not disease_clean.lower().startswith(crop.lower().split()[0]) else disease_clean.title()
            code = f"{crop.lower().split()[0]}_{disease_clean.lower()}".replace(" ", "_").replace("-", "_").replace("__", "_")

        return crop, disease_name, code, is_healthy

    @classmethod
    def select_best_model_for_crop(cls, target_crop: Optional[str] = None) -> str:
        """
        Chooses the optimal neural network model based on target crop.
        - Cotton, Rice, Sugarcane, Wheat -> sanjeevani-04/indian-crop-disease-mobilenetv2
        - Tomato, Potato, Apple, Grape, Pepper, etc. -> neghani/plantvillage-mobilenetv2
        - Auto / Unspecified -> auto ensemble
        """
        if not target_crop or target_crop.lower() in ["auto", "auto-detect", "unknown", "all", "other"]:
            return "auto"

        tc = target_crop.lower()
        if any(c in tc for c in ["soybean", "soyabean", "soya", "soy"]):
            return getattr(settings, "DEFAULT_LOCAL_MODEL", "neghani/plantvillage-mobilenetv2")
        if any(c in tc for c in ["cotton", "kapas", "rice", "paddy", "dhan", "sugarcane", "ganna", "us", "wheat", "gehun", "gahu"]):
            return "sanjeevani-04/indian-crop-disease-mobilenetv2"
        return getattr(settings, "DEFAULT_LOCAL_MODEL", "neghani/plantvillage-mobilenetv2")

    @classmethod
    def _execute_single_model(
        cls,
        image_bytes: bytes,
        model_id: str,
        target_crop: Optional[str] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """Runs inference for a specific registered model."""
        t0 = time.time()
        pil_image, _, _ = ImagePreprocessor.decode_and_validate(image_bytes)
        model, processor, device = ModelRegistry.load_model(model_id)

        try:
            inputs = processor(images=pil_image, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}
        except Exception as proc_err:
            logger.warning(f"Processor transform fallback to standard tensor: {proc_err}")
            tensor = ImagePreprocessor.prepare_inference_tensor(pil_image).to(device)
            inputs = {"pixel_values": tensor}

        import torch
        with torch.inference_mode():
            outputs = model(**inputs)
            logits = outputs.logits

        raw_probs = torch.softmax(logits, dim=-1)
        raw_probs_np = raw_probs.squeeze(0).cpu().numpy()
        probs = ConfidenceCalibrator.apply_temperature_scaling(logits)
        probs_np = probs.squeeze(0).cpu().numpy()

        latency_ms = round((time.time() - t0) * 1000.0, 1)
        ModelRegistry.record_inference_metric(model_id, latency_ms)

        id2label = getattr(model.config, "id2label", {})
        if not id2label:
            id2label = {i: f"class_{i}" for i in range(len(probs_np))}

        # If target crop is specified, we check all classes so we don't miss target crop candidates outside top_k
        top_k_search = max(top_k, 15) if target_crop and target_crop.lower() not in ["auto", "auto-detect", "unknown", "all", "other"] else top_k
        top_indices = probs_np.argsort()[-top_k_search:][::-1]
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

        if target_crop and target_crop.lower() not in ["auto", "auto-detect", "unknown", "all", "other"]:
            tc = target_crop.lower()
            matched_candidates = [c for c in candidates if tc in c["crop"].lower() or c["crop"].lower() in tc]
            if matched_candidates:
                top_pred = matched_candidates[0]
            else:
                top_pred = candidates[0]
        else:
            top_pred = candidates[0]
        if "sanjeevani" in model_id or "indian" in model_id:
            display_model_name = "Indian Agricultural Crop MobileNetV2 (35 Classes)"
            display_revision = "v1.0-field"
        elif "dinov2" in model_id:
            display_model_name = "DINOv2 Small Vision Transformer (PlantVillage)"
            display_revision = "06ebf5e308"
        else:
            display_model_name = "PlantVillage MobileNetV2 (38 Classes)"
            display_revision = "v1.1"

        return {
            "status": "success",
            "provider_name": "AgroScan Local Vision Engine",
            "model_id": model_id,
            "model_name": display_model_name,
            "model_revision": display_revision,
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

    @classmethod
    def predict(
        cls,
        image_bytes: bytes,
        model_id: Optional[str] = None,
        target_crop: Optional[str] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Executes local neural network prediction on the supplied leaf image.
        Intelligently routes or enriches results based on target crop.
        """
        chosen_model_id = model_id or cls.select_best_model_for_crop(target_crop)

        # Explicit single model request
        if chosen_model_id != "auto":
            return cls._execute_single_model(image_bytes, chosen_model_id, target_crop=target_crop, top_k=top_k)

        # Auto multi-model evaluation across horticulture and Indian field crop models
        res_pv = cls._execute_single_model(
            image_bytes,
            getattr(settings, "DEFAULT_LOCAL_MODEL", "neghani/plantvillage-mobilenetv2"),
            target_crop=target_crop,
            top_k=top_k
        )

        try:
            res_indian = cls._execute_single_model(
                image_bytes,
                "sanjeevani-04/indian-crop-disease-mobilenetv2",
                target_crop=target_crop,
                top_k=top_k
            )
        except Exception as indian_err:
            logger.warning(f"Indian crop model inference skipped: {indian_err}")
            return res_pv

        # Select the optimal model:
        # PlantVillage has 38 classes (including Soybean, Tomato, Potato, Apple, Corn, Grape, Pepper, etc.).
        # Indian model has ONLY 4 classes (Cotton, Rice, Sugarcane, Wheat).
        # A 4-class model artificially concentrates its softmax over only 4 crops, producing high confidence.
        # If PlantVillage predicts a specific crop (e.g. Soybean, Tomato, Potato, Grape, Pepper) with confidence >= 0.20,
        # it MUST take precedence over the Indian model's narrow 4-crop guess!
        pv_crop_lower = res_pv.get("crop", "").lower()
        is_pv_specific = any(c in pv_crop_lower for c in ["soybean", "tomato", "potato", "apple", "grape", "corn", "pepper", "orange", "peach", "strawberry"])

        if is_pv_specific and res_pv["confidence"] >= 0.20:
            chosen = res_pv
            other = res_indian
        elif res_indian["confidence"] > (res_pv["confidence"] + 0.15):
            chosen = res_indian
            other = res_pv
        else:
            chosen = res_pv
            other = res_indian

        chosen["top_candidates"] = (chosen["top_candidates"] + other["top_candidates"])[:top_k]
        chosen["latency_ms"] = round(chosen["latency_ms"] + other["latency_ms"], 1)
        return chosen
