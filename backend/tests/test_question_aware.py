"""
AgroScan AI — Question-Aware AI Assistant Master Test Suite
Verifies:
1. 10-Question Specificity (Q1-Q10)
2. Negative multi-question in-session uniqueness test
3. Semantic answer difference and focus validation
4. Follow-up pronoun and entity resolution
5. Non-fabrication of scan, weather, location, and dosages
6. Marathi language question-awareness
7. Cache key differentiation by question and context
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.assistant.assistant_service import AssistantService
from app.services.assistant.question_analyzer import QuestionAnalyzer
from app.services.assistant.response_cache import ResponseCache
from app.services.intent_service import AgriculturalIntent

class TestQuestionAwareAssistant(unittest.TestCase):

    def setUp(self):
        ResponseCache.clear()

    # --- 1. Q1 to Q10 Specificity Tests ---

    def test_q1_disease_identification(self):
        # Q1: What disease does my tomato plant have?
        res = AssistantService.process_message(
            message="What disease does my tomato plant have?",
            manual_plant="Tomato"
        )
        self.assertIn(res["intent"], [AgriculturalIntent.DISEASE_IDENTIFICATION, AgriculturalIntent.DISEASE_SYMPTOMS])
        self.assertTrue(any(w in res["answer"].lower() for w in ["early blight", "late blight", "leaf curl", "blight"]))

    def test_q2_irrigation_frequency(self):
        # Q2: How often should I water my tomato plant?
        res = AssistantService.process_message(
            message="How often should I water my tomato plant?",
            manual_plant="Tomato"
        )
        self.assertEqual(res["intent"], AgriculturalIntent.IRRIGATION)
        # Must answer irrigation, not lecture on early blight disease
        self.assertTrue(any(w in res["answer"].lower() for w in ["irrigation", "water", "moisture", "drip", "schedule"]))
        self.assertNotIn("fungicide", res["answer"].lower())

    def test_q3_why_leaves_turning_yellow(self):
        # Q3: Why are the leaves turning yellow?
        res = AssistantService.process_message(
            message="Why are the leaves turning yellow?",
            manual_plant="Tomato"
        )
        self.assertEqual(res["intent"], AgriculturalIntent.DISEASE_CAUSE)
        self.assertTrue(any(w in res["answer"].lower() for w in ["nitrogen", "chlorosis", "causes", "overwatering", "deficiency", "pathogen", "yellow"]))

    def test_q4_disease_prevention(self):
        # Q4: How can I prevent this disease?
        hist = [
            {"role": "user", "content": "My tomato has early blight."},
            {"role": "assistant", "content": "Early blight is caused by Alternaria solani."}
        ]
        res = AssistantService.process_message(
            message="How can I prevent this disease?",
            conversation_history=hist
        )
        self.assertEqual(res["intent"], AgriculturalIntent.DISEASE_PREVENTION)
        self.assertTrue(any(w in res["answer"].lower() for w in ["rotation", "sanitation", "mancozeb", "pruning", "spacing", "prevent"]))

    def test_q5_disease_transmission_spread(self):
        # Q5: Can this disease spread to nearby plants?
        hist = [
            {"role": "user", "content": "What is early blight?"},
            {"role": "assistant", "content": "Early blight is a fungal disease affecting solanaceous crops."}
        ]
        res = AssistantService.process_message(
            message="Can this disease spread to nearby plants?",
            conversation_history=hist
        )
        self.assertEqual(res["intent"], AgriculturalIntent.DISEASE_TRANSMISSION)
        self.assertTrue(any(w in res["answer"].lower() for w in ["spread", "spores", "wind", "splash", "airborne", "neighboring"]))

    def test_q6_fertilizer_suitable(self):
        # Q6: What fertilizer is suitable?
        res = AssistantService.process_message(
            message="What fertilizer is suitable for tomato?",
            manual_plant="Tomato"
        )
        self.assertEqual(res["intent"], AgriculturalIntent.FERTILIZER)
        self.assertTrue(any(w in res["answer"].lower() for w in ["npk", "nitrogen", "phosphorus", "potash", "manure", "fym"]))

    def test_q7_weather_disease_risk(self):
        # Q7: Will tomorrow's weather increase disease risk?
        weather = {"temperature_c": 26.0, "humidity_pct": 89.0, "rainfall_mm": 15.0}
        res = AssistantService.process_message(
            message="Will tomorrow's weather increase disease risk?",
            manual_plant="Tomato",
            weather_info=weather
        )
        self.assertEqual(res["intent"], AgriculturalIntent.WEATHER_DISEASE_RISK)
        self.assertTrue(any(w in res["answer"].lower() for w in ["humidity", "risk", "spore", "fungal", "89", "outbreak"]))

    def test_q8_soil_requirements(self):
        # Q8: What is the best soil for this crop?
        res = AssistantService.process_message(
            message="What is the best soil for this crop?",
            manual_plant="Sugarcane"
        )
        self.assertEqual(res["intent"], AgriculturalIntent.SOIL)
        self.assertTrue(any(w in res["answer"].lower() for w in ["loam", "alluvial", "drainage", "ph", "clay"]))

    def test_q9_symptoms(self):
        # Q9: What are the symptoms?
        hist = [
            {"role": "user", "content": "What diseases affect mango?"},
            {"role": "assistant", "content": "Mango is affected by powdery mildew and anthracnose."}
        ]
        res = AssistantService.process_message(
            message="What are the symptoms?",
            conversation_history=hist
        )
        self.assertEqual(res["intent"], AgriculturalIntent.DISEASE_SYMPTOMS)
        self.assertTrue(any(w in res["answer"].lower() for w in ["powdery", "white", "blossom", "panicle", "symptoms"]))

    def test_q10_explain_scan_result(self):
        # Q10: Explain my scan result.
        scan = {
            "valid_plant_image": True,
            "crop_detected": "Tomato",
            "disease_name": "Early Blight",
            "confidence_score": 0.94
        }
        res = AssistantService.process_message(
            message="Explain my scan result.",
            scan_context=scan
        )
        self.assertIn(res["intent"], [AgriculturalIntent.SCAN_EXPLANATION, AgriculturalIntent.DISEASE_IDENTIFICATION, AgriculturalIntent.DISEASE_SYMPTOMS])
        self.assertTrue(any(w in res["answer"].lower() for w in ["early blight", "concentric", "target", "spots", "tomato"]))

    # --- 2. Negative Test: Multi-Question In-Session Distinctness ---

    def test_negative_multi_question_session_distinctness(self):
        """5 completely different questions in the same session must produce 5 completely distinct answers."""
        session_hist = []
        questions = [
            "What disease does my plant have?",
            "How much water does it need?",
            "What fertilizer should I use?",
            "Can the disease spread to my other plants?",
            "What soil is suitable for this crop?"
        ]

        answers = []
        intents = []

        for q in questions:
            res = AssistantService.process_message(
                message=q,
                manual_plant="Tomato",
                conversation_history=session_hist
            )
            answers.append(res["answer"])
            intents.append(res["intent"])
            session_hist.append({"role": "user", "content": q})
            session_hist.append({"role": "assistant", "content": res["answer"]})

        # All 5 intents must be completely distinct
        self.assertEqual(len(set(intents)), 5, f"Expected 5 distinct intents, got: {intents}")
        # All 5 answers must be completely distinct
        self.assertEqual(len(set(answers)), 5, "Expected 5 distinct responses across the session")

    # --- 3. Semantic Diversity & Intent vs Focus Test ---

    def test_semantic_focus_difference(self):
        q_water = "How often should I water my tomato plant?"
        q_fert = "What fertilizer is recommended for tomato?"
        q_spread = "How does early blight spread?"

        res_water = AssistantService.process_message(q_water, manual_plant="Tomato")
        res_fert = AssistantService.process_message(q_fert, manual_plant="Tomato")
        res_spread = AssistantService.process_message(q_spread, manual_plant="Tomato")

        self.assertNotEqual(res_water["intent"], res_fert["intent"])
        self.assertNotEqual(res_water["intent"], res_spread["intent"])
        self.assertIn("water", res_water["answer"].lower())
        self.assertIn("fertilizer", res_fert["answer"].lower())
        self.assertTrue(any(w in res_spread["answer"].lower() for w in ["spread", "spores", "wind", "splash"]))

    # --- 4. Non-Fabrication Tests ---

    def test_no_scan_fabrication_when_invalid_image(self):
        res = AssistantService.process_message(
            message="What disease is in this picture?",
            scan_context={"valid_plant_image": False, "crop_detected": None, "disease_name": None}
        )
        self.assertFalse(res["context_used"]["scan"])
        # Must not fabricate Tomato Early Blight
        self.assertNotIn("early blight", res["answer"].lower())

    def test_weather_unavailable_honest_response(self):
        res = AssistantService.process_message(
            message="Will the weather cause disease outbreaks?",
            manual_plant="Cotton",
            weather_info=None
        )
        self.assertTrue(any(w in res["answer"].lower() for w in ["unavailable", "humidity", "weather"]))

    # --- 5. Marathi Language Tests ---

    def test_marathi_irrigation_question(self):
        res = AssistantService.process_message(
            message="टोमॅटोला पाणी किती दिवसांनी द्यावे?",
            language="mr"
        )
        self.assertEqual(res["intent"], AgriculturalIntent.IRRIGATION)
        self.assertTrue(any(w in res["answer"] for w in ["पाणी", "सिंचन", "ठिबक", "वाफसा"]))

    def test_marathi_fertilizer_question(self):
        res = AssistantService.process_message(
            message="उसासाठी कोणते खत वापरावे?",
            language="mr"
        )
        self.assertEqual(res["intent"], AgriculturalIntent.FERTILIZER)
        self.assertTrue(any(w in res["answer"] for w in ["खत", "नत्र", "NPK", "शेणखत"]))

    def test_marathi_yellow_leaves_question(self):
        res = AssistantService.process_message(
            message="माझ्या झाडाची पाने पिवळी का पडत आहेत?",
            language="mr"
        )
        self.assertEqual(res["intent"], AgriculturalIntent.DISEASE_CAUSE)
        self.assertTrue(any(w in res["answer"] for w in ["पिवळी", "अन्नद्रव्य", "नत्र", "निचरा", "पाणी"]))

    # --- 6. Cache Key Differentiation ---

    def test_cache_keys_different_for_different_questions(self):
        k1 = ResponseCache.generate_cache_key("u1", "how to water tomato", "IRRIGATION", "en", "Tomato")
        k2 = ResponseCache.generate_cache_key("u1", "what fertilizer for tomato", "FERTILIZER", "en", "Tomato")
        self.assertNotEqual(k1, k2)

if __name__ == "__main__":
    unittest.main()
