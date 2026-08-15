from typing import Dict, Any
from app.services.disease_knowledge_base import get_disease_by_code

class RecommendationService:
    """
    Deterministic Recommendation Engine sourcing strictly from vetted knowledge base.
    Prevents LLM from inventing unverified chemical dosages.
    """

    @staticmethod
    def get_recommendation_for_disease(disease_code: str) -> Dict[str, Any]:
        data = get_disease_by_code(disease_code)
        return {
            "disease_name": data["disease_name"],
            "crop": data["crop"],
            "symptoms": data["symptoms"],
            "organic_treatment": data["organic_treatment"],
            "chemical_treatment": data["chemical_treatment"],
            "prevention": data["prevention"],
            "general_guidance": data["general_guidance"],
            "disclaimer": "Decision-support guidance only. Follow locally approved product labels and agricultural extension guidelines."
        }
