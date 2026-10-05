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
    },
    "soil_salinity_reclamation": {
        "concept": "Soil Salinity & Sodicity Reclamation",
        "definition": "Management protocols for salt-affected soils (Saline, Sodic/Alkali, and Saline-Sodic) to restore root-zone osmotic balance and soil physical structure.",
        "management_guidelines": [
            "Saline Soils (ECe > 4.0 dS/m, ESP < 15%, pH < 8.5): High neutral soluble salts (chlorides, sulfates of sodium/calcium). Management: Leaching with high quality low-salinity water through subsurface tile drainage. Provide drainage channels to carry washed salts away from root zone.",
            "Sodic / Alkali Soils (ECe < 4.0 dS/m, ESP > 15%, pH > 8.5): High exchangeable sodium causing soil particle dispersion, crusting, and poor aeration. Management: Apply Agricultural Gypsum (CaSO4.2H2O @ 5-10 t/ha based on Gypsum Requirement test) to displace exchangeable Na+ with Ca²⁺, followed by flushing. Incorporate Dhaincha green manure.",
            "Saline-Sodic Soils: Apply gypsum first to replace sodium with calcium, then leach soluble salts. Never leach before adding gypsum, as it causes severe soil dispersion and impermeable hardpan."
        ]
    },
    "drone_spraying_tech": {
        "concept": "Kisan Drone Agricultural Spraying Protocols",
        "definition": "Unmanned Aerial Vehicle (UAV) precision spraying of agrochemicals and liquid nano-fertilizers for rapid coverage, ultra-low volume efficiency, and farmer safety.",
        "management_guidelines": [
            "Flight Parameters: Optimum flight altitude: 1.5 to 2.5 meters above crop canopy. Optimum flight speed: 3 to 5 m/s (10-18 km/h).",
            "Spray Volume: Ultra-Low Volume (ULV): 20 to 30 liters of water per hectare (compared to 400-500 L/ha with traditional knapsack sprayers). Agrochemical chemical active ingredient per acre remains identical to label recommendation.",
            "Weather Limitations: NEVER spray when wind speed exceeds 10-12 km/h (causes severe spray drift). Avoid spraying when ambient temperature >35°C or in midday heat to prevent droplet evaporation.",
            "Nozzle & Adjuvants: Use centrifugal rotary atomizers or anti-drift flat-fan nozzles with droplet size between 150-250 microns. Always mix a non-ionic organosilicone surfactant/spreader."
        ]
    },
    "polyhouse_hydroponics": {
        "concept": "Protected Cultivation & Hydroponic Systems",
        "definition": "Controlled Environment Agriculture (CEA) utilizing polyhouses, shade nets, and soil-less hydroponic systems (NFT, Cocopeat substrate) for high-value year-round horticulture.",
        "management_guidelines": [
            "Naturally Ventilated Polyhouse (NVPH): 200-micron UV-stabilized polyethylene cladding with 40-mesh insect-proof netting on side vents. Protects against heavy rains, hail, insect vectors (whiteflies/thrips), and viral epidemics.",
            "Hydroponic Fertigation: Maintain Nutrient Film Technique (NFT) or Dutch Bucket substrate solution EC at 1.5 - 2.5 dS/m and pH precisely at 5.8 - 6.2 for maximum nutrient solubility.",
            "Root Aeration: Maintain dissolved oxygen (DO) >6-8 ppm in hydroponic reservoir tanks to prevent Pythium root rot.",
            "Climate Control: Use foggers / misters and thermal shade screens (50% shade) during peak summer to keep internal temperatures below 32°C."
        ]
    },
    "bio_stimulants_seaweed": {
        "concept": "Agricultural Bio-stimulants, Humic Acids & Seaweed Extracts",
        "definition": "Natural substances and micro-organisms that enhance plant growth, nutrient uptake efficiency, abiotic stress tolerance (drought/heat/chilling), and crop quality traits independent of nutrient content.",
        "management_guidelines": [
            "Humic & Fulvic Acids: Extracted from Leonardite. Humic acid improves soil cation exchange capacity (CEC), chelates micronutrients, and enhances root branching. Fulvic acid acts as an effective foliar cellular carrier. Application: 1-2 kg/ha humic acid granules soil application or 2 ml/L liquid foliar spray.",
            "Seaweed Extracts (Ascophyllum nodosum / Kappaphycus alvarezii): Rich in natural cytokinins, auxins, betaines, and mannitol. Spraying @ 2-3 ml/L during flower initiation and early fruit set mitigates temperature stress and reduces flower/fruit drop.",
            "Amino Acid Complexes: Enzymatically hydrolyzed plant/protein amino acids save plant metabolic energy during abiotic drought/heat stress. Dose: 2-3 ml/L foliar spray.",
            "Mycorrhiza (VAM - Vesicular Arbuscular Mycorrhizae): Symbiotic root fungus that expands root surface area 100-fold, dramatically enhancing Phosphorus and moisture uptake under water stress."
        ]
    },
    "natural_farming_zbnf": {
        "concept": "Natural & Regenerative Farming Formulations (ZBNF)",
        "definition": "Traditional, low-cost bio-formulations utilizing indigenous cow dung, cow urine, botanical extracts, and local soil microbes to foster living soil ecosystems without synthetic chemicals.",
        "management_guidelines": [
            "Jeevamrut (Microbial Culture): Mix 10 kg desi cow dung + 10 L desi cow urine + 2 kg jaggery + 2 kg pulse flour (besan) + handful of virgin forest/field bund soil in 200 L water. Ferment for 48-72 hours under shade. Apply 200 L/acre through irrigation water or as 10% foliar spray every 21 days to activate soil beneficial bacteria.",
            "Beejamrut (Seed Priming): Mix 5 kg cow dung + 5 L cow urine + 50g slaked lime in 20 L water. Used as protective antimicrobial seed treatment before sowing.",
            "Neemastra (Sucking Pest Control): 5 kg crushed neem leaves + 5 L cow urine + 2 kg cow dung in 100 L water. Ferment 24 hours. Effective against aphids, whiteflies, and jassids.",
            "Brahmastra & Dashparni Ark: Multi-botanical extracts (Neem, Karanj, Castor, Custard apple, Papaya, Calotropis leaves) fermented in cow urine for managing chewing caterpillars, borers, and severe insect attacks."
        ]
    },
    "post_harvest_cold_storage": {
        "concept": "Post-Harvest Management, Pre-Cooling & Cold Chain",
        "definition": "Post-harvest operations that arrest respiration, retard moisture loss, suppress microbial decay, and preserve nutritional and sensory quality from farm gate to consumer.",
        "management_guidelines": [
            "Pre-Cooling: Rapid removal of field heat within 2-4 hours of harvesting using forced-air cooling or hydro-cooling to lower pulp temperature down to recommended storage limits.",
            "Ethylene Management: Ethylene (C2H4) accelerates ripening and senescence. Use potassium permanganate (KMnO4) ethylene scrubber pads or 1-MCP (1-Methylcyclopropene @ 1 ppm) in storage rooms to extend storage life of climacteric fruits (mango, banana, papaya, tomato).",
            "Relative Humidity Control: Maintain 90-95% RH in cold rooms using ultrasonic humidifiers to prevent moisture evaporation, fruit shriveling, and weight loss.",
            "Clean Handling: Disinfect washing tanks with sodium hypochlorite (100-150 ppm active chlorine at pH 6.5-7.0) or ozone water to prevent cross-contamination by post-harvest decay fungi."
        ]
    },
    "frost_cold_wave_protection": {
        "concept": "Frost & Cold Wave Crop Protection Protocols",
        "definition": "Emergency and cultural measures to protect sensitive crops and orchards from freezing injury and radiation frost damage when temperatures drop near 0°C.",
        "management_guidelines": [
            "Smudge Burning / Smoke Blanketing: Burn moist crop straw, cow dung cakes, and green biomass on northern and western field borders at 3-4 AM to create a dense thermal smoke blanket that traps terrestrial infrared radiation.",
            "Light Night Irrigation: Apply light surface irrigation during anticipated cold nights. Water has a high specific heat capacity and releases latent heat of fusion (80 cal/g) as it cools, keeping canopy temperature 2-3°C higher than ambient air.",
            "Foliar Chemical Spray: Spray 0.1% Thiourea (1 g/L) or 0.1% Potassium Nitrate (13:0:45 @ 5 g/L) 2 days before cold wave to increase cellular osmotic concentration and prevent ice crystal formation in plant cells."
        ]
    },
    "weed_management_selective": {
        "concept": "Integrated Weed Management & Selective Herbicides",
        "definition": "Scientific weed control combining cultural, mechanical, and selective chemical herbicides to eliminate weed-crop competition during the critical first 30-45 days.",
        "management_guidelines": [
            "Critical Period of Weed Competition (CPWC): The initial 30-45 days after sowing is critical. Weeds competing during this window can reduce crop yields by 30-70%.",
            "Pre-Emergence Herbicides (Apply within 0-48 hours of sowing on moist soil): Pendimethalin 38.7% CS (600-700 ml/acre) for cotton/soybean/pulses; Atrazine 50% WP (500 g/acre) for maize/sugarcane; Oxyfluorfen 23.5% EC (200 ml/acre) for onion/garlic.",
            "Post-Emergence Herbicides (Apply at 2-4 weed leaf stage): Quizalofop-ethyl 5% EC (400 ml/acre) for selective control of grassy weeds in broadleaf crops (soybean, cotton, pulses); Imazethapyr 10% SL (300 ml/acre) for mixed weeds in soybean/groundnut.",
            "Safe Application: Always use flood-jet or flat-fan nozzles with a hood to avoid spray drift onto crop leaves."
        ]
    },
    "mulching_plastic_organic": {
        "concept": "Agricultural Mulching Techniques & Moisture Conservation",
        "definition": "Covering the soil surface around crop plants with organic materials or plastic film to suppress weeds, conserve soil moisture, regulate root zone temperature, and prevent soil erosion.",
        "management_guidelines": [
            "Silver-Black Polyethylene Mulch (25-30 micron): Silver side facing upward reflects 70% sunlight, cooling the root zone and disorienting aphids/thrips; black side facing downward completely blocks photosynthetically active radiation to stop weed growth. Saves 40-50% irrigation water and prevents soil encrustation.",
            "Organic Biomass Mulch: Applying 5-10 tonnes/ha of sugarcane trash, wheat straw, or shredded crop residue builds soil organic carbon (SOC) and promotes earthworm activity.",
            "Fruit Quality: Keeps developing melons, tomatoes, and strawberries off wet soil, preventing soil-borne fruit rots and blossom end rot."
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
    if "frost" in q_clean or "cold wave" in q_clean or "थंडी" in q_clean or "धुके" in q_clean or "दव" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["frost_cold_wave_protection"]
    if "weed" in q_clean or "herbicide" in q_clean or "तण" in q_clean or "तणनाशक" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["weed_management_selective"]
    if "mulch" in q_clean or "mulching" in q_clean or "आच्छादन" in q_clean or "मल्चिंग" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["mulching_plastic_organic"]
    if "salinity" in q_clean or "sodic" in q_clean or "alkali" in q_clean or "खारवट" in q_clean or "चोपण" in q_clean or "gypsum" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["soil_salinity_reclamation"]
    if "drone" in q_clean or "ड्रोन" in q_clean or "uav" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["drone_spraying_tech"]
    if "polyhouse" in q_clean or "hydroponic" in q_clean or "पॉलीहाऊस" in q_clean or "शेडनेट" in q_clean or "हायड्रोपोनिक्स" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["polyhouse_hydroponics"]
    if "biostimulant" in q_clean or "seaweed" in q_clean or "humic" in q_clean or "बायोस्टिम्युलंट" in q_clean or "ह्युमिक" in q_clean or "fulvic" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["bio_stimulants_seaweed"]
    if "zbnf" in q_clean or "jeevamrut" in q_clean or "natural farming" in q_clean or "जीवामृत" in q_clean or "नैसर्गिक शेती" in q_clean or "दशपर्णी" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["natural_farming_zbnf"]
    if "cold storage" in q_clean or "pre-cooling" in q_clean or "शीतगृह" in q_clean or "post-harvest" in q_clean or "पक्वता" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["post_harvest_cold_storage"]
    if "ph" in q_clean or "soil health" in q_clean or "मातीचा सामू" in q_clean or "acidic" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["soil_health_ph"]
    if "drip" in q_clean or "irrigation" in q_clean or "water" in q_clean or "ठिबक" in q_clean:
        return GENERAL_AGRI_KNOWLEDGE_BASE["water_management"]
        
    return None
