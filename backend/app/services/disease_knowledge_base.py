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
    return DISEASE_KNOWLEDGE_BASE.get(code, DISEASE_KNOWLEDGE_BASE["healthy_leaf"])
