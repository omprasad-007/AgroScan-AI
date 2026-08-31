# AgroScan AI — Source Ranking & Scoring Methodology

## 1. Multi-Source Hierarchy & Authority Directory

AgroScan AI strictly enforces a multi-tier authority hierarchy to prioritize verified institutional and scientific literature over commercial or unverified web articles.

| Level | Category | Institutional Sources | Base Authority |
|---|---|---|---|
| **Level 1** | Government & International Orgs | FAO, ICAR (IARI, CISH, SBI, IISS), State Ag Departments | **1.00** |
| **Level 1** | Agricultural Universities | TNAU, MPKV Rahuri, PAU Ludhiana, VSI Pune | **0.95** |
| **Level 2** | Agricultural Databases | CABI Crop Protection Compendium, Plantwise, EPPO | **0.95** |
| **Level 2** | Peer-Reviewed Research Papers | Springer, ScienceDirect, APS Phytopathology, Frontiers | **0.95** |
| **Level 3** | University Extension Publications | State Extension Bulletins, Package of Practices | **0.88** |
| **Level 4** | Commercial Agribusiness Sites | Agronomic blogs, Commercial vendor guides | **0.60** |
| **Level 5** | Unverified Web / Forums | User forums, social media (Blocked for treatments) | **0.10** |

---

## 2. Composite Scoring Formula

Candidate evidence items are evaluated using a 4-component weighted scoring function:

$$\text{Final Score} = (\text{Authority} \times 0.40) + (\text{Relevance} \times 0.30) + (\text{Recency} \times 0.15) + (\text{Evidence Quality} \times 0.15)$$

### Component Weights Rationale:
1. **Authority (40%)**: Prevents low-quality commercial websites with keyword stuffing from overtaking peer-reviewed publications.
2. **Relevance (30%)**: Ensures high topical alignment with the farmer's specific query.
3. **Recency (15%)**: Favors recent pathology updates and current pest outbreaks.
4. **Evidence Quality (15%)**: Evaluates clarity, specificity of dosages, and scientific precision.

---

## 3. Example Ranking Calculation

### Scenario: Tomato Disease Query
- **Candidate A: FAO Technical IPM Guideline (2023)**
  - Authority = 1.00
  - Relevance = 0.90
  - Recency = 0.95
  - Evidence Quality = 0.96
  - $\text{Score}_A = (1.00 \times 0.40) + (0.90 \times 0.30) + (0.95 \times 0.15) + (0.96 \times 0.15) = 0.9565$

- **Candidate B: Commercial Fertilizer Blog (2024)**
  - Authority = 0.60
  - Relevance = 0.92
  - Recency = 0.98
  - Evidence Quality = 0.50
  - $\text{Score}_B = (0.60 \times 0.40) + (0.92 \times 0.30) + (0.98 \times 0.15) + (0.50 \times 0.15) = 0.7380$

**Result**: FAO guideline is prioritized as the primary evidence source.
