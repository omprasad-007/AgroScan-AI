"""
AgroScan AI — Source Deduplicator
Detects and collapses duplicate URLs, syndicated articles, and redundant citations.
"""

import re
from typing import List, Dict, Any

class SourceDeduplicator:
    """Removes duplicate and syndicated agricultural sources."""

    @classmethod
    def deduplicate(cls, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen_urls = set()
        seen_normalized_titles = set()
        unique = []

        for itm in items:
            url = itm.get("url", "").strip().rstrip("/").lower()
            title = itm.get("title", itm.get("source", "")).strip().lower()
            norm_title = re.sub(r'[^a-zA-Z0-9]', '', title)

            if url and url in seen_urls:
                continue
            if norm_title and norm_title in seen_normalized_titles:
                continue

            if url:
                seen_urls.add(url)
            if norm_title:
                seen_normalized_titles.add(norm_title)

            unique.append(itm)

        return unique
