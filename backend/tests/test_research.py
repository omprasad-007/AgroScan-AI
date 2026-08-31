"""
AgroScan AI — Research Pipeline Unit Tests
Verifies source routing, evidence extraction, deduplication, and citation generation.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.research.research_service import ResearchService
from app.services.research.source_router import SourceRouter
from app.services.research.source_deduplicator import SourceDeduplicator

class TestResearchPipeline(unittest.TestCase):

    def test_source_routing(self):
        cats = SourceRouter.route_sources(
            query="How to control red rot in sugarcane?",
            plant_name="Sugarcane",
            disease_name="Red Rot",
            intent="DISEASE_TREATMENT"
        )
        self.assertIn("sugarcane_red_rot_pathology", cats)

    def test_deduplication(self):
        dup_items = [
            {"title": "FAO Guidelines", "url": "https://fao.org/guidelines/", "claim": "Text A"},
            {"title": "FAO Guidelines", "url": "https://fao.org/guidelines", "claim": "Text A"},
            {"title": "CABI Factsheet", "url": "https://cabi.org/facts", "claim": "Text B"}
        ]
        unique = SourceDeduplicator.deduplicate(dup_items)
        self.assertEqual(len(unique), 2)

    def test_end_to_end_research(self):
        res = ResearchService.conduct_research(
            query="What causes powdery mildew in mango?",
            plant_name="Mango",
            disease_name="Powdery Mildew",
            intent="DISEASE_CAUSE"
        )
        self.assertTrue(len(res["sources"]) > 0)
        self.assertIn(res["source_agreement"], ["high", "medium"])
        self.assertTrue(res["evidence_confidence"] >= 0.85)

if __name__ == "__main__":
    unittest.main()
