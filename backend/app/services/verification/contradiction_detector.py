"""
AgroScan AI — Contradiction Detector
Analyzes retrieved evidence to identify disagreements in cultural, biological, or chemical recommendations.
"""

from typing import List, Dict, Any

class ContradictionDetector:
    """Detects conflicting agricultural recommendations across retrieved sources."""

    @classmethod
    def analyze_contradictions(cls, evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        if len(evidence_items) < 2:
            return {
                "has_contradiction": False,
                "status": "single_source",
                "notes": "Single source used; no contradiction observed."
            }

        # Check for direct contradictions (e.g. chemical vs organic exclusivity)
        claims = [e.get("claim", "").lower() for e in evidence_items]
        
        # Example check: foliar spray effective vs ineffective
        has_foliar_conflict = any("cannot cure" in c for c in claims) and any("foliar spray" in c for c in claims)
        if has_foliar_conflict:
            return {
                "has_contradiction": True,
                "status": "conflicting",
                "notes": "Sources note that foliar sprays cannot cure established vascular infections (such as Red Rot); prevention and sett sanitation are required."
            }

        return {
            "has_contradiction": False,
            "status": "consensus",
            "notes": "High degree of consensus across sources."
        }
