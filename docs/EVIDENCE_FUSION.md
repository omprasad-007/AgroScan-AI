# AgroScan AI — Evidence Fusion & Contradiction Detection

## 1. Overview
Evidence Fusion in AgroScan AI normalizes claims across diverse institutional sources, detects potential contradictions, computes inter-source agreement metrics, and prevents chemical treatment hallucinations.

---

## 2. Evidence Object Structure
Every retrieved data point is normalized into a standard representation:

```json
{
  "claim": "High humidity (>85%) combined with overcast skies creates favorable conditions for fungal spore germination.",
  "title": "FAO Technical Guidelines for Mango Disease Management",
  "source": "FAO Plant Production & Protection",
  "source_type": "government_international",
  "url": "https://www.fao.org/agriculture/crops/the-matic-sitemap/theme/pests/en/",
  "published_date": "2023-04-15",
  "retrieved_date": "2026-08-31",
  "relevance_score": 0.94,
  "authority_score": 1.00,
  "recency_score": 0.95,
  "evidence_score": 0.96,
  "final_score": 0.966
}
```

---

## 3. Contradiction Detection & Agreement Scoring

### 3.1 Agreement Levels
- **`high`**: Two or more Level 1/Level 2 sources (Authority $\ge 0.95$) support the same recommendation.
- **`medium`**: Single Level 1/2 source supported by university extension publications.
- **`conflicting`**: Sources differ on curative vs preventive efficacy (e.g. foliar spray vs sett sanitation for systemic vascular pathogens like Red Rot). The assistant explicitly highlights this distinction to the farmer.

---

## 4. Safety Fact-Checking Pipeline
Before the response is delivered:
1. **Banned Chemical Check**: Identifies high-toxicity or banned chemicals (e.g., *Monocrotophos, Endosulfan, Paraquat, Phorate*) and replaces them with approved registered biological or chemical alternatives.
2. **Dosage Integrity**: Prohibits LLM memory hallucination of chemical dosages, defaulting to label recommendations and local university guidelines.
