"""
AgroScan AI — Agricultural Research Pipeline Service
Coordinates Source Routing, Evidence Extraction, Ranking, Deduplication, and Citation Delivery.
"""

from typing import Dict, Any, List, Optional
from app.services.research.source_router import SourceRouter
from app.services.research.evidence_extractor import EvidenceExtractor
from app.services.research.evidence_ranker import EvidenceRanker
from app.services.research.source_deduplicator import SourceDeduplicator
from app.services.research.citation_service import CitationService

class ResearchService:
    """End-to-end multi-source research pipeline orchestrator."""

    @classmethod
    def conduct_research(
        cls,
        query: str,
        plant_name: Optional[str] = None,
        disease_name: Optional[str] = None,
        intent: Optional[str] = None,
        research_mode: str = "auto"
    ) -> Dict[str, Any]:
        # 1. Source Routing
        target_categories = SourceRouter.route_sources(
            query=query,
            plant_name=plant_name,
            disease_name=disease_name,
            intent=intent or "GENERAL_AGRICULTURE",
            research_mode=research_mode
        )

        # 2. Evidence Extraction
        raw_evidence = EvidenceExtractor.extract_evidence_for_categories(
            categories=target_categories,
            query=query,
            plant_name=plant_name,
            disease_name=disease_name
        )

        # 3. Source Deduplication
        unique_evidence = SourceDeduplicator.deduplicate(raw_evidence)

        # 4. Evidence Ranking (4-component formula)
        top_k = 5 if research_mode == "deep_research" else 3 if research_mode == "quick" else 4
        ranked_evidence = EvidenceRanker.rank_evidence(unique_evidence, top_k=top_k)

        # 5. Build Context Blocks & Structured Sources
        formatted_sources = CitationService.format_sources_for_response(ranked_evidence)
        evidence_text = CitationService.build_evidence_context_block(ranked_evidence)

        # 6. Source Agreement Estimation
        high_auth_count = sum(1 for s in ranked_evidence if s.get("authority_score", 0) >= 0.95)
        agreement_level = "high" if high_auth_count >= 2 else "medium" if high_auth_count == 1 else "diverse"
        confidence_avg = (
            sum(s.get("final_score", 0.90) for s in ranked_evidence) / len(ranked_evidence)
            if ranked_evidence else 0.85
        )

        return {
            "query": query,
            "intent": intent,
            "plant_name": plant_name,
            "disease_name": disease_name,
            "research_mode": research_mode,
            "sources": formatted_sources,
            "evidence_text": evidence_text,
            "ranked_evidence": ranked_evidence,
            "source_agreement": agreement_level,
            "evidence_confidence": round(confidence_avg, 2)
        }
