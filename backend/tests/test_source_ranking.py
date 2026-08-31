"""
AgroScan AI — Source Ranking Unit Tests
Verifies the 4-component weighted source scoring algorithm:
Final Score = (Authority * 0.40) + (Relevance * 0.30) + (Recency * 0.15) + (Evidence Quality * 0.15)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.research.evidence_ranker import EvidenceRanker

class TestSourceRanking(unittest.TestCase):

    def test_ranking_formula_calculation(self):
        # FAO Test: Auth=1.0, Rel=0.90, Rec=0.95, Ev=0.96
        # Expected: (1.0*0.40) + (0.90*0.30) + (0.95*0.15) + (0.96*0.15) = 0.40 + 0.27 + 0.1425 + 0.144 = 0.9565
        item = {
            "source": "FAO",
            "authority_score": 1.0,
            "relevance_score": 0.90,
            "recency_score": 0.95,
            "evidence_score": 0.96
        }
        score = EvidenceRanker.calculate_score(item)
        self.assertAlmostEqual(score, 0.9565, places=3)

    def test_source_prioritization(self):
        fao_item = {
            "title": "FAO IPM Guidelines",
            "source": "FAO",
            "authority_score": 1.00,
            "relevance_score": 0.85,
            "recency_score": 0.90,
            "evidence_score": 0.95
        }
        blog_item = {
            "title": "Random Gardening Blog",
            "source": "Blog",
            "authority_score": 0.40,
            "relevance_score": 0.90,
            "recency_score": 0.95,
            "evidence_score": 0.50
        }
        ranked = EvidenceRanker.rank_evidence([blog_item, fao_item], top_k=2)
        # FAO must rank higher than blog despite blog having higher relevance
        self.assertEqual(ranked[0]["source"], "FAO")
        self.assertTrue(ranked[0]["final_score"] > ranked[1]["final_score"])

if __name__ == "__main__":
    unittest.main()
