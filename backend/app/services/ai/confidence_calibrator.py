"""
AgroScan AI — Confidence Calibration & Uncertainty Handler
Implements temperature scaling on neural network logits, configurable
decision thresholds, model agreement evaluation, and uncertainty handling.
"""

import math
import logging
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from app.core.config import settings

logger = logging.getLogger("agroscan.ai.calibrator")


class ConfidenceCalibrator:
    """
    Evaluates raw probabilities from local models and external providers.
    Applies temperature scaling, maps confidence interpretations,
    and detects diagnostic disagreement.
    """

    DEFAULT_TEMPERATURE: float = 0.8845  # Empirical temperature from PlantVillage validation set

    @classmethod
    def apply_temperature_scaling(cls, logits: Any, temperature: Optional[float] = None) -> Any:
        """
        Scales raw neural network logits by temperature T before softmax.
        T < 1.0 increases discriminative margin for well-calibrated models.
        T > 1.0 softens overconfident distributions.
        """
        t = temperature or getattr(settings, "CONFIDENCE_CALIBRATION_TEMPERATURE", cls.DEFAULT_TEMPERATURE)
        if t <= 0.0:
            t = 1.0

        if hasattr(logits, "softmax"):  # PyTorch Tensor
            import torch
            scaled_logits = logits / t
            return torch.softmax(scaled_logits, dim=-1)

        arr = np.array(logits, dtype=np.float32)
        scaled = arr / t
        exp_arr = np.exp(scaled - np.max(scaled, axis=-1, keepdims=True))
        return exp_arr / np.sum(exp_arr, axis=-1, keepdims=True)

    @classmethod
    def interpret_confidence(cls, confidence: float) -> str:
        """Categorizes calibrated confidence into clear risk-aware bands."""
        high_thresh = getattr(settings, "HIGH_CONFIDENCE_THRESHOLD", 0.70)
        mod_thresh = getattr(settings, "MODERATE_CONFIDENCE_THRESHOLD", 0.50)

        if confidence >= high_thresh:
            return "HIGH_CONFIDENCE"
        elif confidence >= mod_thresh:
            return "MODERATE_CONFIDENCE"
        else:
            return "LOW_CONFIDENCE_UNCERTAIN"

    @classmethod
    def evaluate_model_agreement(
        cls,
        predictions: List[Dict[str, Any]]
    ) -> Tuple[str, float, Optional[str]]:
        """
        Compares multiple model / provider predictions.
        Returns:
            agreement_status: "UNANIMOUS", "MAJORITY", "SINGLE_SOURCE", "CONFLICTING"
            consensus_score: weighted agreement ratio (0.0 to 1.0)
            uncertainty_note: human-readable caution when models diverge
        """
        valid_preds = [p for p in predictions if p and p.get("status") == "success"]

        if not valid_preds:
            return "NO_PREDICTIONS", 0.0, "No diagnostic model succeeded in evaluating this image."

        if len(valid_preds) == 1:
            source = valid_preds[0].get("provider_name", "Local ML Engine")
            conf = valid_preds[0].get("confidence", 0.5)
            return (
                "SINGLE_SOURCE",
                conf,
                f"Single-source preliminary diagnosis from {source}. Verification by an agronomist is recommended for field intervention."
            )

        # Count disease code votes
        disease_votes: Dict[str, int] = {}
        healthy_votes: Dict[bool, int] = {True: 0, False: 0}

        for pred in valid_preds:
            code = pred.get("disease_code", "unknown")
            is_healthy = pred.get("is_healthy", False)
            disease_votes[code] = disease_votes.get(code, 0) + 1
            healthy_votes[is_healthy] += 1

        total = len(valid_preds)
        max_disease_votes = max(disease_votes.values())
        top_code = max(disease_votes, key=disease_votes.get)  # type: ignore

        # Check for direct opposition on healthy vs diseased
        if healthy_votes[True] > 0 and healthy_votes[False] > 0:
            return (
                "CONFLICTING",
                0.40,
                "Diagnostic disagreement: one model detected healthy foliage while another detected pathology. Please capture a clearer close-up of the affected area."
            )

        if max_disease_votes == total:
            return "UNANIMOUS", 1.0, None

        agreement_ratio = max_disease_votes / total
        if agreement_ratio >= 0.5:
            return (
                "MAJORITY",
                round(agreement_ratio, 2),
                f"Majority agreement ({max_disease_votes} of {total} models). Alternative possibilities should be considered."
            )

        return (
            "CONFLICTING",
            round(agreement_ratio, 2),
            "Diagnostic models produced conflicting assessments. Physical agronomic inspection is recommended."
        )
