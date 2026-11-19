"""
AgroScan AI — Hybrid Prediction Orchestrator
Executes the strict 10-step hybrid diagnostic workflow:
Image Validation -> Crop Verification -> Local HF Inference -> External API Query ->
Consensus Fusion -> Calibrated Decision Rules -> Normalized Diagnostic Output.
"""

import asyncio
import logging
import time
from typing import Dict, Any, List, Optional, Tuple

from app.core.config import settings
from app.services.leaf_validator import LeafValidator, LeafValidationResult
from app.services.severity_analyzer import SeverityAnalyzer
from app.services.weather_service import WeatherRiskService
from app.services.ai.image_preprocessor import ImagePreprocessor, ImagePreprocessingError
from app.services.ai.crop_registry import CropRegistry, CropSupportStatus, CropProfile
from app.services.ai.hf_inference_service import HuggingFaceInferenceService
from app.services.ai.confidence_calibrator import ConfidenceCalibrator
from app.services.ai.result_normalizer import ResultNormalizer
from app.services.providers.kindwise_provider import KindwisePlantIdProvider
from app.services.providers.gemini_vision_provider import GeminiVisionProvider

logger = logging.getLogger("agroscan.ai.orchestrator")


class HybridPredictionOrchestrator:
    """
    Production Hybrid AI Orchestration Engine.
    Executes local deep learning models in concert with external botanical APIs.
    Enforces honest uncertainty handling and explicit unsupported-crop management.
    """

    def __init__(self):
        self.kindwise_provider = KindwisePlantIdProvider()
        self.gemini_provider = GeminiVisionProvider()

    async def orchestrate_scan(
        self,
        image_bytes: bytes,
        scan_id: str,
        target_crop: Optional[str] = None,
        weather_params: Optional[Dict[str, float]] = None,
        location: Optional[Dict[str, Any]] = None,
        is_guest: bool = False,
        image_url: Optional[str] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Executes the 10-step hybrid diagnostic workflow.
        """
        t0 = time.time()
        logger.info(f"Starting hybrid scan orchestration for {scan_id} (target_crop: {target_crop})")

        # STEP 1: Verify byte integrity & basic image properties
        try:
            _, np_rgb, img_meta = ImagePreprocessor.decode_and_validate(image_bytes)
        except ImagePreprocessingError as err:
            logger.warning(f"Scan {scan_id} failed image pre-check: {err}")
            return self._build_failure_response(
                scan_id=scan_id,
                status="INVALID_IMAGE",
                reason=str(err),
                image_url=image_url
            )

        # STEP 2 & STEP 3: Stage 1 Strict Leaf Validation Gate
        val_result: LeafValidationResult = LeafValidator.validate_leaf_image(image_bytes)
        val_dict = val_result.model_dump()

        if not val_result.usable_for_diagnosis or not val_result.is_leaf:
            rejection_status = (
                "POOR_IMAGE_QUALITY"
                if val_result.status_code == "INSUFFICIENT_IMAGE_QUALITY"
                else "INVALID_IMAGE"
            )
            logger.info(f"Scan {scan_id} rejected at validation gate: {val_result.status_code}")
            return self._build_validation_rejection_response(
                scan_id=scan_id,
                status=rejection_status,
                val_result=val_result,
                image_url=image_url,
                language=language
            )

        # STEP 4: Identify and verify crop support
        support_status, crop_profile = CropRegistry.check_support(target_crop)
        logger.info(f"Crop check for '{target_crop}': {support_status} (profile: {crop_profile.id if crop_profile else None})")

        # Handle explicit unsupported crop
        if support_status == CropSupportStatus.UNSUPPORTED and crop_profile:
            logger.info(f"Scan {scan_id} is recognized as UNSUPPORTED crop: {crop_profile.common_name}")
            return self._build_unsupported_crop_response(
                scan_id=scan_id,
                crop_profile=crop_profile,
                val_dict=val_dict,
                image_url=image_url
            )

        # STEP 5 & STEP 6: Execute Local Models and Eligible External Providers
        model_predictions: List[Dict[str, Any]] = []
        provider_predictions: List[Dict[str, Any]] = []

        # Local Hugging Face Inference
        hf_success = False
        try:
            hf_res = HuggingFaceInferenceService.predict(image_bytes, target_crop=target_crop)
            if hf_res and hf_res.get("status") == "success":
                model_predictions.append(hf_res)
                hf_success = True
                logger.info(
                    f"Local HF inference succeeded: {hf_res['crop']} - {hf_res['disease_name']} "
                    f"({hf_res['confidence']:.2f}) in {hf_res['latency_ms']}ms"
                )
        except Exception as hf_err:
            logger.warning(f"Local HF model inference exception: {hf_err}")

        # External Cloud Providers (Parallel Async Call with Timeout)
        external_tasks = []
        if self.gemini_provider.is_available():
            external_tasks.append(
                self._safe_provider_call(self.gemini_provider, image_bytes, target_crop, location, language)
            )
        if self.kindwise_provider.is_available():
            external_tasks.append(
                self._safe_provider_call(self.kindwise_provider, image_bytes, target_crop, location, language)
            )

        if external_tasks:
            external_results = await asyncio.gather(*external_tasks, return_exceptions=True)
            for res in external_results:
                if isinstance(res, dict) and res.get("status") == "success":
                    provider_predictions.append(res)

        # STEP 7 & STEP 8: Normalize and Compare Results
        all_sources = model_predictions + provider_predictions

        if not all_sources:
            logger.error(f"All inference sources failed for scan {scan_id}")
            return self._build_failure_response(
                scan_id=scan_id,
                status="PROVIDER_UNAVAILABLE",
                reason="Both local AI model and external botanical services were temporarily unavailable.",
                image_url=image_url
            )

        # Evaluate consensus and agreement
        agreement_status, consensus_score, uncertainty_note = ConfidenceCalibrator.evaluate_model_agreement(all_sources)

        # Select primary candidate
        primary = model_predictions[0] if model_predictions else (provider_predictions[0] if provider_predictions else {})

        # Fallback to Gemini Vision if:
        # 1. Local model failed or is UNCERTAIN (confidence < 0.50)
        # 2. Gemini identified a crop matching user's selected non-PlantVillage crop (e.g. Mango, Sugarcane, Cotton, Rice)
        if provider_predictions:
            ext_top = provider_predictions[0]
            ext_crop = ext_top.get("plant", "")
            local_conf = float(model_predictions[0].get("confidence", 0.0)) if model_predictions else 0.0
            ext_conf = float(ext_top.get("confidence", 0.0))

            if not hf_success or local_conf < getattr(settings, "MODERATE_CONFIDENCE_THRESHOLD", 0.50):
                primary = ext_top
                logger.info(f"Local model uncertain ({local_conf:.2f}); seamlessly falling back to Gemini Vision ({ext_conf:.2f} - {ext_crop})")
            elif ext_crop and crop_profile and ext_crop.lower() in crop_profile.common_name.lower():
                primary = ext_top
            elif target_crop and target_crop.lower() not in ["auto", "crop", "general"] and ext_crop.lower() in target_crop.lower():
                primary = ext_top

        plant_name = primary.get("crop") or primary.get("plant") or (crop_profile.common_name if crop_profile else "Plant")
        scientific_name = primary.get("scientific_name") or (crop_profile.scientific_name if crop_profile else "Plantae")
        disease_name = primary.get("disease_name") or primary.get("disease") or "Unknown"
        disease_code = primary.get("disease_code") or "unknown_condition"
        is_healthy = primary.get("is_healthy", False)
        calibrated_conf = float(primary.get("confidence", 0.50))

        # STEP 9: Apply Calibrated Decision Rules
        final_status = "DISEASE_DETECTED"
        if is_healthy or "healthy" in disease_code.lower():
            final_status = "HEALTHY"
        elif agreement_status == "CONFLICTING" or calibrated_conf < getattr(settings, "MODERATE_CONFIDENCE_THRESHOLD", 0.50):
            final_status = "UNCERTAIN"

        # Additional feature extractions: Lesion Severity & Weather Risk
        severity_result = SeverityAnalyzer.analyze_image_bytes(image_bytes)
        w_params = weather_params or {"temperature_c": 24.0, "humidity_pct": 78.0, "rainfall_mm": 5.0}
        weather_result = WeatherRiskService.calculate_risk(
            temp_c=w_params.get("temperature_c", 24.0),
            humidity_pct=w_params.get("humidity_pct", 78.0),
            rainfall_mm=w_params.get("rainfall_mm", 5.0),
            crop=plant_name,
            disease=disease_name
        )

        # STEP 10: Standardize Response into Part 8 Schema
        normalized_response = ResultNormalizer.normalize_diagnosis(
            scan_id=scan_id,
            status=final_status,
            image_validation=val_dict,
            plant_name=plant_name,
            scientific_name=scientific_name,
            crop_profile=crop_profile,
            disease_name=disease_name,
            disease_code=disease_code,
            confidence=calibrated_conf,
            is_healthy=is_healthy,
            model_predictions=model_predictions,
            provider_predictions=provider_predictions,
            agreement_status=agreement_status,
            consensus_score=consensus_score,
            uncertainty_note=uncertainty_note,
            severity_data=severity_result,
            weather_data=weather_result,
            image_url=image_url,
            is_guest=is_guest,
            is_demo=False
        )

        total_latency = round((time.time() - t0) * 1000.0, 1)
        logger.info(f"Scan {scan_id} completed in {total_latency}ms -> {final_status}: {plant_name} | {disease_name} ({calibrated_conf:.2f})")
        return normalized_response

    async def _safe_provider_call(self, provider: Any, image_bytes: bytes, target_crop: Optional[str], location: Optional[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Calls an external provider with a strict timeout and wraps result safely."""
        try:
            timeout_sec = 25.0
            res = await asyncio.wait_for(
                provider.diagnose(image_bytes=image_bytes, plant_name=target_crop, location=location, language=language),
                timeout=timeout_sec
            )
            return res.model_dump() if hasattr(res, "model_dump") else dict(res)
        except asyncio.TimeoutError:
            logger.warning(f"External provider {getattr(provider, 'name', 'api')} timed out.")
            return {"provider": getattr(provider, "name", "external"), "status": "timeout"}
        except Exception as err:
            logger.warning(f"External provider {getattr(provider, 'name', 'api')} error: {err}")
            return {"provider": getattr(provider, "name", "external"), "status": "error", "error": str(err)}

    def _build_unsupported_crop_response(self, scan_id: str, crop_profile: CropProfile, val_dict: Dict[str, Any], image_url: Optional[str]) -> Dict[str, Any]:
        return ResultNormalizer.normalize_diagnosis(
            scan_id=scan_id,
            status="UNSUPPORTED_CROP",
            image_validation=val_dict,
            plant_name=crop_profile.common_name,
            scientific_name=crop_profile.scientific_name,
            crop_profile=crop_profile,
            disease_name="Unsupported Pathology Calibration",
            disease_code="unsupported_crop",
            confidence=0.0,
            is_healthy=False,
            model_predictions=[],
            provider_predictions=[],
            agreement_status="NOT_APPLICABLE",
            consensus_score=0.0,
            uncertainty_note=f"Calibrated disease models are currently unavailable for {crop_profile.common_name}.",
            image_url=image_url
        )

    def _build_validation_rejection_response(self, scan_id: str, status: str, val_result: LeafValidationResult, image_url: Optional[str], language: str) -> Dict[str, Any]:
        msg = val_result.message_mr if language == "mr" else val_result.message_en
        return {
            "id": scan_id,
            "scan_id": scan_id,
            "status": status,
            "image_validation_status": val_result.status_code,
            "message": msg,
            "rejection_reason": val_result.rejection_reason or msg,
            "usable_for_diagnosis": False,
            "quality_metrics": val_result.quality_metrics,
            "image_url": image_url,
            "confidence": 0.0,
            "plant": "Unknown",
            "disease": "Not Evaluated",
            "healthy_status": False,
            "recommendation": {
                "organic_treatment": "Please retake a clear, focused photograph of a single plant leaf in daylight.",
                "chemical_treatment": "No chemical application should be performed on unverified samples.",
                "prevention": "Ensure the camera lens is clean and the leaf fills the majority of the camera frame.",
                "disclaimer": "Invalid or non-leaf image rejected at validation gate."
            }
        }

    def _build_failure_response(self, scan_id: str, status: str, reason: str, image_url: Optional[str]) -> Dict[str, Any]:
        return {
            "id": scan_id,
            "scan_id": scan_id,
            "status": status,
            "image_validation_status": "FAILED",
            "message": reason,
            "rejection_reason": reason,
            "usable_for_diagnosis": False,
            "confidence": 0.0,
            "plant": "Unknown",
            "disease": "Diagnosis Unavailable",
            "healthy_status": False,
            "image_url": image_url,
            "recommendation": {
                "organic_treatment": "Diagnosis could not be completed. Please retry in a few moments.",
                "chemical_treatment": "Consult a qualified agricultural professional before chemical treatment.",
                "prevention": "Inspect plants physically for localized discoloration or pests.",
                "disclaimer": "Analysis engine unavailable."
            }
        }


# Singleton orchestrator instance
orchestrator = HybridPredictionOrchestrator()
