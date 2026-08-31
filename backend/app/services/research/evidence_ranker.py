"""
AgroScan AI — Evidence Ranker
Computes weighted composite scores for all candidate evidence items using:
Final Score = (Authority * 0.40) + (Relevance * 0.30) + (Recency * 0.15) + (Evidence Quality * 0.15)
"""

from typing import List, Dict, Any

class EvidenceRanker:
    """Ranks and prioritizes evidence objects based on multi-dimensional quality metrics."""

    WEIGHT_AUTHORITY = 0.40
    WEIGHT_RELEVANCE = 0.30
    WEIGHT_RECENCY = 0.15
    WEIGHT_EVIDENCE_QUALITY = 0.15

    @classmethod
    def calculate_score(cls, item: Dict[str, Any]) -> float:
        auth = float(item.get("authority_score", 0.85))
        rel = float(item.get("relevance_score", 0.70))
        rec = float(item.get("recency_score", 0.80))
        ev_q = float(item.get("evidence_score", 0.85))

        final_score = (
            (auth * cls.WEIGHT_AUTHORITY) +
            (rel * cls.WEIGHT_RELEVANCE) +
            (rec * cls.WEIGHT_RECENCY) +
            (ev_q * cls.WEIGHT_EVIDENCE_QUALITY)
        )
        return round(final_score, 4)

    @classmethod
    def rank_evidence(cls, evidence_items: List[Dict[str, Any]], top_k: int = 4) -> List[Dict[str, Any]]:
        scored = []
        for item in evidence_items:
            scored_item = dict(item)
            scored_item["final_score"] = cls.calculate_score(item)
            scored.append(scored_item)

        # Sort descending by final score
        sorted_items = sorted(scored, key=lambda x: x["final_score"], reverse=True)
        return sorted_items[:top_k]
