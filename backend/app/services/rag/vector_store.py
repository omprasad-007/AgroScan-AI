"""
AgroScan AI — Local RAG Vector & Knowledge Store
Indexes structured agronomy records, disease pathology profiles, and general agronomic science.
"""

from typing import List, Dict, Any
from app.knowledge.plants_data import PLANTS_KNOWLEDGE_BASE
from app.knowledge.diseases_data import DISEASES_KNOWLEDGE_BASE
from app.knowledge.general_agri_data import GENERAL_AGRI_KNOWLEDGE_BASE
from app.services.rag.embedding_service import EmbeddingService

class VectorStore:
    """Indexed local agricultural knowledge chunks."""

    _documents: List[Dict[str, Any]] = []
    _initialized: bool = False

    @classmethod
    def initialize_store(cls):
        if cls._initialized:
            return

        docs = []

        # 1. Index Plants
        for key, p in PLANTS_KNOWLEDGE_BASE.items():
            content = (
                f"Crop: {p['common_name']} ({p['scientific_name']}). "
                f"Soil: {p['soil']}. pH: {p['pH']}. Climate: {p['climate']}. "
                f"Irrigation: {p['irrigation']}. Fertilizer: {p['fertilizer']}. "
                f"Harvesting: {p['harvesting']}. Pests: {', '.join(p['pests'])}. "
                f"Diseases: {', '.join(p['diseases'])}."
            )
            docs.append({
                "id": f"plant_{key}",
                "type": "plant",
                "entity": p["common_name"],
                "content": content,
                "metadata": p
            })

        # 2. Index Diseases
        for key, d in DISEASES_KNOWLEDGE_BASE.items():
            content = (
                f"Disease: {d['disease_name']} ({d['scientific_name']}). "
                f"Hosts: {', '.join(d['host_plants'])}. "
                f"Symptoms: {d['symptoms']}. Causes: {d['causes']}. "
                f"Prevention: {d['prevention']}. Bio-control: {d['biological_control']}. "
                f"Chemical management: {d['chemical_management']}."
            )
            docs.append({
                "id": f"disease_{key}",
                "type": "disease",
                "entity": d["disease_name"],
                "content": content,
                "metadata": d
            })

        # 3. Index General Agronomy Concepts
        for key, g in GENERAL_AGRI_KNOWLEDGE_BASE.items():
            content = f"Concept: {g['concept']}. Definition: {g['definition']}."
            docs.append({
                "id": f"general_{key}",
                "type": "general_agri",
                "entity": g["concept"],
                "content": content,
                "metadata": g
            })

        cls._documents = docs
        cls._initialized = True

    @classmethod
    def search(cls, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        cls.initialize_store()
        scored = []
        for doc in cls._documents:
            sim = EmbeddingService.compute_similarity(query, doc["content"])
            scored.append((sim, doc))

        # Sort descending by similarity
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for sim, doc in scored[:top_k] if sim > 0.05]
