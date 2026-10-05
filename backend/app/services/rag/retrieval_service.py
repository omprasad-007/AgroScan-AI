"""
AgroScan AI — Local RAG Retrieval Service
Retrieves exact, entity-targeted slices of verified agronomic knowledge.
Generates query-dependent search representations and isolates facts by intent.
"""

from typing import Dict, Any, Optional, List
from app.knowledge.plants_data import get_plant_data
from app.knowledge.diseases_data import get_disease_data, check_disease_plant_relevance
from app.knowledge.general_agri_data import get_general_agri_concept
from app.services.intent_service import IntentService, AgriculturalIntent
from app.services.rag.vector_store import VectorStore

class RetrievalService:
    """Retrieves targeted, intent-specific agricultural grounding facts and generates dynamic queries."""

    @classmethod
    def generate_retrieval_query(
        cls,
        intent: str,
        plant_name: Optional[str] = None,
        disease_name: Optional[str] = None,
        question: Optional[str] = None
    ) -> str:
        """Generates intent-grounded search query for RAG and research engines."""
        terms = []
        if plant_name:
            terms.append(plant_name.lower())
        if disease_name:
            terms.append(disease_name.lower())

        intent_keywords = {
            AgriculturalIntent.IRRIGATION: "irrigation water requirement schedule drip moisture",
            AgriculturalIntent.FERTILIZER: "fertilizer NPK dosage split application nutrients",
            AgriculturalIntent.NUTRITION: "micronutrient deficiency chlorosis symptoms zinc boron",
            AgriculturalIntent.SOIL: "soil type pH drainage land preparation loam",
            AgriculturalIntent.HARVESTING: "harvesting maturity indicators post-harvest storage",
            AgriculturalIntent.PLANTING: "sowing planting method seed rate spacing",
            AgriculturalIntent.GROWTH_STAGE: "growth stages tillering flowering vegetative",
            AgriculturalIntent.DISEASE_IDENTIFICATION: "disease symptoms identification diagnosis signs",
            AgriculturalIntent.DISEASE_SYMPTOMS: "foliar symptoms lesions visual signs leaf spots",
            AgriculturalIntent.DISEASE_CAUSE: "pathogen causes etiology favorable conditions origin",
            AgriculturalIntent.DISEASE_PREVENTION: "prevention cultural control sanitation crop rotation",
            AgriculturalIntent.DISEASE_TREATMENT: "treatment organic bio-spray chemical fungicide dosage",
            AgriculturalIntent.DISEASE_TRANSMISSION: "transmission spread airborne spores transmission mechanism",
            AgriculturalIntent.PEST: "pest identification damage symptoms life cycle",
            AgriculturalIntent.PEST_MANAGEMENT: "pest control IPM sticky traps biological management",
            AgriculturalIntent.WEATHER_DISEASE_RISK: "weather humidity disease outbreak risk spore germination",
            AgriculturalIntent.WEATHER: "weather temperature rainfall humidity forecast",
            AgriculturalIntent.SCAN_EXPLANATION: "diagnostic scan confidence leaf symptoms visual analysis",
            AgriculturalIntent.GENERAL_AGRICULTURE: "agronomy principles farming practices crop physiology"
        }

        terms.append(intent_keywords.get(intent, "agronomy management"))
        return " ".join(terms)

    @classmethod
    def retrieve_grounding(
        cls,
        question: str,
        scan_context: Optional[Dict[str, Any]] = None,
        manual_plant: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, Any]]] = None
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
            if "key_principles" in general_concept:
                grounding_facts.append("Principles:\n- " + "\n- ".join(general_concept["key_principles"]))

        if plant_info:
            cname = plant_info["common_name"]
            grounding_facts.append(f"TARGET PLANT: {cname} ({plant_info['scientific_name']})")
            if intent == AgriculturalIntent.SOIL:
                grounding_facts.append(f"Soil Requirements: {plant_info['soil']} | pH: {plant_info['pH']}")
            elif intent == AgriculturalIntent.IRRIGATION:
                grounding_facts.append(f"Irrigation: {plant_info['irrigation']} | Rainfall: {plant_info['rainfall']}")
            elif intent in [AgriculturalIntent.FERTILIZER, AgriculturalIntent.NUTRITION]:
                grounding_facts.append(f"Fertilizer Protocol: {plant_info['fertilizer']}")
            elif intent == AgriculturalIntent.HARVESTING:
                grounding_facts.append(f"Harvesting: {plant_info['harvesting']} | Post-Harvest: {plant_info['post_harvest']}")
            elif intent == AgriculturalIntent.PLANTING:
                grounding_facts.append(f"Planting: {plant_info['planting']} | Spacing: {plant_info['spacing']}")
            elif intent == AgriculturalIntent.PEST:
                grounding_facts.append("Major Pests:\n- " + "\n- ".join(plant_info["pests"]))
                grounding_facts.append(f"Pest Prevention: {plant_info['prevention']}")
            else:
                grounding_facts.append(f"Cultivation: {plant_info['soil']}, {plant_info['irrigation']}")

        if disease_info:
            grounding_facts.append(f"TARGET DISEASE: {disease_info['disease_name']} ({disease_info['scientific_name']})")
            if intent in [AgriculturalIntent.DISEASE_SYMPTOMS, AgriculturalIntent.DISEASE_IDENTIFICATION, AgriculturalIntent.SCAN_EXPLANATION]:
                grounding_facts.append(f"Symptoms: {disease_info['symptoms']}")
                if "visual_symptoms" in disease_info:
                    grounding_facts.append("Visual Markers:\n- " + "\n- ".join(disease_info["visual_symptoms"]))
            elif intent == AgriculturalIntent.DISEASE_CAUSE:
                grounding_facts.append(f"Causes & Pathogen: {disease_info['causes']}")
                grounding_facts.append(f"Favorable Conditions: {disease_info['favorable_conditions']}")
            elif intent == AgriculturalIntent.DISEASE_TRANSMISSION:
                grounding_facts.append(f"Spread & Transmission: {disease_info['spread_conditions']}")
                grounding_facts.append(f"Favorable Conditions: {disease_info['favorable_conditions']}")
            elif intent == AgriculturalIntent.DISEASE_PREVENTION:
                grounding_facts.append(f"Prevention: {disease_info['prevention']} | Cultural: {disease_info['cultural_control']}")
            elif intent == AgriculturalIntent.DISEASE_TREATMENT:
                grounding_facts.append(f"Biological Control: {disease_info['biological_control']}")
                grounding_facts.append(f"Chemical Management: {disease_info['chemical_management']}")
                grounding_facts.append(f"Safety & Pre-Harvest Interval: {disease_info['safety_notes']}")
            elif intent == AgriculturalIntent.WEATHER_DISEASE_RISK:
                grounding_facts.append(f"Weather Favorability: {disease_info['favorable_conditions']}")
                grounding_facts.append(f"Spread Risk: {disease_info['spread_conditions']}")

        # Vector semantic fallback if facts are empty
        if not grounding_facts:
            semantic_docs = VectorStore.search(question, top_k=2)
            for doc in semantic_docs:
                grounding_facts.append(doc["content"])

        retrieval_query = cls.generate_retrieval_query(
            intent=intent,
            plant_name=plant_name,
            disease_name=disease_name,
            question=question
        )

        return {
            "intent": intent,
            "plant_name": plant_name,
            "disease_name": disease_name,
            "context_source": context_source,
            "plant_info": plant_info,
            "disease_info": disease_info,
            "general_concept": general_concept,
            "retrieval_query": retrieval_query,
            "grounding_text": "\n".join(grounding_facts)
        }
