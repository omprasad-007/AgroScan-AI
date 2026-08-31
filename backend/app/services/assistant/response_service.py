"""
AgroScan AI — Response Service
Structures final responses with verified citations, confidence scores, and context flags.
"""

from typing import Dict, Any, List

class ResponseService:
    """Formats standardized API response structures."""

    @classmethod
    def build_research_payload(
        cls,
        answer: str,
        intent: str,
        sources: List[Dict[str, Any]],
        confidence: float,
        source_agreement: str,
        context_meta: Dict[str, Any],
        weather_used: bool = False
    ) -> Dict[str, Any]:
        return {
            "answer": answer,
            "intent": intent,
            "confidence": confidence,
            "evidence_confidence": confidence,
            "source_agreement": source_agreement,
            "sources": sources,
            "evidence": {
                "source_agreement": source_agreement,
                "sources_used": len(sources)
            },
            "context_used": {
                "scan": context_meta.get("has_valid_scan", False),
                "plant": bool(context_meta.get("plant_name")),
                "disease": bool(context_meta.get("disease_name")),
                "weather": weather_used,
                "location": bool(context_meta.get("location")),
                "rag": True,
                "web": len(sources) > 0,
                "research": any(s.get("type") in ["peer_reviewed_paper", "research", "scientific"] for s in sources)
            }
        }
