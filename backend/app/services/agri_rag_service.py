"""
AgroScan AI — Dynamic Retrieval-Augmented Generation (RAG) Service
Retrieves precise, intent-specific agricultural facts from structured knowledge bases
(Plants, Diseases, and General Agronomy) without sending massive irrelevant databases to LLM.
"""

from typing import List, Dict, Any, Optional
from app.knowledge.plants_data import get_plant_data
from app.knowledge.diseases_data import get_disease_data, check_disease_plant_relevance
from app.knowledge.general_agri_data import get_general_agri_concept
from app.services.intent_service import IntentService, AgriculturalIntent

class AgriRAGService:
    """Retrieves targeted, query-specific agricultural grounding knowledge."""

    @classmethod
    def is_weather_relevant(cls, question: str) -> bool:
        """Returns True only when the question explicitly needs real-time weather metrics."""
        if not question:
            return False
        intent = IntentService.detect_intent(question)
        return intent in [AgriculturalIntent.WEATHER, AgriculturalIntent.WEATHER_DISEASE_RISK]

    @classmethod
    def retrieve_grounding(
        cls,
        question: str,
        scan_context: Optional[Dict[str, Any]] = None,
        manual_plant: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Executes intent detection, entity resolution, and targeted knowledge retrieval.
        Returns structured grounding payload.
        """
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

        # Ensure disease relevance to target plant
        if plant_name and disease_name:
            if not check_disease_plant_relevance(disease_name, plant_name):
                disease_info = None  # Prevent cross-crop disease confusion

        grounding_facts = []

        # 1. General Agronomy Concepts (Photosynthesis, Crop Rotation, IPM, Soil pH)
        if general_concept:
            grounding_facts.append(f"CONCEPT: {general_concept['concept']}")
            grounding_facts.append(f"Definition: {general_concept['definition']}")
            if "key_principles" in general_concept:
                grounding_facts.append("Principles:\n- " + "\n- ".join(general_concept["key_principles"]))
            if "four_pillars" in general_concept:
                grounding_facts.append("IPM Pillars:\n- " + "\n- ".join(general_concept["four_pillars"]))
            if "management_guidelines" in general_concept:
                grounding_facts.append("Guidelines:\n- " + "\n- ".join(general_concept["management_guidelines"]))
            if "recommended_sequences" in general_concept:
                grounding_facts.append("Crop Sequences:\n- " + "\n- ".join(general_concept["recommended_sequences"]))

        # 2. Plant-Specific Grounding by Intent
        if plant_info:
            cname = plant_info["common_name"]
            sname = plant_info["scientific_name"]
            grounding_facts.append(f"TARGET PLANT: {cname} ({sname}) | Type: {plant_info['plant_type']}")

            if intent == AgriculturalIntent.SOIL:
                grounding_facts.append(f"Soil Requirements: {plant_info['soil']}")
                grounding_facts.append(f"Optimal Soil pH: {plant_info['pH']}")

            elif intent == AgriculturalIntent.IRRIGATION:
                grounding_facts.append(f"Irrigation Guidelines: {plant_info['irrigation']}")
                grounding_facts.append(f"Rainfall & Climate: {plant_info['rainfall']} | {plant_info['climate']}")

            elif intent in [AgriculturalIntent.FERTILIZER, AgriculturalIntent.NUTRITION]:
                grounding_facts.append(f"Fertilizer & Nutrition Protocol: {plant_info['fertilizer']}")

            elif intent == AgriculturalIntent.HARVESTING:
                grounding_facts.append(f"Harvesting Maturity & Methods: {plant_info['harvesting']}")
                grounding_facts.append(f"Post-Harvest & Storage: {plant_info['post_harvest']}")

            elif intent == AgriculturalIntent.PLANTING:
                grounding_facts.append(f"Planting & Sowing Method: {plant_info['planting']}")
                grounding_facts.append(f"Recommended Spacing: {plant_info['spacing']}")
                grounding_facts.append(f"Climate & Temp: {plant_info['climate']} | {plant_info['temperature']}")

            elif intent == AgriculturalIntent.GROWTH_STAGE:
                grounding_facts.append("Growth Stages:\n- " + "\n- ".join(plant_info["growth_stages"]))

            elif intent == AgriculturalIntent.PEST:
                grounding_facts.append("Major Pests & IPM:\n- " + "\n- ".join(plant_info["pests"]))
                grounding_facts.append(f"Prevention: {plant_info['prevention']}")

            elif intent in [AgriculturalIntent.DISEASE_IDENTIFICATION, AgriculturalIntent.DISEASE_SYMPTOMS]:
                if not disease_info:
                    grounding_facts.append("Major Diseases Affecting this Crop:\n- " + "\n- ".join(plant_info["diseases"]))

            elif intent == AgriculturalIntent.CROP_MANAGEMENT:
                grounding_facts.append(f"Cultural Care & Prevention: {plant_info['prevention']}")
                grounding_facts.append(f"Spacing & Canopy Management: {plant_info['spacing']}")

        # 3. Disease-Specific Grounding by Intent
        if disease_info:
            dname = disease_info["disease_name"]
            dsname = disease_info["scientific_name"]
            grounding_facts.append(f"TARGET DISEASE: {dname} ({dsname}) | Pathogen: {disease_info['pathogen_type']}")

            if intent in [AgriculturalIntent.DISEASE_SYMPTOMS, AgriculturalIntent.DISEASE_IDENTIFICATION]:
                grounding_facts.append(f"Diagnostic Symptoms: {disease_info['symptoms']}")
                grounding_facts.append("Visual Markers:\n- " + "\n- ".join(disease_info["visual_symptoms"]))

            elif intent == AgriculturalIntent.DISEASE_CAUSE:
                grounding_facts.append(f"Etiology & Causes: {disease_info['causes']}")
                grounding_facts.append(f"Favorable Conditions: {disease_info['favorable_conditions']}")
                grounding_facts.append(f"Spread Mechanisms: {disease_info['spread_conditions']}")

            elif intent == AgriculturalIntent.DISEASE_PREVENTION:
                grounding_facts.append(f"Preventive Measures: {disease_info['prevention']}")
                grounding_facts.append(f"Cultural Controls: {disease_info['cultural_control']}")
                grounding_facts.append(f"Biological Prevention: {disease_info['biological_control']}")

            elif intent == AgriculturalIntent.DISEASE_TREATMENT:
                grounding_facts.append(f"Biological / Organic Remedies: {disease_info['biological_control']}")
                grounding_facts.append(f"Approved Chemical Controls: {disease_info['chemical_management']}")
                grounding_facts.append(f"Safety & PHI: {disease_info['safety_notes']}")
                grounding_facts.append(f"Expert Escalation: {disease_info['when_to_seek_expert_help']}")

            else:
                # Default disease summary for other questions
                grounding_facts.append(f"Symptoms: {disease_info['symptoms']}")
                grounding_facts.append(f"Organic Management: {disease_info['biological_control']}")
                grounding_facts.append(f"Chemical Management: {disease_info['chemical_management']}")

        return {
            "intent": intent,
            "plant_name": plant_name,
            "disease_name": disease_name,
            "context_source": context_source,
            "plant_info": plant_info,
            "disease_info": disease_info,
            "general_concept": general_concept,
            "grounding_text": "\n".join(grounding_facts) if grounding_facts else ""
        }

    @classmethod
    def build_reference_block(
        cls,
        question: str,
        scan_context: Optional[Dict[str, Any]] = None,
        manual_plant: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Constructs concise grounding text block for LLM system prompt."""
        result = cls.retrieve_grounding(
            question=question,
            scan_context=scan_context,
            manual_plant=manual_plant,
            conversation_history=conversation_history
        )
        text = result["grounding_text"].strip()
        if not text:
            return ""
        return f"--- VERIFIED AGRICULTURAL KNOWLEDGE BASE GROUNDING ---\n{text}\n-------------------------------------------------------"
