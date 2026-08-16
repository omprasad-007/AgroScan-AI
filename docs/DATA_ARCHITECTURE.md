# AgroScan AI — Data Architecture & Separation Matrix

## Overview
AgroScan AI strictly separates **Permanent Local Crop Knowledge** from **User-Specific Scan Data**.

---

## 1. Local Crop Knowledge Base (`crop_knowledge_db.py`)
- **Scope**: Permanent agricultural domain knowledge.
- **Supported Crops (10 Core)**:
  1. Tomato (`Solanum lycopersicum`)
  2. Potato (`Solanum tuberosum`)
  3. Rice (`Oryza sativa`)
  4. Wheat (`Triticum aestivum`)
  5. Cotton (`Gossypium hirsutum`)
  6. Soybean (`Glycine max`)
  7. Maize (`Zea mays`)
  8. Chilli (`Capsicum annuum`)
  9. Onion (`Allium cepa`)
  10. Sugarcane (`Saccharum officinarum`)

---

## 2. User Data Layer (SQLAlchemy ORM + LocalStorage Fallback)
- **Scope**: Per-user predictions, recommendations, chat sessions, and farm plots.
- **IDOR Protection**: Evaluated on server-side using `filter(user_id == current_user.id)`.
- **Zero Inter-User Leakage**: User A cannot access or view User B's scan history or farm details.
