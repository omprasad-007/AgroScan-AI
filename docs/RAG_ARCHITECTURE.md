# AgroScan AI — RAG Architecture & Knowledge Pipeline

## 1. Introduction
The AgroScan AI Retrieval-Augmented Generation (RAG) subsystem supplies localized, structured agronomic and pathological ground truth to the reasoning models. This prevents hallucinations, eliminates reliance on generic prompt text, and guarantees question-specific answers.

---

## 2. RAG Retrieval Architecture

```
User Query ("What is the best soil for mango?")
                     │
                     ▼
           [Entity & Intent Classifier]
        (Intent: SOIL | Plant: Mango)
                     │
                     ▼
             [Targeted Retrieval]
  ├── Structured Field Lookup:
  │   - Soil: Deep, rich alluvial / red loamy
  │   - pH: 5.5 to 7.5
  │   - Drainage: Well-drained, 2-2.5m depth
  └── Vector Semantic Search (Fallback if needed)
                     │
                     ▼
          [Grounding Block Formatter]
                     │
                     ▼
          [LLM Context Injection]
```

---

## 3. Knowledge Base Slices

### 3.1 Plant Profiles (`app/knowledge/plants_data.py`)
Each crop record encapsulates verified agronomic fields:
- `soil` & `pH`: Texture, permeability, acidity/alkalinity bounds.
- `climate`, `temperature`, `rainfall`: Macro-climatic parameters.
- `irrigation`: Water requirement and critical stage intervals (e.g. pre-bloom dry spell).
- `planting` & `spacing`: Pit preparation, graft methods, population density.
- `fertilizer`: NPK split schedules and organic basal manures.
- `growth_stages`, `pests`, `diseases`, `harvesting`, and `post_harvest`.

### 3.2 Disease Pathology Profiles (`app/knowledge/diseases_data.py`)
- `symptoms` & `visual_symptoms`: Diagnostic indicators.
- `causes` & `favorable_conditions`: Pathogen etiology, humidity, temperature thresholds.
- `prevention`, `cultural_control`, `biological_control`, `chemical_management`.
- `safety_notes`: Pre-Harvest Intervals (PHI) and application caveats.

### 3.3 General Agronomic Principles (`app/knowledge/general_agri_data.py`)
- Crop Rotation sequences, Photosynthesis physiology, Integrated Pest Management (IPM), Soil pH remediation.

---

## 4. Cross-Crop Relationship Validation
To prevent cross-contamination (e.g. associating Tomato Late Blight with Mango), `check_disease_plant_relevance` validates biological host ranges before passing pathology facts to the prompt.
