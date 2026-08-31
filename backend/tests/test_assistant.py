"""
AgroScan AI — Assistant Master Unit Tests
Tests question-specificity, manual plant vs scan context, conversation memory, Marathi, and scan rejection.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.assistant.assistant_service import AssistantService
from app.services.intent_service import AgriculturalIntent

class TestAssistant(unittest.TestCase):

    def test_soil_question_specificity(self):
        res = AssistantService.process_message("What is the best soil for mango?")
        self.assertEqual(res["intent"], AgriculturalIntent.SOIL)
        self.assertTrue(any(w in res["answer"].lower() for w in ["alluvial", "loam", "drain", "ph", "clay"]))

    def test_irrigation_question_specificity(self):
        res = AssistantService.process_message("How much water does mango need?")
        self.assertEqual(res["intent"], AgriculturalIntent.IRRIGATION)
        self.assertTrue(any(w in res["answer"].lower() for w in ["irrigation", "water", "flowering", "days"]))

    def test_harvesting_question_specificity(self):
        res = AssistantService.process_message("When should mango be harvested?")
        self.assertEqual(res["intent"], AgriculturalIntent.HARVESTING)
        self.assertTrue(any(w in res["answer"].lower() for w in ["maturity", "shoulder", "color", "gravity"]))

    def test_manual_plant_selection_no_scan_fabrication(self):
        res = AssistantService.process_message(
            message="What fertilizer is suitable?",
            manual_plant="Sugarcane"
        )
        self.assertEqual(res["context_used"]["plant"], True)
        self.assertEqual(res["context_used"]["scan"], False)
        self.assertNotIn("you scanned", res["answer"].lower())

    def test_invalid_scan_rejection(self):
        # When an invalid scan or selfie is uploaded, no disease is fabricated
        res = AssistantService.process_message(
            message="What is this plant?",
            scan_context={"valid_plant_image": False, "crop_detected": None, "disease_name": None}
        )
        self.assertEqual(res["context_used"]["scan"], False)

    def test_marathi_localization(self):
        res = AssistantService.process_message(
            message="आंब्यासाठी कोणती माती योग्य आहे?",
            language="mr"
        )
        self.assertTrue(any(w in res["answer"] for w in ["माती", "निचरा", "जमीन", "गाळाची"]))

    def test_multi_turn_context_memory(self):
        hist = [
            {"role": "user", "content": "What diseases affect mango?"},
            {"role": "assistant", "content": "Mango is affected by Powdery Mildew and Anthracnose."}
        ]
        res = AssistantService.process_message(
            message="What are the symptoms?",
            conversation_history=hist
        )
        self.assertTrue(any(w in res["answer"].lower() for w in ["mango", "powdery", "anthracnose", "patches", "panicle", "symptoms"]))

if __name__ == "__main__":
    unittest.main()
