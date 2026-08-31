"""
AgroScan AI — Intelligent Source Router
Determines targeted knowledge repositories to query based on intent, entities, and research mode.
Prevents unbounded queries across irrelevant databases.
"""

from typing import List, Optional
from app.services.intent_service import AgriculturalIntent

class SourceRouter:
    """Selects targeted agricultural research categories according to intent and crop/disease entities."""

    @classmethod
    def route_sources(
        cls,
        query: str,
        plant_name: Optional[str],
        disease_name: Optional[str],
        intent: str,
        research_mode: str = "auto"
    ) -> List[str]:
        q_lower = (query or "").lower().strip()
        p_clean = (plant_name or "").lower()
        d_clean = (disease_name or "").lower()
        
        categories: List[str] = []

        # 1. Mango
        if "mango" in p_clean or "mango" in q_lower or "आंबा" in q_lower:
            if any(w in q_lower or w in d_clean for w in ["mildew", "powdery", "भुरी", "fungus", "disease", "रोग"]):
                categories.append("mango_pathology_powdery_mildew")
            if intent in [AgriculturalIntent.SOIL, AgriculturalIntent.IRRIGATION, AgriculturalIntent.HARVESTING] or any(w in q_lower for w in ["soil", "water", "irrigation", "harvest", "माती", "पाणी", "काढणी"]):
                categories.append("mango_agronomy_soil_water")
            if not categories:
                categories.extend(["mango_pathology_powdery_mildew", "mango_agronomy_soil_water"])

        # 2. Sugarcane
        elif "sugarcane" in p_clean or "sugarcane" in q_lower or "ऊस" in q_lower:
            if any(w in q_lower or w in d_clean for w in ["red rot", "rot", "smut", "disease", "रोग"]):
                categories.append("sugarcane_red_rot_pathology")
            if intent in [AgriculturalIntent.FERTILIZER, AgriculturalIntent.IRRIGATION, AgriculturalIntent.SOIL] or any(w in q_lower for w in ["fertilizer", "npk", "water", "खत", "सिंचन"]):
                categories.append("sugarcane_agronomy_fertilizer_water")
            if not categories:
                categories.extend(["sugarcane_red_rot_pathology", "sugarcane_agronomy_fertilizer_water"])

        # 3. Tomato / Potato / Solanaceous
        elif any(w in p_clean or w in q_lower for w in ["tomato", "potato", "टोमॅटो", "बटाटा", "blight", "करपा", "spot"]):
            categories.append("tomato_potato_blights_pathology")

        # 4. General Biology / Agronomy / Weather
        if intent in [AgriculturalIntent.GENERAL_AGRICULTURE, AgriculturalIntent.WEATHER, AgriculturalIntent.WEATHER_DISEASE_RISK] or any(w in q_lower for w in ["rotation", "photosynthesis", "ipm", "ph", "सामू", "प्रकाशसंश्लेषण", "फेरपालट", "weather", "हवामान"]):
            categories.append("general_agronomy_principles")

        if not categories:
            categories.append("general_agronomy_principles")

        return list(dict.fromkeys(categories))
