# AgroScan AI — Multi-Source Agricultural AI Architecture

## 1. System Overview
AgroScan AI is an **Evidence-Grounded Multi-Source Agricultural Decision-Support System** designed for high-accuracy crop diagnostics, soil health recommendations, water management scheduling, and plant pathology guidance.

Unlike generic conversational wrappers, AgroScan AI separates **Image Machine Learning classification** from **Multi-Source Evidence Synthesis**, ensuring that AI models act as reasoning and synthesis engines grounded in verified agricultural literature rather than ungrounded generative sources.

---

## 2. Architectural Pipeline

```
                         USER QUESTION
                               │
                               ▼
                      ┌─────────────────┐
                      │ Intent Detector │
                      └────────┬────────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
             Plant         Disease        Context
             Context       Context       Weather/GPS
                 │             │             │
                 └─────────────┼─────────────┘
                               ▼
                     ┌──────────────────┐
                     │ Source Router    │
                     └────────┬─────────┘
                              │
           ┌──────────────────┼───────────────────┐
           ▼                  ▼                   ▼
       FAO / ICAR          CABI             Research Papers
           │                  │                   │
           ▼                  ▼                   ▼
     Government          Agriculture        Scientific
     Sources             Databases          Literature
           │                  │                   │
           └──────────────────┼───────────────────┘
                              ▼
                    ┌────────────────────┐
                    │ Evidence Extractor │
                    └──────────┬─────────┘
                               ▼
                    ┌────────────────────┐
                    │ Evidence Ranking   │
                    └──────────┬─────────┘
                               ▼
                  ┌─────────────────────────┐
                  │ Multiple AI Analysis    │
                  │ Gemini + optional LLM   │
                  └────────────┬────────────┘
                               ▼
                    ┌────────────────────┐
                    │ Fact Checker       │
                    └──────────┬─────────┘
                               ▼
                     ┌───────────────────┐
                     │ Final Answer      │
                     │ + Confidence      │
                     │ + Sources         │
                     └───────────────────┘
```

---

## 3. Core Component Breakdown

### 3.1 Assistant Service Layer (`app/services/assistant/`)
- `assistant_service.py`: Central coordinator routing queries through intent detection, context resolution, research retrieval, LLM reasoning, and fact checking.
- `intent_service.py`: 18+ intent classifier identifying domains (`SOIL`, `IRRIGATION`, `FERTILIZER`, `HARVESTING`, `DISEASE_SYMPTOMS`, `DISEASE_CAUSE`, `DISEASE_PREVENTION`, `DISEASE_TREATMENT`, `WEATHER_DISEASE_RISK`, `GENERAL_AGRICULTURE`).
- `context_service.py`: Resolves active entities across real scan predictions, manual plant selections, and multi-turn conversations without conflation.
- `conversation_service.py`: Manages session-level isolation and message history sanitization.
- `response_service.py`: Packages final answers, structured clickable citations, confidence metrics, and context flags.

### 3.2 Research Engine Layer (`app/services/research/`)
- `source_registry.py`: Directory of verified international and national agricultural knowledge repositories with authority ratings.
- `source_router.py`: Selects targeted knowledge categories matching intent and botanical taxonomy.
- `evidence_extractor.py`: Normalizes heterogeneous external facts into structured Evidence Objects.
- `evidence_ranker.py`: Computes composite quality scores using a 4-component weighted formula.
- `source_deduplicator.py`: Eliminates duplicate URLs and syndicated text.
- `citation_service.py`: Formats verifiable external links with trust badges.

### 3.3 Retrieval-Augmented Generation Layer (`app/services/rag/`)
- `vector_store.py`: In-memory index of 20+ crop agronomy profiles, pathology datasheets, and general agricultural science.
- `embedding_service.py`: Computes term-frequency and semantic similarity scores.
- `retrieval_service.py`: Retrieves targeted knowledge slices for prompt grounding.

### 3.4 Model & Synthesis Layer (`app/services/llm/`)
- `gemini_provider.py`: Primary client for Google Gemini 1.5 Flash and Gemini 2.5 Flash.
- `secondary_provider.py`: Failover client for OpenAI / OpenRouter.
- `llm_router.py`: Complexity-based model router (`QUICK`, `STANDARD`, `DEEP_RESEARCH`).
- `synthesis_service.py`: Prompt builder with strict safety constraints and deterministic offline domain fallback.

### 3.5 Verification Layer (`app/services/verification/`)
- `fact_checker.py`: Sanitizes responses to suppress unverified high-risk chemical claims.
- `contradiction_detector.py`: Detects conflicting source recommendations.
- `confidence_service.py`: Computes aggregate confidence scores.
