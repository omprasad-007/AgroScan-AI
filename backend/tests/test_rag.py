"""
AgroScan AI — Local RAG Unit Tests
Verifies VectorStore initialization, embedding similarity, and entity retrieval.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.rag.retrieval_service import RetrievalService
from app.services.rag.vector_store import VectorStore
from app.services.rag.embedding_service import EmbeddingService

class TestRAG(unittest.TestCase):

    def test_vector_store_initialization_and_search(self):
        VectorStore.initialize_store()
        results = VectorStore.search("mango powdery mildew", top_k=2)
        self.assertTrue(len(results) > 0)
        self.assertTrue(any("mango" in r["content"].lower() or "mildew" in r["content"].lower() for r in results))

    def test_embedding_similarity(self):
        sim = EmbeddingService.compute_similarity("sugarcane red rot disease", "Red Rot of Sugarcane causes internal red stalk discoloration")
        self.assertTrue(sim > 0.3)

    def test_retrieval_service_intent_slice(self):
        grounding = RetrievalService.retrieve_grounding("What is the best soil for mango?")
        self.assertEqual(grounding["intent"], "SOIL")
        self.assertEqual(grounding["plant_name"], "Mango")
        self.assertIn("alluvial", grounding["grounding_text"].lower())

if __name__ == "__main__":
    unittest.main()
