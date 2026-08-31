"""
AgroScan AI — Local RAG Retrieval Service
Retrieves exact, entity-targeted slices of verified agronomic knowledge.
"""

from typing import Dict, Any, Optional, List
from app.knowledge.plants_data import get_plant_data
from app.knowledge.diseases_data import get_disease_data, check_disease_plant_relevance
from app.knowledge.general_agri_data import get_general_agri_concept
from app.services.intent_service import IntentService, AgriculturalIntent
from app.services.rag.vector_store import VectorStore

class RetrievalService:
    """Retrieves targeted, intent-specific agricultural grounding facts."""

    @classmethod
    def retrieve_grounding(
        cls,
        question: str,
        scan_context: Optional[Dict[str, Any]] = None,
        manual_plant: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        ctx_meta = IntentService.resolve_context(
            query=question,
            scan_context=scan_context,
            manual_plant=manual_plant,
            conversation_history=conversation_history
        )

        intent = ctx_meta["intent"]
        plant_name = ctx_meta["plant"]
        disease_name = ctx_meta["disease"]
        context_source = ctx_meta["context_source"]

        plant_info = get_plant_data(plant_name) if plant_name else None
        disease_info = get_disease_data(disease_name) if disease_name else None
        general_concept = get_general_agri_concept(question)

        # Cross-crop disease relevance filter
        if plant_name and disease_name:
            if not check_disease_plant_relevance(disease_name, plant_name):
                disease_info = None

        grounding_facts: List[str] = []

        if general_concept:
            grounding_facts.append(f"CONCEPT: {general_concept['concept']}")
            grounding_facts.append(f"Definition: {general_concept['definition']}")

        if plant_info:
            cname = plant_info["common_name"]
            grounding_facts.append(f"TARGET PLANT: {cname} ({plant_info['scientific_name']})")
            if intent == AgriculturalIntent.SOIL:
                grounding_facts.append(f"Soil Requirements: {plant_info['soil']} | pH: {plant_info['pH']}")
            elif intent == AgriculturalIntent.IRRIGATION:
                grounding_facts.append(f"Irrigation: {plant_info['irrigation']} | Rainfall: {plant_info['rainfall']}")
            elif intent == AgriculturalIntent.FERTILIZER:
                grounding_facts.append(f"Fertilizer Protocol: {plant_info['fertilizer']}")
            elif intent == AgriculturalIntent.HARVESTING:
                grounding_facts.append(f"Harvesting: {plant_info['harvesting']} | Post-Harvest: {plant_info['post_harvest']}")
            else:
                grounding_facts.append(f"Cultivation: {plant_info['soil']}, {plant_info['irrigation']}")

        if disease_info:
            grounding_facts.append(f"TARGET DISEASE: {disease_info['disease_name']} ({disease_info['scientific_name']})")
            if intent in [AgriculturalIntent.DISEASE_SYMPTOMS, AgriculturalIntent.DISEASE_IDENTIFICATION]:
                grounding_facts.append(f"Symptoms: {disease_info['symptoms']}")
            elif intent == AgriculturalIntent.DISEASE_PREVENTION:
                grounding_facts.append(f"Prevention: {disease_info['prevention']} | Cultural: {disease_info['cultural_control']}")
            elif intent == AgriculturalIntent.DISEASE_TREATMENT:
                grounding_facts.append(f"Biological Control: {disease_info['biological_control']}")
                grounding_facts.append(f"Chemical Management: {disease_info['chemical_management']}")
                grounding_facts.append(f"Safety & Pre-Harvest Interval: {disease_info['safety_notes']}")

        # Vector semantic fallback if facts are empty
        if not grounding_facts:
            semantic_docs = VectorStore.search(question, top_k=2)
            for doc in semantic_docs:
                grounding_facts.append(doc["content"])

        return {
            "intent": intent,
            "plant_name": plant_name,
            "disease_name": disease_name,
            "context_source": context_source,
            "plant_info": plant_info,
            "disease_info": disease_info,
            "general_concept": general_concept,
            "grounding_text": "\n".join(grounding_facts)
        }
