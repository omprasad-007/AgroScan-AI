"""
AgroScan AI — Confidence Service
Calculates multi-dimensional evidence confidence scores.
"""

from typing import List, Dict, Any

class ConfidenceService:
    """Computes evidence confidence based on authority, relevance, and agreement."""

    @classmethod
    def calculate_confidence(
        cls,
        evidence_items: List[Dict[str, Any]],
        has_contradictions: bool = False
    ) -> float:
        if not evidence_items:
            return 0.70

        avg_score = sum(item.get("final_score", 0.85) for item in evidence_items) / len(evidence_items)
        if has_contradictions:
            avg_score -= 0.10

        return round(max(0.50, min(0.98, avg_score)), 2)
