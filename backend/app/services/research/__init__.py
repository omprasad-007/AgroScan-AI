"""
AgroScan AI Research Package
"""

from app.services.research.research_service import ResearchService
from app.services.research.source_router import SourceRouter
from app.services.research.source_registry import SourceCategory, AUTHORITY_WEIGHTS, VERIFIED_RESEARCH_ENTRIES
from app.services.research.evidence_extractor import EvidenceExtractor
from app.services.research.evidence_ranker import EvidenceRanker
from app.services.research.source_deduplicator import SourceDeduplicator
from app.services.research.citation_service import CitationService

__all__ = [
    "ResearchService",
    "SourceRouter",
    "SourceCategory",
    "AUTHORITY_WEIGHTS",
    "VERIFIED_RESEARCH_ENTRIES",
    "EvidenceExtractor",
    "EvidenceRanker",
    "SourceDeduplicator",
    "CitationService"
]
