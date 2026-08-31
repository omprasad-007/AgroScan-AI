"""
AgroScan AI — Multi-Source Agricultural AI Assistant Comprehensive Test Suite
Tests intent classification, multi-source research grounding, evidence fusion,
source citations, distinct answers, multi-turn memory, session isolation, and Marathi localization.
"""

import os
import sys
import io
import unittest

# Fix Windows console UTF-8 output
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.ai_provider_service import AIProviderService
from app.services.intent_service import IntentService, AgriculturalIntent
from app.services.research_service import AgriculturalResearchService

class TestAgroScanAIAssistant(unittest.TestCase):

    def test_01_sugarcane_soil(self):
        q = "What is the best soil for sugarcane?"
        res = AIProviderService.generate_structured_research_response(message=q)
        self.assertEqual(res["intent"], AgriculturalIntent.SOIL)
        self.assertTrue(len(res["sources"]) > 0)
        self.assertIn("soil", res["answer"].lower())
        self.assertTrue(any(w in res["answer"].lower() for w in ["loam", "alluvial", "drain", "ph", "clay"]))

    def test_02_sugarcane_water(self):
        q = "How much water does sugarcane require?"
        res = AIProviderService.generate_structured_research_response(message=q)
        self.assertEqual(res["intent"], AgriculturalIntent.IRRIGATION)
        self.assertTrue(any(w in res["answer"].lower() for w in ["irrigation", "water", "drip", "moisture", "mm"]))

    def test_03_sugarcane_diseases(self):
        q = "What diseases affect sugarcane?"
        res = AIProviderService.generate_structured_research_response(message=q)
        self.assertEqual(res["intent"], AgriculturalIntent.DISEASE_IDENTIFICATION)
        self.assertTrue(any(w in res["answer"].lower() for w in ["red rot", "smut", "grassy shoot", "rust"]))

    def test_04_red_rot_control(self):
        q = "How can I control red rot?"
        res = AIProviderService.generate_structured_research_response(message=q)
        self.assertEqual(res["intent"], AgriculturalIntent.DISEASE_TREATMENT)
        self.assertTrue(any(w in res["answer"].lower() for w in ["sett", "trichoderma", "carbendazim", "hot water", "rotation", "resistant"]))

    def test_05_weather_disease_risk(self):
        q = "Is this weather favorable for fungal disease?"
        weather = {"temperature_c": 28.0, "humidity_pct": 88.0, "rainfall_mm": 12.0}
        res = AIProviderService.generate_structured_research_response(message=q, weather_info=weather)
        self.assertEqual(res["intent"], AgriculturalIntent.WEATHER_DISEASE_RISK)
        self.assertTrue(any(w in res["answer"].lower() for w in ["humidity", "fungal", "risk", "spore", "moisture"]))

    def test_06_tomato_brown_spots(self):
        q = "My tomato leaves have brown spots. What could cause it?"
        res = AIProviderService.generate_structured_research_response(message=q)
        self.assertTrue(any(w in res["answer"].lower() for w in ["early blight", "alternaria", "septoria", "fungal", "deficiency"]))

    def test_07_photosynthesis_negative_test(self):
        q = "What is photosynthesis?"
        res = AIProviderService.generate_structured_research_response(message=q)
        self.assertEqual(res["intent"], AgriculturalIntent.GENERAL_AGRICULTURE)
        self.assertTrue(any(w in res["answer"].lower() for w in ["chlorophyll", "sunlight", "carbon dioxide", "glucose", "oxygen"]))
        # Must not fabricate a disease scan
        self.assertNotIn("you scanned", res["answer"].lower())

    def test_08_fertilizer_guidance(self):
        q = "What fertilizer is suitable for sugarcane?"
        res = AIProviderService.generate_structured_research_response(message=q)
        self.assertEqual(res["intent"], AgriculturalIntent.FERTILIZER)
        self.assertTrue(any(w in res["answer"].lower() for w in ["npk", "250", "nitrogen", "phosphorus", "potash"]))

    def test_09_early_vs_late_blight_differentiation(self):
        q = "What is the difference between early blight and late blight?"
        res = AIProviderService.generate_structured_research_response(message=q)
        self.assertTrue(any(w in res["answer"].lower() for w in ["alternaria", "target", "bullseye", "concentric"]))
        self.assertTrue(any(w in res["answer"].lower() for w in ["phytophthora", "water-soaked", "downy", "cool"]))

    def test_10_research_sources_citations(self):
        q = "Search recent research on tomato disease management."
        res = AIProviderService.generate_structured_research_response(message=q, research_mode="deep_research")
        self.assertTrue(len(res["sources"]) >= 2)
        # Check source attributes
        for src in res["sources"]:
            self.assertIn("title", src)
            self.assertIn("url", src)
            self.assertIn("trust_score", src)
            self.assertTrue(src["trust_score"] >= 0.85)

    def test_11_marathi_localization(self):
        q = "उसासाठी खत व्यवस्थापन कसे करावे?"
        res = AIProviderService.generate_structured_research_response(message=q, language="mr")
        self.assertTrue(any(w in res["answer"] for w in ["खत", "नत्र", "स्फुरद", "पालाश", "NPK", "शेणखत"]))

    def test_12_multi_turn_context_and_isolation(self):
        # Turn 1
        hist = []
        t1_q = "What diseases affect mango?"
        t1_res = AIProviderService.generate_structured_research_response(message=t1_q, conversation_history=hist)
        hist.append({"role": "user", "content": t1_q})
        hist.append({"role": "assistant", "content": t1_res["answer"]})

        # Turn 2: Follow-up question relying on Mango context
        t2_q = "What are the symptoms?"
        t2_res = AIProviderService.generate_structured_research_response(message=t2_q, conversation_history=hist)
        self.assertTrue(any(w in t2_res["answer"].lower() for w in ["mango", "powdery", "anthracnose", "patches", "panicle"]))

        # Turn 3: New conversation with Sugarcane (zero leakage from Mango)
        new_hist = []
        t3_q = "What disease affects sugarcane?"
        t3_res = AIProviderService.generate_structured_research_response(message=t3_q, conversation_history=new_hist)
        self.assertNotIn("mango", t3_res["answer"].lower())
        self.assertTrue(any(w in t3_res["answer"].lower() for w in ["red rot", "smut", "sugarcane"]))

    def test_13_distinctness(self):
        queries = [
            "What is the best soil for mango?",
            "How much water does mango need?",
            "When should mango be harvested?",
            "What is crop rotation?",
            "What is 2+2?"
        ]
        answers = [AIProviderService.generate_response(q) for q in queries]
        # All 5 answers must be completely distinct
        self.assertEqual(len(answers), len(set(answers)))

if __name__ == "__main__":
    unittest.main()
