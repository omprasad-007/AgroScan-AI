CROP_CULTIVATION_KB = {
    "Tomato": {
        "common_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae (Nightshade)",
        "growth_cycle": "Annual (90 - 120 days from sowing)",
        "soil": "Well-drained sandy loam or clay loam, rich in organic matter (pH 6.0 - 6.8).",
        "sunlight": "Full sun (6 to 8 hours of direct daily sunlight).",
        "sowing": "Sow seeds 0.5 cm deep in nursery beds during Oct-Nov (Rabi) or Jun-Jul (Kharif).",
        "transplanting": "Transplant 25-30 day old healthy seedlings at 60 cm x 45 cm spacing.",
        "irrigation": "Drip irrigation recommended. Water at 5-7 day intervals; maintain uniform soil moisture to prevent blossom end rot.",
        "fertilization": "Apply NPK 100:60:60 kg/ha with basal FYM (15-20 t/ha). Top dress Nitrogen at 30 and 45 days after transplanting.",
        "harvest_indicators": "Fruits turn firm, glossy, and transition from green to pinkish-red.",
        "estimated_period": "70 - 80 days after transplanting; harvest every 3 - 4 days for 6 - 8 weeks."
    },
    "Potato": {
        "common_name": "Potato",
        "scientific_name": "Solanum tuberosum",
        "family": "Solanaceae (Nightshade)",
        "growth_cycle": "Annual Tuber Crop (90 - 110 days)",
        "soil": "Loose, friable, well-drained loamy soil high in organic content (pH 5.2 - 6.4).",
        "sunlight": "Full sun exposure (6 - 8 hours daily).",
        "sowing": "Plant disease-free seed tubers 5-7 cm deep during Oct-Nov (Winter crop in plains).",
        "transplanting": "Direct tuber planting at 60 cm row-to-row and 20 cm plant-to-plant distance.",
        "irrigation": "Light irrigation after planting; repeat every 8-10 days. Stop watering 10 days before harvest.",
        "fertilization": "NPK 120:80:100 kg/ha. Apply full Phosphorous and Potash with half Nitrogen as basal dose.",
        "harvest_indicators": "Vines turn yellow, dry up, and skin of tubers becomes firm and non-peeling.",
        "estimated_period": "90 - 105 days after planting depending on variety."
    },
    "Corn (Maize)": {
        "common_name": "Corn (Maize)",
        "scientific_name": "Zea mays",
        "family": "Poaceae (Grasses)",
        "growth_cycle": "Annual Cereal (85 - 110 days)",
        "soil": "Deep, fertile, well-drained silt loam or clay loam (pH 6.5 - 7.5).",
        "sunlight": "Full direct sunlight (8+ hours daily).",
        "sowing": "Sow seeds 4-5 cm deep during June-July (Kharif) or Oct-Nov (Rabi).",
        "transplanting": "Direct seed dibbling at 60 cm x 20 cm spacing.",
        "irrigation": "Critical irrigation stages: Tasseling, Silking, and Grain filling stage.",
        "fertilization": "NPK 120:60:40 kg/ha. Top dress N at knee-high and silking stages.",
        "harvest_indicators": "Husks dry out and turn light tan; kernel milk-line disappears and black layer forms at cob base.",
        "estimated_period": "90 - 110 days after sowing."
    },
    "General Crop": {
        "common_name": "General Field Crop",
        "scientific_name": "Plantae",
        "family": "Agronomic Variety",
        "growth_cycle": "Seasonal Annual",
        "soil": "Fertile, well-drained agricultural soil rich in organic humus (pH 6.0 - 7.2).",
        "sunlight": "Direct sunlight 6 - 8 hours per day.",
        "sowing": "Follow seasonal cropping calendar (Kharif / Rabi / Zaid).",
        "transplanting": "Standard row spacing depending on field geometry.",
        "irrigation": "Irrigate according to moisture tension and crop growth phase.",
        "fertilization": "Balanced NPK application according to soil test recommendations.",
        "harvest_indicators": "Crop reaches full physiological maturity with characteristic color change.",
        "estimated_period": "Seasonal cycle (90 - 150 days)."
    }
}

DISEASE_KNOWLEDGE_BASE = {
    "tomato_late_blight": {
        "crop": "Tomato",
        "disease_name": "Tomato Late Blight",
        "disease_code": "tomato_late_blight",
        "scientific_name": "Phytophthora infestans",
        "symptoms": "Dark, water-soaked spots on leaf tips and stems, rapidly enlarging into large dark brown/black lesions with pale green halos. White mold visible on leaf undersides in high humidity.",
        "organic_treatment": "Apply copper octanoate (copper soap) or neem oil sprays every 7-10 days. Remove and destroy infected leaves immediately. Improve airflow around plants.",
        "chemical_treatment": "Spray systemic fungicides containing Chlorothalonil, Mancozeb, or Cymoxanil at first sign of infection. Follow product label instructions.",
        "prevention": "Use certified disease-free seeds. Avoid overhead irrigation. Practice 3-year crop rotation with non-solanaceous crops.",
        "general_guidance": "Late Blight spreads extremely fast in warm, moist weather (15-22°C with >80% humidity). Inspect crops daily during monsoon."
    },
    "tomato_early_blight": {
        "crop": "Tomato",
        "disease_name": "Tomato Early Blight",
        "disease_code": "tomato_early_blight",
        "scientific_name": "Alternaria solani",
        "symptoms": "Concentric rings ('target board' pattern) inside dark brown spots on older lower leaves. Surrounding tissue turns yellow and drops prematurely.",
        "organic_treatment": "Spray Bacillus subtilis bio-fungicide or copper hydroxide. Mulch soil around plant base to prevent fungal spores from splashing up.",
        "chemical_treatment": "Apply Difenoconazole, Azoxystrobin, or Mancozeb sprays at 10-14 day intervals.",
        "prevention": "Prune lower branches up to 30 cm above soil. Ensure adequate spacing for sunlight penetration.",
        "general_guidance": "Early Blight thrives in high humidity and high temperatures (24-29°C). Keep foliage dry."
    },
    "tomato_yellow_leaf_curl": {
        "crop": "Tomato",
        "disease_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "disease_code": "tomato_yellow_leaf_curl",
        "scientific_name": "Begomovirus",
        "symptoms": "Severe stunting of young leaves, upward leaf curling, yellowing (chlorosis) between leaf veins, and blossom drop leading to stunted yield.",
        "organic_treatment": "No cure for viral infection. Remove infected plants immediately. Apply yellow sticky traps and neem oil to control whitefly vector (Bemisia tabaci).",
        "chemical_treatment": "Spray systemic insecticides like Imidacloprid or Thiamethoxam to control whiteflies.",
        "prevention": "Plant TYLCV-resistant hybrids. Install 50-mesh insect-proof netting over nursery beds.",
        "general_guidance": "TYLCV is transmitted exclusively by whiteflies. Controlling insect vectors is the primary defense."
    },
    "potato_late_blight": {
        "crop": "Potato",
        "disease_name": "Potato Late Blight",
        "disease_code": "potato_late_blight",
        "scientific_name": "Phytophthora infestans",
        "symptoms": "Large irregulary shaped brown lesions on leaves and stems with white fungal growth on undersides. Tuber rot turns flesh reddish-brown.",
        "organic_treatment": "Apply Bordeaux mixture (1%) or copper oxychloride before wet weather sets in. Hill up soil around potato plants to protect tubers.",
        "chemical_treatment": "Apply Metalaxyl + Mancozeb or Dimethomorph sprays. Rotate active ingredients to avoid resistance.",
        "prevention": "Plant resistant varieties like Kufri Girdhari. Destroy volunteer potato plants and crop residues after harvest.",
        "general_guidance": "Monitor field after fog or rains. Protect tubers during harvesting."
    },
    "corn_common_rust": {
        "crop": "Corn (Maize)",
        "disease_name": "Corn Common Rust",
        "disease_code": "corn_common_rust",
        "scientific_name": "Puccinia sorghi",
        "symptoms": "Small, oval, golden-brown to cinnamon-brown powdery pustules on upper and lower leaf surfaces. Pustules turn black late in the season.",
        "organic_treatment": "Spray sulfur-based organic fungicides. Maintain balanced soil fertility avoiding excessive nitrogen application.",
        "chemical_treatment": "Spray Tebuconazole or Propiconazole at 15-day intervals if rust covers >5% leaf area prior to flowering.",
        "prevention": "Plant rust-resistant maize hybrids. Rotate with legumes like soybean or groundnut.",
        "general_guidance": "Favored by cool temperatures (16-23°C) and high dew duration."
    },
    "healthy_leaf": {
        "crop": "General Crop",
        "disease_name": "Healthy Leaf (No Disease Detected)",
        "disease_code": "healthy_leaf",
        "scientific_name": "N/A",
        "symptoms": "Vibrant green foliage with smooth uniform leaf surface. No lesions, discoloration, wilting, or fungal pustules detected.",
        "organic_treatment": "Maintain regular watering schedule and organic compost application. Continue monitoring weekly.",
        "chemical_treatment": "No chemical treatment required. Avoid unnecessary pesticide application to preserve beneficial insects.",
        "prevention": "Maintain soil health, crop rotation, balanced NPK fertilization, and proper field drainage.",
        "general_guidance": "Crop is healthy. Keep recording routine observations."
    }
}

def get_disease_by_code(code: str) -> dict:
    info = DISEASE_KNOWLEDGE_BASE.get(code, DISEASE_KNOWLEDGE_BASE["healthy_leaf"])
    crop_name = info.get("crop", "General Crop")
    cult_info = CROP_CULTIVATION_KB.get(crop_name, CROP_CULTIVATION_KB["General Crop"])
    
    result = dict(info)
    result["plant_info"] = {
        "common_name": cult_info["common_name"],
        "scientific_name": info.get("scientific_name") or cult_info["scientific_name"],
        "family": cult_info["family"],
        "growth_cycle": cult_info["growth_cycle"]
    }
    result["cultivation"] = {
        "soil": cult_info["soil"],
        "sunlight": cult_info["sunlight"],
        "sowing": cult_info["sowing"],
        "transplanting": cult_info["transplanting"],
        "irrigation": cult_info["irrigation"],
        "fertilization": cult_info["fertilization"]
    }
    result["harvesting"] = {
        "indicators": cult_info["harvest_indicators"],
        "estimated_period": cult_info["estimated_period"]
    }
    return result

