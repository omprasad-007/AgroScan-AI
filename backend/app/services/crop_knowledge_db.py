"""
AgroScan AI — Local Agricultural Crop Knowledge Base
Provides structured agricultural information for 10 core crops.
Separated completely from per-user scan data and predictions.
"""

from typing import Dict, Any, List, Optional

CROP_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "tomato": {
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "climate": "Warm temperate & tropical climate. Ideal temperature: 20°C - 27°C.",
        "soil": "Well-drained sandy loam soil rich in organic matter. pH: 6.0 - 6.8.",
        "planting": "Transplant 4-5 week old nursery seedlings into raised beds.",
        "spacing": "60 cm row-to-row spacing, 45 cm plant-to-plant spacing.",
        "irrigation": "Regular drip irrigation at root zone; avoid wetting foliage to prevent fungal blight.",
        "fertilization": "NPK ratio 10-26-26 during planting, top-dress with Calcium Nitrate during fruit set.",
        "common_diseases": ["Early Blight", "Late Blight", "Yellow Leaf Curl Virus", "Bacterial Spot"],
        "common_pests": ["Fruit Borer", "Whiteflies", "Aphids", "Spider Mites"],
        "prevention": "Stake plants for air circulation, use mulching, practice 3-year crop rotation."
    },
    "potato": {
        "crop": "Potato",
        "scientific_name": "Solanum tuberosum",
        "climate": "Cool climate crop. Ideal temperature for tuber growth: 15°C - 20°C.",
        "soil": "Loose, friable, well-drained sandy loam soil. pH: 5.2 - 6.4.",
        "planting": "Plant healthy disease-free seed tubers 5-7 cm deep in ridges.",
        "spacing": "50 cm between rows, 20 cm between tuber seeds.",
        "irrigation": "Irrigate every 8-10 days; stop watering 10 days prior to harvest.",
        "fertilization": "Apply well-rotted FYM (25 t/ha) + NPK 120:60:120 kg/ha.",
        "common_diseases": ["Late Blight", "Early Blight", "Black Scurf", "Common Scab"],
        "common_pests": ["Potato Tuber Moth", "Aphids", "Cutworms"],
        "prevention": "Use certified seed tubers, perform earthing up at 30 days, avoid waterlogging."
    },
    "rice": {
        "crop": "Rice",
        "scientific_name": "Oryza sativa",
        "climate": "Hot and humid tropical climate. Ideal temperature: 22°C - 32°C.",
        "soil": "Clayey loam or heavy clay soils capable of holding water. pH: 5.5 - 7.0.",
        "planting": "Transplant 21-day nursery seedlings into puddled fields.",
        "spacing": "20 cm x 15 cm in puddled soil matrix.",
        "irrigation": "Maintain 2-5 cm standing water layer during tillering and flowering.",
        "fertilization": "Apply Nitrogen in 3 split doses (basal, tillering, panicle initiation).",
        "common_diseases": ["Blast Disease", "Bacterial Leaf Blight", "Sheath Blight"],
        "common_pests": ["Stem Borer", "Brown Planthopper", "Gall Midge"],
        "prevention": "Drain field periodically, apply Neem cake, destroy stubble post-harvest."
    },
    "wheat": {
        "crop": "Wheat",
        "scientific_name": "Triticum aestivum",
        "climate": "Cool winter growing period with warm dry harvesting period. Temp: 10°C - 25°C.",
        "soil": "Well-drained clay loam or loam soil. pH: 6.0 - 7.5.",
        "planting": "Sow seeds using seed drill at 4-5 cm depth during November.",
        "spacing": "22.5 cm between rows.",
        "irrigation": "5-6 irrigations at critical stages (Crown Root Initiation, Flowering, Grain filling).",
        "fertilization": "NPK 120:60:40 kg/ha with Zinc Sulfate application.",
        "common_diseases": ["Yellow Rust", "Brown Rust", "Powdery Mildew", "Loose Smut"],
        "common_pests": ["Aphids", "Termites", "Armyworms"],
        "prevention": "Seed treatment with Carboxin, timely sowing, balanced fertilizer application."
    },
    "cotton": {
        "crop": "Cotton",
        "scientific_name": "Gossypium hirsutum",
        "climate": "Tropical and subtropical climate. Requires minimum 180 frost-free days.",
        "soil": "Deep black cotton soil (Vertisols) or alluvial soil. pH: 6.0 - 8.0.",
        "planting": "Sow seeds in dibbling method at 3-4 cm depth.",
        "spacing": "90 cm x 60 cm for Bt hybrids.",
        "irrigation": "Critical during boll formation stage; avoid waterlogging during early growth.",
        "fertilization": "NPK 120:60:60 kg/ha with Magnesium and Boron foliar sprays.",
        "common_diseases": ["Bacterial Blight", "Alternaria Leaf Spot", "Fusarium Wilt"],
        "common_pests": ["Pink Bollworm", "Whitefly", "Thrips", "Mealybug"],
        "prevention": "Erect yellow sticky traps, practice field sanitation, spray Beauveria bassiana."
    },
    "soybean": {
        "crop": "Soybean",
        "scientific_name": "Glycine max",
        "climate": "Warm and moist climate. Ideal temperature: 20°C - 30°C.",
        "soil": "Well-drained fertile loamy soil rich in organic carbon. pH: 6.5 - 7.5.",
        "planting": "Sow treated seeds with Rhizobium culture at 3-4 cm depth.",
        "spacing": "45 cm row spacing, 5-7 cm plant spacing.",
        "irrigation": "Kharif crop relies on monsoon; give protective irrigation at pod filling if dry.",
        "fertilization": "NPK 20:60:40:20 (N:P:K:S kg/ha). Nitrogen fixed via root nodules.",
        "common_diseases": ["Yellow Mosaic Virus", "Rust", "Charcoal Rot", "Collar Rot"],
        "common_pests": ["Girdle Beetle", "Tobacco Caterpillar", "Semilooper"],
        "prevention": "Inoculate seeds with Bradyrhizobium, use resistant cultivars, spray neem oil."
    },
    "maize": {
        "crop": "Maize (Corn)",
        "scientific_name": "Zea mays",
        "climate": "Adaptable to warm temperate & tropical conditions. Temp: 18°C - 32°C.",
        "soil": "Deep, fertile, well-drained loamy soil. pH: 5.8 - 7.2.",
        "planting": "Sow seeds on ridges or flat beds at 4-5 cm depth.",
        "spacing": "60 cm x 20 cm.",
        "irrigation": "Irrigate at knee-high stage, tasseling, and cob formation.",
        "fertilization": "NPK 120:60:50 kg/ha. Apply Potash during basal dressing.",
        "common_diseases": ["Turcicum Leaf Blight", "Maydis Leaf Blight", "Downy Mildew"],
        "common_pests": ["Fall Armyworm", "Stem Borer", "Corn Earworm"],
        "prevention": "Apply Metarhizium anisopliae, use pheromone traps for Fall Armyworm control."
    },
    "chilli": {
        "crop": "Chilli",
        "scientific_name": "Capsicum annuum",
        "climate": "Warm humid climate. Ideal temperature: 20°C - 30°C.",
        "soil": "Well-drained sandy loam or clay loam soil. pH: 6.0 - 7.0.",
        "planting": "Transplant 35-40 day nursery seedlings.",
        "spacing": "60 cm x 45 cm.",
        "irrigation": "Light frequent drip irrigation; stop irrigation during fruit ripening.",
        "fertilization": "NPK 100:50:50 kg/ha with Micronutrient foliar sprays.",
        "common_diseases": ["Anthracnose / Fruit Rot", "Powdery Mildew", "Chilli Leaf Curl Virus"],
        "common_pests": ["Thrips", "Yellow Mites", "Aphids"],
        "prevention": "Use blue sticky traps for thrips, intercrop with marigold, spray Trichoderma."
    },
    "onion": {
        "crop": "Onion",
        "scientific_name": "Allium cepa",
        "climate": "Mild climate without extreme heat or cold. Temp: 13°C - 24°C.",
        "soil": "Friable, well-drained loamy soil rich in humus. pH: 6.0 - 7.2.",
        "planting": "Transplant 6-7 week old nursery seedlings or sow bulbs.",
        "spacing": "15 cm x 10 cm on raised beds.",
        "irrigation": "Frequent light irrigations; cease watering 15 days before harvesting.",
        "fertilization": "NPK 100:50:50 + 30 kg Sulfur per hectare.",
        "common_diseases": ["Purple Blotch", "Stemphylium Leaf Blight", "Downy Mildew"],
        "common_pests": ["Onion Thrips", "Maggots"],
        "prevention": "Maintain proper drainage, apply Mancozeb preventive spray during overcast weather."
    },
    "sugarcane": {
        "crop": "Sugarcane",
        "scientific_name": "Saccharum officinarum",
        "climate": "Hot sunny tropical climate with high rainfall. Temp: 26°C - 33°C.",
        "soil": "Deep well-drained loamy soil rich in organic matter. pH: 6.5 - 7.5.",
        "planting": "Plant 3-budded setts in furrows covered with 5 cm soil.",
        "spacing": "90 cm to 120 cm row-to-row distance.",
        "irrigation": "Irrigate every 10-12 days in summer, 20 days in winter.",
        "fertilization": "NPK 250:115:115 kg/ha applied in split doses during earthing up.",
        "common_diseases": ["Red Rot", "Smut", "Wilt", "Grassy Shoot Disease"],
        "common_pests": ["Early Shoot Borer", "Top Borer", "Pyrilla"],
        "prevention": "Sett treatment with Carbendazim, introduce Trichogramma parasitoids."
    }
}

def get_crop_guide(crop_name: str) -> Dict[str, Any]:
    key = crop_name.lower().strip()
    for k, v in CROP_KNOWLEDGE_BASE.items():
        if k in key or key in k:
            return v
    
    # Return default structured crop guide fallback
    return {
        "crop": crop_name.capitalize(),
        "scientific_name": f"{crop_name.capitalize()} (Plantae sp.)",
        "climate": "Requires moderate sunny climate and ambient temperature between 18°C and 28°C.",
        "soil": "Well-drained loamy soil with neutral pH (6.0 - 7.0).",
        "planting": "Plant quality certified seeds or healthy nursery seedlings.",
        "spacing": "Standard recommended row spacing of 45-60 cm.",
        "irrigation": "Maintain soil moisture at root zone without waterlogging.",
        "fertilization": "Balanced NPK application with organic compost mulching.",
        "common_diseases": ["Fungal Leaf Spot", "Bacterial Blight"],
        "common_pests": ["Aphids", "Caterpillars"],
        "prevention": "Practice field sanitation, crop rotation, and periodic leaf inspection."
    }

def list_all_crops() -> List[Dict[str, str]]:
    return [{"code": k, "name": v["crop"], "scientific_name": v["scientific_name"]} for k, v in CROP_KNOWLEDGE_BASE.items()]
