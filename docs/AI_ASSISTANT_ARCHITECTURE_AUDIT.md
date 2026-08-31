# AgroScan AI — Assistant Architecture Audit & Refactor Plan

## 1. Executive Summary & Audit Context
This audit reviews the AI Assistant pipeline in AgroScan AI. The goal is to transition the assistant from a monolithic structure to a clean, modular, multi-source evidence-grounded agricultural decision-support system.

---

## 2. Current Architecture & Identified Limitations

### 2.1 Monolithic Service Layer
- **Previous State**: Intent classification, RAG retrieval, Gemini API calling, offline synthesis, and research evidence generation were partly coupled in `ai_provider_service.py` and `research_service.py`.
- **Architectural Requirement**: Clean separation of concerns into domain-specific packages:
  - `assistant/`: Intent detection, context resolution, conversation memory, response orchestration.
  - `research/`: Source routing, registry, evidence extraction, ranking, deduplication, citation formatting.
  - `rag/`: Local vector store, embedding service, and domain retrieval.
  - `llm/`: Model routing (Gemini 1.5/2.5, secondary provider), system prompt assembly, synthesis.
  - `verification/`: Safety fact-checking, contradiction detection, confidence scoring.

### 2.2 Scan Context vs Manual Plant Context
- **Risk**: Earlier iterations risked conflating manual selection with real image model predictions.
- **Requirement**: Strict separation:
  - Valid image scan -> `scan_context` with real ML confidence and disease bounding.
  - Manual crop choice -> `manual_context` with explicit phrasing *"Based on the crop you selected..."*.
  - Rejected image (non-leaf/selfie) -> explicit rejection with zero fabricated disease diagnoses.

### 2.3 Source Priority & Multi-Source Evidence Fusion
- **Requirement**: A strictly enforced source hierarchy:
  - **Level 1 (Authority 1.00)**: FAO, ICAR (IARI, CISH, SBI, IISS), State Ag Universities (TNAU, MPKV, PAU), Gov Ag Departments.
  - **Level 2 (Authority 0.95)**: CABI, Plantwise, Crop Protection Compendium, Peer-Reviewed Research Papers (Springer, APS, ScienceDirect).
  - **Level 3 (Authority 0.90)**: University Extension Publications.
  - **Level 4 (Authority 0.60)**: Commercial agricultural sites (supplementary only).
  - **Level 5 (Authority 0.10)**: Forums/blogs/social media (strictly avoided for treatments).

### 2.4 Evidence Scoring Formula
- Source ranking computed via:
  $$\text{Final Score} = (\text{Authority} \times 0.40) + (\text{Relevance} \times 0.30) + (\text{Recency} \times 0.15) + (\text{Evidence Quality} \times 0.15)$$

### 2.5 Safety Fact-Checking
- Extraction of generated claims and cross-validation against retrieved source evidence to prevent pesticide dosage or chemical fabrication.

---

## 3. Target Modular Directory Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── chat.py
│   │       │   ├── assistant.py
│   │       │   ├── scan.py
│   │       │   ├── plants.py
│   │       │   ├── weather.py
│   │       │   └── farm.py
│   │       └── router.py
│   │
│   ├── services/
│   │   ├── assistant/
│   │   │   ├── assistant_service.py
│   │   │   ├── intent_service.py
│   │   │   ├── context_service.py
│   │   │   ├── conversation_service.py
│   │   │   └── response_service.py
│   │   │
│   │   ├── research/
│   │   │   ├── research_service.py
│   │   │   ├── source_router.py
│   │   │   ├── source_registry.py
│   │   │   ├── evidence_extractor.py
│   │   │   ├── evidence_ranker.py
│   │   │   ├── source_deduplicator.py
│   │   │   └── citation_service.py
│   │   │
│   │   ├── rag/
│   │   │   ├── retrieval_service.py
│   │   │   ├── embedding_service.py
│   │   │   └── vector_store.py
│   │   │
│   │   ├── llm/
│   │   │   ├── gemini_provider.py
│   │   │   ├── secondary_provider.py
│   │   │   ├── llm_router.py
│   │   │   └── synthesis_service.py
│   │   │
│   │   ├── verification/
│   │   │   ├── fact_checker.py
│   │   │   ├── contradiction_detector.py
│   │   │   └── confidence_service.py
│   │   │
│   │   ├── crop_knowledge_db.py
│   │   ├── weather_service.py
│   │   └── geocoding_service.py
│   │
│   └── knowledge/
│       ├── plants_data.py
│       ├── diseases_data.py
│       └── general_agri_data.py
│
├── tests/
│   ├── test_assistant.py
│   ├── test_research.py
│   ├── test_rag.py
│   ├── test_fact_checker.py
│   └── test_source_ranking.py
│
└── docs/
    ├── MULTI_SOURCE_AI_ARCHITECTURE.md
    ├── RAG_ARCHITECTURE.md
    ├── SOURCE_RANKING.md
    ├── EVIDENCE_FUSION.md
    └── AI_EVALUATION.md
```

---

## 4. Implementation Steps & Verification Strategy
1. Construct modular research packages (`source_registry.py`, `source_router.py`, `evidence_extractor.py`, `evidence_ranker.py`, `source_deduplicator.py`, `citation_service.py`).
2. Construct modular RAG packages (`retrieval_service.py`, `embedding_service.py`, `vector_store.py`).
3. Construct modular LLM and synthesis packages (`gemini_provider.py`, `secondary_provider.py`, `llm_router.py`, `synthesis_service.py`).
4. Construct verification and fact-checking packages (`fact_checker.py`, `contradiction_detector.py`, `confidence_service.py`).
5. Construct assistant coordination services (`assistant_service.py`, `context_service.py`, `conversation_service.py`, `response_service.py`).
6. Wire API endpoints `/api/v1/chat` and `/api/assistant/research`.
7. Write and execute the full test matrix across 5 test modules (`test_assistant.py`, `test_research.py`, `test_rag.py`, `test_fact_checker.py`, `test_source_ranking.py`).
8. Generate benchmark evaluation metrics and write Data Science documentation.
