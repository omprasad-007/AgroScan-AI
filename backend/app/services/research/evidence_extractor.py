"""
AgroScan AI — Evidence Extractor
Extracts, normalizes, and packages claims from diverse sources into a standard Evidence Object.
"""

import datetime
from typing import Dict, Any, List, Optional
from app.services.research.source_registry import VERIFIED_RESEARCH_ENTRIES, AUTHORITY_WEIGHTS, SourceCategory

class EvidenceExtractor:
    """Standardizes heterogeneous agricultural data into structured Evidence Objects."""

    @classmethod
    def extract_evidence_for_categories(
        cls,
        categories: List[str],
        query: str,
        plant_name: Optional[str],
        disease_name: Optional[str]
    ) -> List[Dict[str, Any]]:
        raw_items: List[Dict[str, Any]] = []
        today_str = datetime.date.today().isoformat()
        q_words = set((query or "").lower().split())

        for cat in categories:
            entries = VERIFIED_RESEARCH_ENTRIES.get(cat, [])
            for item in entries:
                claim_text = item["claim"]
                auth_score = item.get("authority_score", AUTHORITY_WEIGHTS.get(item.get("source_type"), 0.85))
                ev_quality = item.get("evidence_quality", 0.90)

                # Compute keyword relevance
                claim_lower = claim_text.lower()
                matched_words = [w for w in q_words if len(w) > 3 and w in claim_lower]
                rel_score = min(0.98, max(0.65, 0.70 + len(matched_words) * 0.07))

                # Compute recency score based on published year
                pub_year = 2023
                try:
                    pub_year = int(item.get("published_date", "2023")[:4])
                except Exception:
                    pass
                recency_score = 0.95 if pub_year >= 2024 else 0.85 if pub_year >= 2023 else 0.75

                evidence_obj = {
                    "claim": claim_text,
                    "title": item.get("title", item.get("source", "Agricultural Research Source")),
                    "source": item["source"],
                    "source_type": item.get("source_type", SourceCategory.LEVEL_2_AGRI_DB),
                    "url": item["url"],
                    "published_date": item.get("published_date", "2023-01-01"),
                    "retrieved_date": today_str,
                    "relevance_score": round(rel_score, 2),
                    "authority_score": round(auth_score, 2),
                    "recency_score": round(recency_score, 2),
                    "evidence_score": round(ev_quality, 2)
                }
                raw_items.append(evidence_obj)

        return raw_items
