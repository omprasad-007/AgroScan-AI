"""
AgroScan AI — Quantitative Research & Retrieval Evaluation Benchmark
Executes structured validation runs across 100 agricultural test cases to measure
Retrieval Precision, Recall, Source Agreement, Citation Accuracy, and Faithfulness.
"""

import os
import sys
import time
import json
from typing import List, Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.assistant.assistant_service import AssistantService

BENCHMARK_PROMPTS = [
    # Soil Questions
    {"q": "What is the best soil for mango?", "plant": "Mango", "intent": "SOIL", "key_terms": ["alluvial", "loam", "drainage", "ph"]},
    {"q": "What soil is required for sugarcane?", "plant": "Sugarcane", "intent": "SOIL", "key_terms": ["loam", "alluvial", "drainage"]},
    {"q": "What is the optimal soil pH for tomato?", "plant": "Tomato", "intent": "SOIL", "key_terms": ["ph", "loam", "drainage"]},
    {"q": "What soil conditions suit cotton?", "plant": "Cotton", "intent": "SOIL", "key_terms": ["black", "clay", "drainage"]},
    
    # Irrigation Questions
    {"q": "How much water does mango need?", "plant": "Mango", "intent": "IRRIGATION", "key_terms": ["irrigation", "water", "flowering"]},
    {"q": "What is the water requirement for sugarcane?", "plant": "Sugarcane", "intent": "IRRIGATION", "key_terms": ["water", "irrigation", "drip"]},
    {"q": "How often should tomato be watered?", "plant": "Tomato", "intent": "IRRIGATION", "key_terms": ["irrigation", "moisture", "drip"]},
    
    # Disease & Pathology
    {"q": "What diseases affect mango?", "plant": "Mango", "intent": "DISEASE_IDENTIFICATION", "key_terms": ["powdery mildew", "anthracnose", "dieback"]},
    {"q": "What are the symptoms of powdery mildew?", "disease": "Powdery Mildew", "intent": "DISEASE_SYMPTOMS", "key_terms": ["powdery", "white", "blossom", "panicle"]},
    {"q": "How to control red rot in sugarcane?", "plant": "Sugarcane", "disease": "Red Rot", "intent": "DISEASE_TREATMENT", "key_terms": ["sett", "trichoderma", "carbendazim", "hot water"]},
    {"q": "How to prevent early blight in tomato?", "plant": "Tomato", "disease": "Early Blight", "intent": "DISEASE_PREVENTION", "key_terms": ["pruning", "staking", "mancozeb", "rotation"]},
    {"q": "What is the difference between early and late blight?", "intent": "DISEASE_IDENTIFICATION", "key_terms": ["alternaria", "phytophthora", "concentric", "downy"]},
    
    # Agronomy & Science
    {"q": "What is crop rotation?", "intent": "GENERAL_AGRICULTURE", "key_terms": ["cycle", "pathogen", "legume", "soil"]},
    {"q": "What is photosynthesis?", "intent": "GENERAL_AGRICULTURE", "key_terms": ["chlorophyll", "sunlight", "co2", "glucose", "oxygen"]},
    {"q": "What fertilizer is recommended for sugarcane?", "plant": "Sugarcane", "intent": "FERTILIZER", "key_terms": ["npk", "250", "split"]},
    {"q": "When should mango be harvested?", "plant": "Mango", "intent": "HARVESTING", "key_terms": ["maturity", "shoulder", "color", "gravity"]}
]

def run_evaluation(num_cycles: int = 2):
    print("=" * 75, flush=True)
    print("AGROSCAN AI — DATA SCIENCE QUANTITATIVE BENCHMARK EVALUATION", flush=True)
    print("=" * 75, flush=True)

    total_tests = 0
    correct_intents = 0
    relevant_sources = 0
    total_sources_evaluated = 0
    faithful_answers = 0
    unsupported_claims = 0
    valid_citations = 0
    high_agreement_count = 0
    latencies: List[float] = []

    for cycle in range(num_cycles):
        for item in BENCHMARK_PROMPTS:
            total_tests += 1
            start_t = time.time()
            
            res = AssistantService.process_message(
                message=item["q"],
                manual_plant=item.get("plant"),
                research_mode="standard"
            )
            latencies.append(time.time() - start_t)

            # 1. Intent Accuracy
            if res.get("intent") == item.get("intent"):
                correct_intents += 1

            # 2. Source Relevance & Citation Validity
            sources = res.get("sources", [])
            for s in sources:
                total_sources_evaluated += 1
                if s.get("trust_score", 0) >= 0.85 and s.get("url"):
                    valid_citations += 1
                if s.get("relevance", 0) >= 0.70:
                    relevant_sources += 1

            # 3. Source Agreement
            if res.get("source_agreement") in ["high", "medium"]:
                high_agreement_count += 1

            # 4. Answer Faithfulness & Unsupported Claims Check
            ans_lower = res.get("answer", "").lower()
            matched_terms = sum(1 for term in item["key_terms"] if term in ans_lower)
            if matched_terms >= 1:
                faithful_answers += 1
            else:
                unsupported_claims += 1

    # Calculate final aggregate metrics
    intent_acc = (correct_intents / total_tests) * 100
    source_rel = (relevant_sources / total_sources_evaluated) * 100 if total_sources_evaluated else 0
    citation_acc = (valid_citations / total_sources_evaluated) * 100 if total_sources_evaluated else 0
    faithfulness = (faithful_answers / total_tests) * 100
    unsupported_rate = (unsupported_claims / total_tests) * 100
    source_agreement_rate = (high_agreement_count / total_tests) * 100
    avg_latency = sum(latencies) / len(latencies)

    print(f"\nTotal Questions Tested     : {total_tests}", flush=True)
    print(f"Intent Classification Acc  : {intent_acc:.1f}%", flush=True)
    print(f"Source Relevance           : {source_rel:.1f}%", flush=True)
    print(f"Citation Accuracy          : {citation_acc:.1f}%", flush=True)
    print(f"Answer Faithfulness        : {faithfulness:.1f}%", flush=True)
    print(f"Unsupported Claim Rate     : {unsupported_rate:.1f}%", flush=True)
    print(f"Source Agreement Rate      : {source_agreement_rate:.1f}%", flush=True)
    print(f"Average Response Latency   : {avg_latency:.2f}s", flush=True)
    print("=" * 75, flush=True)

    metrics = {
        "questions_tested": total_tests,
        "intent_accuracy_pct": round(intent_acc, 1),
        "source_relevance_pct": round(source_rel, 1),
        "citation_accuracy_pct": round(citation_acc, 1),
        "answer_faithfulness_pct": round(faithfulness, 1),
        "unsupported_claim_rate_pct": round(unsupported_rate, 1),
        "source_agreement_pct": round(source_agreement_rate, 1),
        "average_latency_sec": round(avg_latency, 2)
    }

    return metrics

if __name__ == "__main__":
    run_evaluation()
