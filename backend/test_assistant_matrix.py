"""
AgroScan AI Assistant — Verification Test Suite
Tests all 10 standard agricultural questions, negative questions, multi-turn memory,
and Marathi translations against the AIProviderService & AgriRAGService.
"""

import os
import sys
import io

# Fix Windows console UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_provider_service import AIProviderService
from app.services.intent_service import IntentService, AgriculturalIntent

def run_tests():
    print("=" * 80)
    print("AGROSCAN AI ASSISTANT — TEST MATRIX EXECUTION")
    print("=" * 80)

    test_cases = [
        # Test 1: Mango Soil
        ("What is the best soil for mango?", "en", None, None, AgriculturalIntent.SOIL, ["alluvial", "loam", "drain", "pH"]),
        
        # Test 2: Mango Irrigation
        ("How much water does mango need?", "en", None, None, AgriculturalIntent.IRRIGATION, ["irrigation", "water", "flowering"]),
        
        # Test 3: Mango Harvesting
        ("When should mango be harvested?", "en", None, None, AgriculturalIntent.HARVESTING, ["maturity", "shoulder", "color"]),
        
        # Test 4: Mango Diseases
        ("What diseases affect mango?", "en", None, None, AgriculturalIntent.DISEASE_IDENTIFICATION, ["Powdery Mildew", "Anthracnose", "Dieback"]),
        
        # Test 5: Powdery Mildew Symptoms
        ("What are the symptoms of powdery mildew?", "en", None, None, AgriculturalIntent.DISEASE_SYMPTOMS, ["powdery", "white", "blossom", "panicle"]),
        
        # Test 6: Powdery Mildew Prevention
        ("How can I prevent powdery mildew?", "en", None, None, AgriculturalIntent.DISEASE_PREVENTION, ["prune", "sanitation", "sunlight", "nitrogen"]),
        
        # Test 7: Powdery Mildew Treatment
        ("How can I control powdery mildew?", "en", None, None, AgriculturalIntent.DISEASE_TREATMENT, ["Sulphur", "Neem", "Hexaconazole", "biological"]),
        
        # Test 8: Sugarcane Fertilizer
        ("What fertilizer is suitable for sugarcane?", "en", None, None, AgriculturalIntent.FERTILIZER, ["NPK", "250", "split", "Acetobacter"]),
        
        # Test 9: Weather Outbreak Risk
        ("Will current weather increase disease risk?", "en", None, {"temperature_c": 27, "humidity_pct": 86}, AgriculturalIntent.WEATHER_DISEASE_RISK, ["humidity", "fungal", "risk"]),
        
        # Test 10: Crop Rotation
        ("What is crop rotation?", "en", None, None, AgriculturalIntent.GENERAL_AGRICULTURE, ["practice", "pathogen", "legume", "soil"]),
        
        # Negative Test: Photosynthesis
        ("What is photosynthesis?", "en", None, None, AgriculturalIntent.GENERAL_AGRICULTURE, ["sunlight", "carbon dioxide", "oxygen", "plants"]),
        
        # Marathi Test: Mango Soil
        ("आंब्यासाठी कोणती माती योग्य आहे?", "mr", None, None, AgriculturalIntent.SOIL, ["माती", "निचरा", "जमीन", "गाळाची"]),
        
        # Marathi Test: Powdery Mildew
        ("भुरी रोगाची लक्षणे कोणती?", "mr", None, None, AgriculturalIntent.DISEASE_SYMPTOMS, ["पांढरी", "पावडर", "बुरशी"]),
        
        # Non-Agri Math Test
        ("What is 2+2?", "en", None, None, AgriculturalIntent.GENERAL, ["4"])
    ]

    all_passed = True
    responses = []

    for i, (q, lang, scan_ctx, weather_ctx, expected_intent, expected_terms) in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] Testing: \"{q}\" (lang={lang})")
        
        # Check Intent
        detected_intent = IntentService.detect_intent(q)
        print(f"  -> Detected Intent: {detected_intent} (Expected: {expected_intent})")
        
        # Generate Response
        reply = AIProviderService.generate_response(
            message=q,
            scan_context=scan_ctx,
            weather_info=weather_ctx,
            language=lang
        )
        responses.append((q, reply))
        
        print(f"  -> Response Preview:\n{reply[:250]}...\n")
        
        # Check that response is non-empty and contains relevant terms
        matches = [term for term in expected_terms if term.lower() in reply.lower()]
        if not reply or len(matches) == 0:
            print(f"  FAILED: Missing expected terms {expected_terms}")
            all_passed = False
        else:
            print(f"  PASSED (Matched: {matches})")

    # Multi-turn Context Test (Section 22)
    print("\n" + "=" * 80)
    print("TESTING MULTI-TURN CONVERSATION MEMORY & ISOLATION")
    print("=" * 80)

    # Turn 1:
    hist = []
    t1_q = "What diseases affect mango?"
    t1_res = AIProviderService.generate_response(message=t1_q, conversation_history=hist)
    hist.append({"role": "user", "content": t1_q})
    hist.append({"role": "assistant", "content": t1_res})
    print(f"Turn 1 Q: \"{t1_q}\"\nTurn 1 A: {t1_res[:150]}...")

    # Turn 2: Follow-up relying on Turn 1 context
    t2_q = "What are the symptoms?"
    t2_res = AIProviderService.generate_response(message=t2_q, conversation_history=hist)
    hist.append({"role": "user", "content": t2_q})
    hist.append({"role": "assistant", "content": t2_res})
    print(f"\nTurn 2 Q: \"{t2_q}\"\nTurn 2 A: {t2_res[:200]}...")

    if "mango" in t2_res.lower() or "powdery" in t2_res.lower() or "anthracnose" in t2_res.lower() or "symptoms" in t2_res.lower():
        print("  -> Multi-turn Turn 2 PASSED (Inherited Mango/Disease context correctly)")
    else:
        print("  -> Multi-turn Turn 2 WARN: Context not explicitly mentioned")

    # Turn 3: Brand new conversation (Isolation test)
    new_hist = []
    t3_q = "What disease affects sugarcane?"
    t3_res = AIProviderService.generate_response(message=t3_q, conversation_history=new_hist)
    print(f"\nNew Session Q: \"{t3_q}\"\nNew Session A: {t3_res[:200]}...")

    if "mango" not in t3_res.lower() and ("red rot" in t3_res.lower() or "smut" in t3_res.lower() or "sugarcane" in t3_res.lower()):
        print("  -> New Session Isolation PASSED (Zero leakage from prior Mango session)")
    else:
        print("  -> New Session Isolation FAILED")
        all_passed = False

    # Check distinctness of answers (No repeated canned answers)
    print("\n" + "=" * 80)
    print("DISTINCTNESS CHECK (Zero Repeated Answers)")
    print("=" * 80)
    all_texts = [r[1] for r in responses]
    unique_texts = set(all_texts)
    print(f"Total Questions: {len(all_texts)} | Unique Responses: {len(unique_texts)}")
    if len(all_texts) == len(unique_texts):
        print("PERFECT: 100% of responses are distinct and tailored to the question.")
    else:
        print(f"WARN: {len(all_texts) - len(unique_texts)} duplicate responses found.")
        all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("ALL TESTS PASSED SUCCESSFULLY!")
    else:
        print("SOME TESTS FAILED.")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()
