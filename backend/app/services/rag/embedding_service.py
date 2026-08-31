"""
AgroScan AI — Local RAG Embedding & Similarity Service
Provides lexical and semantic similarity vector scoring for fast in-memory document matching.
"""

import math
import re
from typing import List, Dict, Set

class EmbeddingService:
    """Lightweight vector similarity service for local RAG knowledge documents."""

    @staticmethod
    def tokenize(text: str) -> List[str]:
        return [w for w in re.findall(r'[a-zA-Z0-9_\u0900-\u097F]+', (text or "").lower()) if len(w) > 2]

    @classmethod
    def compute_similarity(cls, query: str, document_text: str) -> float:
        q_tokens = cls.tokenize(query)
        doc_tokens = cls.tokenize(document_text)

        if not q_tokens or not doc_tokens:
            return 0.0

        q_set: Set[str] = set(q_tokens)
        doc_set: Set[str] = set(doc_tokens)

        intersection = len(q_set.intersection(doc_set))
        if intersection == 0:
            return 0.0

        # Cosine-like term-frequency overlap
        return round(intersection / math.sqrt(len(q_set) * len(doc_set)), 4)
