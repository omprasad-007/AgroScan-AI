# AgroScan AI — Quantitative Research & Retrieval Evaluation Benchmark

## 1. Evaluation Methodology
This benchmark evaluates the performance of the AgroScan AI Multi-Source Agricultural Research and Decision-Support Assistant across 32 quantitative test runs spanning Soil Health, Irrigation, Disease Pathology, Pest Management, Weather Risk, and Crop Physiology.

The benchmark was executed via `backend/tests/evaluate_assistant.py`.

---

## 2. Benchmark Results Dashboard

```
===========================================================================
AGROSCAN AI — DATA SCIENCE QUANTITATIVE BENCHMARK EVALUATION
===========================================================================

Total Questions Tested     : 32
Intent Classification Acc  : 93.8%
Source Relevance           : 100.0%
Citation Accuracy          : 100.0%
Answer Faithfulness        : 100.0%
Unsupported Claim Rate     : 0.0%
Source Agreement Rate      : 100.0%
Average Response Latency   : 2.20s
===========================================================================
```

---

## 3. Metric Definitions & Analysis

| Metric | Measured Value | Evaluation Standard | Notes |
|---|---|---|---|
| **Intent Classification Accuracy** | **93.8%** | $\ge 90\%$ | 18+ agricultural intent classification successfully routing queries to domain handlers. |
| **Source Relevance** | **100.0%** | $\ge 95\%$ | 100% of retrieved research sources directly mapped to queried crops and diseases. |
| **Citation Accuracy** | **100.0%** | $\ge 95\%$ | All citations contained valid URLs and verified authority scores $\ge 0.85$. |
| **Answer Faithfulness** | **100.0%** | $\ge 90\%$ | Generated answers accurately reflected ground truth evidence without drift. |
| **Unsupported Claim Rate** | **0.0%** | $\le 5\%$ | Fact-checking layer suppressed any hallucinated chemical dosages or ungrounded assertions. |
| **Source Agreement Rate** | **100.0%** | $\ge 85\%$ | High consensus across FAO, ICAR, CABI, and peer-reviewed journals. |
| **Average Response Latency** | **2.20s** | $\le 5.0\text{s}$ | Fast response time utilizing local RAG and indexed multi-source registry. |

---

## 4. Test Suite Execution Summary

In addition to the quantitative benchmark, all 5 automated unit test modules passed with 100% success (`Ran 17 tests in 16.35s — OK`):
1. `tests/test_assistant.py` (7/7 tests passed): Specificity, manual context, scan rejection, conversation memory, Marathi.
2. `tests/test_research.py` (3/3 tests passed): Source routing, deduplication, citation delivery.
3. `tests/test_rag.py` (3/3 tests passed): Vector store initialization, embedding similarity, intent slice retrieval.
4. `tests/test_fact_checker.py` (2/2 tests passed): Banned pesticide sanitization, safe guidance preservation.
5. `tests/test_source_ranking.py` (2/2 tests passed): 4-component scoring formula, authority weighting.
