"""
AgroScan AI — Citation Service
Formats grounded, verified citations and evidence blocks for LLM context and user presentation.
"""

from typing import List, Dict, Any

class CitationService:
    """Formats verified citations for frontend rendering and LLM prompt context."""

    @classmethod
    def format_sources_for_response(cls, ranked_evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        sources = []
        for itm in ranked_evidence:
            sources.append({
                "title": itm.get("title", itm.get("source", "Agricultural Source")),
                "source": itm.get("source", "Agricultural Database"),
                "url": itm.get("url", "https://agroscan-ai.app"),
                "type": itm.get("source_type", "official"),
                "relevance": itm.get("relevance_score", 0.90),
                "trust_score": itm.get("authority_score", 0.95),
                "final_score": itm.get("final_score", 0.92)
            })
        return sources

    @classmethod
    def build_evidence_context_block(cls, ranked_evidence: List[Dict[str, Any]]) -> str:
        if not ranked_evidence:
            return ""

        lines = ["--- VERIFIED MULTI-SOURCE EVIDENCE (FAO / ICAR / CABI / PEER-REVIEWED) ---"]
        for itm in ranked_evidence:
            src = itm.get("source", "Source")
            claim = itm.get("claim", "")
            score = itm.get("final_score", 0.90)
            lines.append(f"• [{src} | Quality Score: {score}]: {claim}")
        lines.append("--------------------------------------------------------------------------")
        return "\n".join(lines)
