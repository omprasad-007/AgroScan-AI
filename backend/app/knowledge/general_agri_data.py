"""
AgroScan AI — General Agricultural Science Knowledge Base
Contains foundational agricultural principles: Crop Rotation, Photosynthesis,
Integrated Pest Management (IPM), Soil pH & Salinity, Bio-fertilizers, and Water Management.
"""

from typing import Dict, Any, Optional

GENERAL_AGRI_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "crop_rotation": {
        "concept": "Crop Rotation",
        "definition": "Crop rotation is the systematic practice of growing different types of crops sequentially on the same land across seasons and years, rather than growing a single monoculture continuously.",
        "key_principles": [
            "Break Pest and Pathogen Cycles: Soil-borne fungi, nematodes, and host-specific insect pests build up when the same crop is grown repeatedly. Rotating with a non-host plant starves out the pathogen.",
            "Replenish Soil Nutrients: Alternating deep-rooted crops with shallow-rooted crops taps nutrients from different soil strata. Legumes (e.g. soybean, gram, groundnut) fix atmospheric nitrogen into the root zone via symbiotic Rhizobium bacteria, enriching the soil for subsequent heavy-feeding cereals (e.g. wheat, maize, sugarcane).",
            "Improve Soil Structure: Alternating fibrous root crops (like grasses/cereals) with tap root crops aerates the soil, improves water infiltration, and builds soil organic matter.",
            "Weed Suppression: Different crop planting schedules, canopy densities, and competitive habits disrupt weed life cycles."
        ],
        "recommended_sequences": [
            "Solanaceous rotation: Tomato/Potato -> Legume (Soybean/Gram) -> Cereal (Wheat/Maize) -> Green Manure (Sunnhemp/Dhaincha). Never plant Solanaceous crops (Tomato, Potato, Chilli, Brinjal) back-to-back.",
            "Cotton rotation: Cotton -> Wheat / Chickpea -> Green Manure.",
            "Sugarcane rotation: Sugarcane (Main + 1 Ratoon) -> Paddy / Soybean -> Wheat / Onion."
        ]
    },
    "photosynthesis": {
        "concept": "Photosynthesis & Plant Physiology",
        "definition": "Photosynthesis is the fundamental biological process by which green plants utilize chlorophyll pigments to capture solar light energy, converting carbon dioxide (CO2) from the air and water (H2O) from the soil into glucose/carbohydrates (chemical energy) and releasing oxygen (O2) into the atmosphere.",
        "chemical_equation": "6 CO2 + 6 H2O + Light Energy -> C6H12O6 (Glucose) + 6 O2",
        "agricultural_importance": [
            "Primary Driver of Crop Yield: Every kilogram of grain, fiber, fruit, or biomass produced by a crop is derived directly from photosynthetic carbon assimilation.",
            "Impact of Foliar Diseases: Leaf-infecting diseases (such as leaf blights, powdery mildew, rusts, and leaf spots) destroy active green chlorophyll and block sunlight, causing severe reduction in photosynthesis, poor fruit/grain filling, and stunted yields.",
            "Canopy Management: Proper plant spacing, weeding, pruning, and trellising ensure maximum sunlight interception by all leaf layers across the plant canopy.",
            "Stomatal Conductance: Moisture stress causes plants to close leaf stomata to conserve water, which halts CO2 intake and stops photosynthesis."
        ]
    },
    "integrated_pest_management": {
        "concept": "Integrated Pest Management (IPM)",
        "definition": "Integrated Pest Management (IPM) is an ecologically sound, comprehensive approach that combines biological, cultural, physical/mechanical, and chemical tools in a harmonious sequence to keep pest populations below Economic Threshold Levels (ETL), minimizing hazards to human health and the environment.",
        "four_pillars": [
            "1. Cultural Control: Deep summer plowing, crop rotation, trap cropping (e.g. marigold for tomato fruit borer / nematodes, castor for Spodoptera), balanced fertilization, and clean field sanitation.",
            "2. Mechanical / Physical Control: Yellow sticky traps (for whiteflies, aphids, leaf miners), blue sticky traps (for thrips), light traps (for moths/beetles), and pheromone traps (for bollworms and armyworms).",
            "3. Biological Control: Conserving and releasing natural predators and parasitoids (e.g. Trichogramma wasps, Chrysoperla green lacewings, ladybird beetles) and bio-pesticides (Neem oil, Bacillus thuringiensis, Beauveria bassiana, Metarhizium).",
            "4. Chemical Control: Used only as a last resort when pest population crosses the Economic Threshold Level (ETL). Utilize selective, green-label, targeted molecules at recommended label doses."
        ]
    },
    "soil_health_ph": {
        "concept": "Soil Health, pH, and Nutrition",
        "definition": "Soil pH measures the acidity or alkalinity of the soil solution on a scale of 0 to 14. A neutral pH of 6.0 to 7.5 provides the highest availability of primary nutrients (N, P, K) and micronutrients.",
        "management_guidelines": [
            "Acidic Soils (pH < 6.0): Restricts Phosphorus availability and can cause Aluminum/Manganese toxicity. Corrected by applying Agricultural Lime (Calcium Carbonate - CaCO3) or Dolomite.",
            "Alkaline / Sodic Soils (pH > 8.0): Locks up micronutrients (Zinc, Iron, Manganese, Boron) causing chlorosis. Corrected by incorporating Agricultural Gypsum (Calcium Sulfate - CaSO4.2H2O), elemental sulfur, and abundant organic compost.",
            "Soil Organic Carbon (SOC): Adding 10-25 tonnes/ha of well-rotted Farm Yard Manure (FYM), vermicompost, or green manuring with Dhaincha (Sesbania) / Sunnhemp increases water holding capacity, promotes beneficial soil microbes, and buffers soil pH."
        ]
    },
    "water_management": {
        "concept": "Water Management & Micro-Irrigation",
        "definition": "Efficient irrigation delivers adequate root-zone moisture while preventing waterlogging, anaerobic root stress, and foliar disease outbreaks.",
        "management_guidelines": [
            "Drip Irrigation: Delivers water and water-soluble fertilizers (fertigation) directly to the root zone at low pressure. Saves 40-60% water, increases fertilizer use efficiency by 30-40%, and prevents foliar wetting that triggers fungal blights.",
            "Vafsa Condition: The optimum balance of 50% air and 50% water in soil pore spaces. Irrigation should be scheduled to maintain Vafsa rather than creating flooded anaerobic conditions.",
            "Critical Growth Stages: Moisture stress must be strictly avoided during flowering, pollination, and grain/fruit filling stages across all crops."
        ]
    }
}

def get_general_agri_concept(query: str) -> Optional[Dict[str, Any]]:
    """Lookup general agricultural concept from knowledge base."""
    if not query:
        return None
        
    q_clean = query.lower().strip()
    
    if "rotation" in q_clean or "फेरपालट" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["crop_rotation"]
    if "photosynthesis" in q_clean or "प्रकाशसंश्लेषण" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["photosynthesis"]
    if "ipm" in q_clean or "integrated pest" in q_clean or "कीड व्यवस्थापन" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["integrated_pest_management"]
    if "ph" in q_clean or "soil health" in q_clean or "मातीचा सामू" in q_clean or "acidic" in q_clean or "saline" in q_clean or "alkaline" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["soil_health_ph"]
    if "drip" in q_clean or "irrigation" in q_clean or "water" in q_clean or "ठिबक" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["water_management"]
        
    return None
