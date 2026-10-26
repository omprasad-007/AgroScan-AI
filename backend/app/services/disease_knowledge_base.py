from typing import Dict, Any, List

CROP_CULTIVATION_KB: Dict[str, Dict[str, str]] = {
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
    "Mango": {
        "common_name": "Mango",
        "scientific_name": "Mangifera indica",
        "family": "Anacardiaceae",
        "growth_cycle": "Perennial Fruit Tree (Bearing in 3-5 years, productive for 40+ years)",
        "soil": "Deep, well-drained rich alluvial or red loamy soil (pH 5.5 - 7.5). Avoid waterlogged soil.",
        "sunlight": "Full direct tropical sunshine (8+ hours daily).",
        "sowing": "Plant grafted saplings (Veneer/Epicotyl) in 1m x 1m pits during monsoon onset (July-August).",
        "transplanting": "Plant at 10m x 10m traditional spacing, or 5m x 5m High Density Planting (HDP).",
        "irrigation": "Irrigate young trees every 4-6 days. Withhold water for 2-3 months prior to flowering (Nov-Dec) to induce floral flush.",
        "fertilization": "Apply 1000g N, 500g P2O5, 1000g K2O per bearing tree per year in two splits (July-Aug and Feb-March).",
        "harvest_indicators": "Shoulders swell above pedicel, skin changes to olive-green, specific gravity reaches 1.01.",
        "estimated_period": "March to July depending on variety."
    },
    "Sugarcane": {
        "common_name": "Sugarcane",
        "scientific_name": "Saccharum officinarum",
        "family": "Poaceae (Grasses)",
        "growth_cycle": "Perennial Cash Crop (12 - 18 months depending on planting season)",
        "soil": "Deep, well-drained fertile loamy soil rich in organic matter (pH 6.5 - 7.5).",
        "sunlight": "High solar radiation throughout vegetative elongation.",
        "sowing": "Plant 3-budded setts treated with Carbendazim in 20-25 cm deep furrows.",
        "transplanting": "Row-to-row distance 90 cm to 120 cm (or 150 cm wide paired row for drip lines).",
        "irrigation": "Formative phase: every 7-10 days. Withhold irrigation 25 days before harvest to concentrate sucrose.",
        "fertilization": "NPK 250:115:115 kg/ha applied across formative stages with micronutrient foliar spray.",
        "harvest_indicators": "Brix reading exceeds 18-20% on hand refractometer; cane leaves dry out.",
        "estimated_period": "12 months (Suru) or 16-18 months (Adsali)."
    },
    "Cotton": {
        "common_name": "Cotton",
        "scientific_name": "Gossypium hirsutum",
        "family": "Malvaceae (Mallow)",
        "growth_cycle": "Annual Cash Crop (150 - 180 days)",
        "soil": "Deep black cotton soils (Vertisols) with high water retention capacity (pH 6.5 - 8.0).",
        "sunlight": "Abundant bright sunshine; sensitive to early frosts.",
        "sowing": "Sow Bt/hybrid seeds 4-5 cm deep with pre-monsoon shower (May-June).",
        "transplanting": "Spacing 90 cm x 60 cm or 120 cm x 45 cm for high density.",
        "irrigation": "Critical stages: Square formation, flowering, and boll development. Avoid excess moisture during boll opening.",
        "fertilization": "NPK 120:60:60 kg/ha with Boron and Magnesium sulfate sprays.",
        "harvest_indicators": "Bolls burst open fully showing clean, fluffy white cotton lint.",
        "estimated_period": "November to February across 3 - 4 pickings."
    },
    "Rice (Paddy)": {
        "common_name": "Rice (Paddy)",
        "scientific_name": "Oryza sativa",
        "family": "Poaceae (Grasses)",
        "growth_cycle": "Annual Cereal (105 - 145 days)",
        "soil": "Heavy clay loam or silty clay with low permeability (pH 5.5 - 7.0).",
        "sunlight": "Direct warm sunlight with high humidity.",
        "sowing": "Nursery bed sowing in June-July for Kharif season.",
        "transplanting": "Transplant 20-25 day seedlings at 20 cm x 15 cm spacing (2-3 seedlings per hill).",
        "irrigation": "Maintain 2-5 cm standing water layer from tillering to grain filling. Drain field 10 days before harvest.",
        "fertilization": "NPK 100:50:50 kg/ha with Zinc Sulfate (25 kg/ha) basal.",
        "harvest_indicators": "80-85% grains turn golden-yellow and moisture drops to 20%.",
        "estimated_period": "October to December (Kharif)."
    },
    "Wheat": {
        "common_name": "Wheat",
        "scientific_name": "Triticum aestivum",
        "family": "Poaceae (Grasses)",
        "growth_cycle": "Winter Annual (110 - 130 days)",
        "soil": "Fertile, well-drained loam or clay loam soil (pH 6.0 - 7.5).",
        "sunlight": "Cool sunny winter weather with warm dry harvest period.",
        "sowing": "Line sowing behind plough or seed drill in first fortnight of November.",
        "transplanting": "Direct drilling at 20-22.5 cm row spacing.",
        "irrigation": "Crown root initiation (21 DAS), tillering, jointing, flowering, and milk stages.",
        "fertilization": "NPK 120:60:40 kg/ha with split nitrogen application.",
        "harvest_indicators": "Straw and spikes turn golden brown; grain is hard and snaps cleanly under tooth.",
        "estimated_period": "March to April."
    },
    "Soybean": {
        "common_name": "Soybean",
        "scientific_name": "Glycine max",
        "family": "Fabaceae (Legumes)",
        "growth_cycle": "Annual Oilseed/Legume (90 - 105 days)",
        "soil": "Well-drained fertile loam or black clay soil (pH 6.0 - 7.5).",
        "sunlight": "Full direct sunlight throughout growth.",
        "sowing": "Sow at 3-4 cm depth with onset of monsoon (June-July).",
        "transplanting": "Direct line sowing at 45 cm x 5 cm spacing.",
        "irrigation": "Mainly rainfed; supplemental irrigation at flowering and pod development.",
        "fertilization": "NPK 20:60:40 kg/ha with Rhizobium and PSB biofertilizer seed treatment.",
        "harvest_indicators": "Leaves turn yellow and drop off; pods turn golden brown and rattle when shaken.",
        "estimated_period": "September to October."
    },
    "Chilli / Pepper": {
        "common_name": "Chilli / Pepper",
        "scientific_name": "Capsicum annuum",
        "family": "Solanaceae",
        "growth_cycle": "Annual Herbaceous Shrub (120 - 150 days)",
        "soil": "Well-drained light loamy or black soil with organic compost (pH 6.5 - 7.5).",
        "sunlight": "Full sunny exposure (7+ hours daily).",
        "sowing": "Sow in nursery in May-June or Oct-Nov.",
        "transplanting": "Transplant 35-day seedlings at 60 cm x 45 cm spacing.",
        "irrigation": "Irrigate every 6-8 days. Avoid moisture stress during flowering.",
        "fertilization": "NPK 120:60:60 kg/ha with secondary Calcium & Boron sprays.",
        "harvest_indicators": "Green chillies for vegetable; bright crimson red for dry spice harvest.",
        "estimated_period": "Multiple pickings over 2 - 3 months."
    },
    "Grapes": {
        "common_name": "Grapes",
        "scientific_name": "Vitis vinifera",
        "family": "Vitaceae",
        "growth_cycle": "Perennial Deciduous Vine",
        "soil": "Well-drained sandy loam or gravelly soil (pH 6.5 - 7.5).",
        "sunlight": "Warm dry climate with long sunny days.",
        "sowing": "Rootstock propagation (Dogridge / Salt Creek) trained on Bower or Y-trellis.",
        "transplanting": "Plant at 3m x 1.8m or 2.7m x 1.5m spacing.",
        "irrigation": "Drip irrigation; cut water after veraison to concentrate sugar.",
        "fertilization": "Fertigate balanced NPK with Potassium Schoenite during berry development.",
        "harvest_indicators": "Berries soften, attain uniform color, and Brix reaches 18-22°.",
        "estimated_period": "February to April in Peninsular India."
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
        "harvest_indicators": "Husks dry out and turn light tan; kernel milk-line disappears.",
        "estimated_period": "90 - 110 days after sowing."
    },
    "Onion": {
        "common_name": "Onion",
        "scientific_name": "Allium cepa",
        "family": "Amaryllidaceae",
        "growth_cycle": "Biennial grown as Annual (120 - 140 days)",
        "soil": "Friable, light sandy loam or alluvial soil rich in humus (pH 6.0 - 7.0).",
        "sunlight": "Direct bright sunlight; bulb formation requires 10-12 hours of photoperiod.",
        "sowing": "Nursery sowing in Oct-Nov (Rabi) or May-June (Kharif).",
        "transplanting": "Transplant 6-7 week seedlings on flat beds or BBF at 15 cm x 10 cm.",
        "irrigation": "Frequent light irrigations every 7-10 days. Stop water 15 days before harvest.",
        "fertilization": "NPK 100:50:50 kg/ha + 20 kg Sulphur/ha for pungency and storage life.",
        "harvest_indicators": "50% of the plants exhibit neck fall / leaf top drooping.",
        "estimated_period": "March to May (Rabi) or Oct to Dec (Kharif)."
    },
    "Pomegranate": {
        "common_name": "Pomegranate",
        "scientific_name": "Punica granatum",
        "family": "Lythraceae",
        "growth_cycle": "Perennial Shrub / Small Tree",
        "soil": "Deep loamy or alluvial soil with good drainage (pH 6.5 - 7.5).",
        "sunlight": "Semi-arid climate with high summer heat and sunny skies.",
        "sowing": "Air-layered or hardwood cutting saplings planted in 60x60x60cm pits.",
        "transplanting": "Square spacing at 4.5m x 3m or 4m x 3m.",
        "irrigation": "Regulated deficit drip irrigation according to Bahar treatment.",
        "fertilization": "625g N, 250g P2O5, 500g K2O per mature plant annually.",
        "harvest_indicators": "Rind color changes to deep pink/red, fruit produces metallic sound on tapping.",
        "estimated_period": "135 - 150 days after flower set."
    },
    "Banana": {
        "common_name": "Banana",
        "scientific_name": "Musa acuminata",
        "family": "Musaceae",
        "growth_cycle": "Giant Herbaceous Monocot (11 - 13 months)",
        "soil": "Deep, rich, loose loamy soil with high organic matter (pH 6.0 - 7.5).",
        "sunlight": "Warm, humid tropical climate with high sunlight.",
        "sowing": "Tissue culture plantlets or sword suckers (1.5-2.0 kg).",
        "transplanting": "Spacing 1.8m x 1.8m or 1.5m x 1.5m under drip irrigation.",
        "irrigation": "High water requirement (1800-2000 mm); irrigate every 3-4 days.",
        "fertilization": "NPK 200:40:200 g/plant applied in 4 splits during vegetative phase.",
        "harvest_indicators": "Fruit angles disappear and become rounded; dried floral ends shed easily.",
        "estimated_period": "11 - 12 months after planting."
    },
    "Citrus / Lemon": {
        "common_name": "Citrus / Lemon",
        "scientific_name": "Citrus limon",
        "family": "Rutaceae",
        "growth_cycle": "Perennial Small Tree",
        "soil": "Well-drained light loamy soil (pH 6.5 - 7.5).",
        "sunlight": "Subtropical to tropical sunshine.",
        "sowing": "Budded plants on Rangpur lime or rough lemon rootstocks.",
        "transplanting": "Spacing 5m x 5m or 6m x 6m.",
        "irrigation": "Basin or drip irrigation; avoid letting water touch the tree trunk.",
        "fertilization": "Apply 600g N, 200g P2O5, 300g K2O per bearing tree.",
        "harvest_indicators": "Fruits turn light green to yellowish with glossy skin.",
        "estimated_period": "Multiple seasons (Ambiya / Mrig bahar)."
    },
    "General Crop": {
        "common_name": "General Agricultural Crop",
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

DISEASE_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    # TOMATO
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

    # POTATO
    "potato_late_blight": {
        "crop": "Potato",
        "disease_name": "Potato Late Blight",
        "disease_code": "potato_late_blight",
        "scientific_name": "Phytophthora infestans",
        "symptoms": "Large irregularly shaped brown lesions on leaves and stems with white fungal growth on undersides. Tuber rot turns flesh reddish-brown.",
        "organic_treatment": "Apply Bordeaux mixture (1%) or copper oxychloride before wet weather sets in. Hill up soil around potato plants to protect tubers.",
        "chemical_treatment": "Apply Metalaxyl + Mancozeb or Dimethomorph sprays. Rotate active ingredients to avoid resistance.",
        "prevention": "Plant resistant varieties like Kufri Girdhari. Destroy volunteer potato plants and crop residues after harvest.",
        "general_guidance": "Monitor field after fog or rains. Protect tubers during harvesting."
    },
    "potato_early_blight": {
        "crop": "Potato",
        "disease_name": "Potato Early Blight",
        "disease_code": "potato_early_blight",
        "scientific_name": "Alternaria solani",
        "symptoms": "Dark brown circular spots with concentric target-board rings on mature foliage; premature yellowing and foliage death.",
        "organic_treatment": "Foliar spray of Trichoderma viride or copper hydroxide (2g/L).",
        "chemical_treatment": "Spray Mancozeb 75% WP (2.5g/L) or Propiconazole 25% EC (1ml/L).",
        "prevention": "Plant certified seed tubers; practice strict 3-year non-solanaceous crop rotation.",
        "general_guidance": "Provide balanced potassium and nitrogen to maintain leaf vigor."
    },

    # MANGO
    "mango_anthracnose": {
        "crop": "Mango",
        "disease_name": "Mango Anthracnose",
        "disease_code": "mango_anthracnose",
        "scientific_name": "Colletotrichum gloeosporioides",
        "symptoms": "Dark brown to black angular sunken spots on leaves, panicles, and fruits. In wet weather, orange-pink gelatinous spore masses appear.",
        "organic_treatment": "Foliar spray of cold-pressed Neem Oil (5ml/L) with mild soap surfactant. Prune dried twigs and apply Bordeaux paste (10%).",
        "chemical_treatment": "Spray Copper Oxychloride 50% WP (3.0g/L) or Carbendazim 50% WP (1.0g/L) or Azoxystrobin (1ml/L) at 14-day intervals.",
        "prevention": "Prune overlapping branches after harvest to allow sun penetration. Hot water treatment of fruit (48°C for 5 min).",
        "general_guidance": "High humidity (>85%) during panicle flush triggers infection."
    },
    "mango_powdery_mildew": {
        "crop": "Mango",
        "disease_name": "Mango Powdery Mildew",
        "disease_code": "mango_powdery_mildew",
        "scientific_name": "Oidium mangiferae",
        "symptoms": "Superficial white powdery talc-like patches on panicles, blossoms, and tender leaves. Blossoms turn brown and drop.",
        "organic_treatment": "Spray fermented buttermilk (1:10 dilution) or Wettable Sulphur (2g/L) during early morning.",
        "chemical_treatment": "Apply Hexaconazole 5% EC (1.0ml/L) or Difenoconazole 25% EC (0.5ml/L) at panicle emergence.",
        "prevention": "Avoid excess nitrogen fertilizers which produce dense succulent shoots vulnerable to mildew.",
        "general_guidance": "Active during dry cool nights (10-15°C) and warm sunny days (25-30°C)."
    },

    # SUGARCANE
    "sugarcane_red_rot": {
        "crop": "Sugarcane",
        "disease_name": "Sugarcane Red Rot",
        "disease_code": "sugarcane_red_rot",
        "scientific_name": "Colletotrichum falcatum",
        "symptoms": "Third or fourth leaf from top shows yellowing, drying along margins. Stalk pith turns dull red with crosswise white patches and alcoholic odor.",
        "organic_treatment": "Treat seed setts with Trichoderma harzianum (10g/L) before planting. Remove and burn diseased clumps immediately.",
        "chemical_treatment": "Soak seed setts in Carbendazim 50% WP (1g/L) solution for 15 minutes before furrow placement.",
        "prevention": "Plant certified resistant varieties like Co 0238 or Co 86032. Avoid ratoon crops in infested fields.",
        "general_guidance": "Most destructive disease of sugarcane in India. Rogue out infected clumps immediately."
    },
    "sugarcane_smut": {
        "crop": "Sugarcane",
        "disease_name": "Sugarcane Smut",
        "disease_code": "sugarcane_smut",
        "scientific_name": "Sporisorium scitamineum",
        "symptoms": "Emergence of a long, black, whip-like curved structure (spindle) from the central growing shoot, covered by a silver membrane.",
        "organic_treatment": "Bag the smut whip in a plastic cover before cutting to prevent airborne spore dissemination.",
        "chemical_treatment": "Dip seed setts in Propiconazole (1ml/L) or Triadimefon (1g/L).",
        "prevention": "Select disease-free certified nursery setts; rogue out infected clumps before whip bursts.",
        "general_guidance": "Whip produces millions of black teliospores spread rapidly by wind."
    },

    # COTTON
    "cotton_bacterial_blight": {
        "crop": "Cotton",
        "disease_name": "Cotton Bacterial Blight (Blackarm)",
        "disease_code": "cotton_bacterial_blight",
        "scientific_name": "Xanthomonas citri pv. malvacearum",
        "symptoms": "Angular water-soaked leaf spots bordered by leaf veins ('Angular Leaf Spot'). Lesions turn dark brown/black and spread down petioles and stems ('Blackarm').",
        "organic_treatment": "Spray Pseudomonas fluorescens (10g/L) and ensure wide row spacing to maximize airflow.",
        "chemical_treatment": "Foliar spray of Copper Oxychloride (2.5g/L) mixed with Streptomycin sulfate / Tetracycline (100 ppm, 1g/10L).",
        "prevention": "Delint seed with concentrated sulphuric acid (100ml/kg seed). Use resistant hybrids.",
        "general_guidance": "Rain splashes and wind-driven droplets accelerate bacterial transmission."
    },
    "cotton_leaf_curl": {
        "crop": "Cotton",
        "disease_name": "Cotton Leaf Curl Virus (CLCuV)",
        "disease_code": "cotton_leaf_curl",
        "scientific_name": "Begomovirus",
        "symptoms": "Upward or downward cupping of leaves, thickening of veins on underside, and development of enations (leaf-like outgrowths) on veins.",
        "organic_treatment": "Install yellow sticky traps (15/acre). Spray 5% neem seed kernel extract (NSKE) to control whitefly vector.",
        "chemical_treatment": "Spray systemic insecticides like Diafenthiuron 50% WP (1g/L) or Spiromesifen (1ml/L) to control whiteflies.",
        "prevention": "Eradicate weed hosts like Abutilon indicum and Parthenium hysterophorus near field borders.",
        "general_guidance": "Transmitted exclusively by whitefly Bemisia tabaci."
    },

    # RICE
    "rice_blast": {
        "crop": "Rice (Paddy)",
        "disease_name": "Rice Blast",
        "disease_code": "rice_blast",
        "scientific_name": "Magnaporthe oryzae",
        "symptoms": "Spindle-shaped / diamond-shaped lesions with gray-white centers and brown margins on leaf blades. Stems at node or panicle base turn black and snap ('Neck Blast').",
        "organic_treatment": "Spray Pseudomonas fluorescens (5g/L). Avoid excessive split applications of chemical nitrogen.",
        "chemical_treatment": "Spray Tricyclazole 75% WP (0.6g/L) or Isoprothiolane 40% EC (1.5ml/L) at first appearance of spindle spots.",
        "prevention": "Treat seeds with Carbendazim (2g/kg seed). Maintain balanced potassium nutrition.",
        "general_guidance": "Favored by night temperatures around 20°C, high relative humidity (>90%), and prolonged dew."
    },
    "rice_brown_spot": {
        "crop": "Rice (Paddy)",
        "disease_name": "Rice Brown Spot",
        "disease_code": "rice_brown_spot",
        "scientific_name": "Bipolaris oryzae",
        "symptoms": "Numerous small, circular to oval dark brown spots resembling sesame seeds with yellow haloes on leaf blades.",
        "organic_treatment": "Apply balanced micronutrient foliar spray (Zinc and Silicon). Seed treatment with Trichoderma.",
        "chemical_treatment": "Spray Mancozeb 75% WP (2.5g/L) or Edifenphos (1ml/L).",
        "prevention": "Correct soil nutrient deficiency, particularly nitrogen, potassium, and silicon in light soils.",
        "general_guidance": "Often associated with poor soil fertility or nutritional stress."
    },

    # WHEAT
    "wheat_yellow_rust": {
        "crop": "Wheat",
        "disease_name": "Wheat Stripe / Yellow Rust",
        "disease_code": "wheat_yellow_rust",
        "scientific_name": "Puccinia striiformis",
        "symptoms": "Bright yellow, powdery pustules arranged in prominent parallel stripes/lines along leaf veins. Yellow dust rubs off on fingers.",
        "organic_treatment": "Spray sulfur dust or bio-fungicide Bacillus amyloliquefaciens.",
        "chemical_treatment": "Spray Propiconazole 25% EC (1ml/L) or Tebuconazole 25.9% EC (1ml/L) at first sign of stripe rust in field.",
        "prevention": "Sow rust-resistant varieties like DBW 187, DBW 222, HD 3086. Practice timely sowing.",
        "general_guidance": "Spreads rapidly during cool, humid winter mornings in Northern and Northwestern plains."
    },
    "wheat_leaf_blight": {
        "crop": "Wheat",
        "disease_name": "Wheat Leaf Blight",
        "disease_code": "wheat_leaf_blight",
        "scientific_name": "Bipolaris sorokiniana",
        "symptoms": "Oval to oblong brown spots with yellow halos expanding into large necrotic blotches; early drying of flag leaf.",
        "organic_treatment": "Foliar spray of Trichoderma harzianum; seed treatment with bio-agents.",
        "chemical_treatment": "Spray Mancozeb (2g/L) or Azoxystrobin (1ml/L).",
        "prevention": "Ensure certified seed; avoid drought stress during grain filling stage.",
        "general_guidance": "Prevalent in warm, humid regions of eastern and central wheat zones."
    },

    # SOYBEAN
    "soybean_rust": {
        "crop": "Soybean",
        "disease_name": "Soybean Rust",
        "disease_code": "soybean_rust",
        "scientific_name": "Phakopsora pachyrhizi",
        "symptoms": "Tiny brown to reddish-brown raised pustules on the undersides of leaves, causing yellowing and rapid premature defoliation.",
        "organic_treatment": "Apply wettable sulfur (2g/L) or bio-control agent Trichoderma viride.",
        "chemical_treatment": "Apply Hexaconazole 5% EC (1ml/L) or Pyraclostrobin (1ml/L) at first appearance.",
        "prevention": "Plant resistant cultivars; practice proper plant spacing for canopy aeration.",
        "general_guidance": "High humidity and continuous rain during pod-fill stage dramatically accelerate spread."
    },
    "soybean_frogeye_leaf_spot": {
        "crop": "Soybean",
        "disease_name": "Soybean Frogeye Leaf Spot",
        "disease_code": "soybean_frogeye_leaf_spot",
        "scientific_name": "Cercospora sojina",
        "symptoms": "Circular to angular spots with grayish-white centers and distinct reddish-purple to dark brown borders ('frogeye').",
        "organic_treatment": "Foliar spray of copper hydroxide or neem-based formulations.",
        "chemical_treatment": "Spray Azoxystrobin + Difenoconazole or Thiophanate-methyl.",
        "prevention": "Crop rotation with non-legume crops; use certified disease-free seed.",
        "general_guidance": "Warm, humid conditions promote disease cycle."
    },

    # CHILLI
    "chilli_leaf_curl": {
        "crop": "Chilli / Pepper",
        "disease_name": "Chilli Leaf Curl Virus",
        "disease_code": "chilli_leaf_curl",
        "scientific_name": "Begomovirus",
        "symptoms": "Leaves curl upwards and downwards, puckered leaf texture, reduced leaf size, short internodes, and stunted bushy growth.",
        "organic_treatment": "Install yellow and blue sticky traps (20/acre). Spray 5% NSKE or Neem oil (3ml/L) to manage thrips and whiteflies.",
        "chemical_treatment": "Spray Fipronil 5% SC (1.5ml/L) or Acetamiprid 20% SP (0.5g/L) for vector control.",
        "prevention": "Nursery barrier crops (Maize or Sorghum borders); rogue out infected plants.",
        "general_guidance": "Transmitted by thrips and whiteflies. Controlling vectors early is essential."
    },
    "chilli_anthracnose": {
        "crop": "Chilli / Pepper",
        "disease_name": "Chilli Anthracnose / Dieback",
        "disease_code": "chilli_anthracnose",
        "scientific_name": "Colletotrichum capsici",
        "symptoms": "Dieback of twigs from tip downward. Circular sunken black spots with concentric rings on green and ripe chilli pods.",
        "organic_treatment": "Spray copper oxychloride (2.5g/L) before flowering; prune affected top twigs.",
        "chemical_treatment": "Spray Azoxystrobin 23% SC (1ml/L) or Difenoconazole (0.5ml/L) at 10-14 day intervals.",
        "prevention": "Seed treatment with Thiram (2g/kg); avoid overhead sprinkler irrigation.",
        "general_guidance": "Splashing rains spread spores rapidly across pods."
    },

    # GRAPES
    "grape_downy_mildew": {
        "crop": "Grapes",
        "disease_name": "Grape Downy Mildew",
        "disease_code": "grape_downy_mildew",
        "scientific_name": "Plasmopara viticola",
        "symptoms": "Yellowish, oily lesions on upper leaf surface ('oil spots') and dense white downy fungal cotton on lower leaf surface.",
        "organic_treatment": "Spray 1% Bordeaux mixture before monsoon rain; remove infected leaves from vineyard floor.",
        "chemical_treatment": "Apply Dimethomorph 50% WP (1g/L) or Cymoxanil + Mancozeb (2g/L) or Metalaxyl-M.",
        "prevention": "Canopy management to ensure rapid drying after rain; keep lower foliage elevated above soil.",
        "general_guidance": "Requires free water droplets on foliage for spore germination."
    },
    "grape_powdery_mildew": {
        "crop": "Grapes",
        "disease_name": "Grape Powdery Mildew",
        "disease_code": "grape_powdery_mildew",
        "scientific_name": "Erysiphe necator",
        "symptoms": "White to ash-gray powdery coating on leaves, tendrils, and berries. Berries crack open exposing seeds.",
        "organic_treatment": "Apply sulfur dust (25 kg/ha) or wettable sulfur (2g/L) early morning.",
        "chemical_treatment": "Spray Penconazole 10% EC (0.5ml/L) or Kresoxim-methyl 44.3% SC (0.7ml/L).",
        "prevention": "Open canopy pruning to allow direct sunlight penetration.",
        "general_guidance": "Thrives in warm, dry weather with shade and high humidity."
    },

    # CORN
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
    "corn_northern_leaf_blight": {
        "crop": "Corn (Maize)",
        "disease_name": "Corn Northern Leaf Blight",
        "disease_code": "corn_northern_leaf_blight",
        "scientific_name": "Exserohilum turcicum",
        "symptoms": "Long, elliptical grayish-green or tan lesions (cigar-shaped, 3-15 cm long) parallel to leaf margins.",
        "organic_treatment": "Foliar spray of Trichoderma harzianum; incorporate crop residues after harvest.",
        "chemical_treatment": "Spray Mancozeb (2.5g/L) or Azoxystrobin (1ml/L) if lesions appear below the ear leaf prior to silking.",
        "prevention": "Plant resistant hybrids; 2-year crop rotation with non-host crops.",
        "general_guidance": "Moderate temperatures (18-27°C) with heavy morning dew trigger severe blights."
    },

    # ONION
    "onion_purple_blotch": {
        "crop": "Onion",
        "disease_name": "Onion Purple Blotch",
        "disease_code": "onion_purple_blotch",
        "scientific_name": "Alternaria porri",
        "symptoms": "Small water-soaked lesions that turn purple to dark brown with yellowish borders; leaves snap at lesion points.",
        "organic_treatment": "Spray copper oxychloride (2.5g/L) with sticker/spreader agent (sandovit).",
        "chemical_treatment": "Spray Difenoconazole 25% EC (1ml/L) or Mancozeb 75% WP (2.5g/L).",
        "prevention": "Avoid overhead sprinkler irrigation; ensure adequate plant spacing.",
        "general_guidance": "High humidity (>80%) and warm temperatures (25-30°C) favor rapid progression."
    },

    # POMEGRANATE
    "pomegranate_bacterial_blight": {
        "crop": "Pomegranate",
        "disease_name": "Pomegranate Bacterial Blight (Telya)",
        "disease_code": "pomegranate_bacterial_blight",
        "scientific_name": "Xanthomonas axonopodis pv. punicae",
        "symptoms": "Dark brown, water-soaked oily spots with yellow haloes on leaves ('Telya'). Y-shaped or L-shaped cracks on fruit rind.",
        "organic_treatment": "Prune infected twigs 5 cm below infection and apply Bordeaux paste. Spray Pseudomonas fluorescens.",
        "chemical_treatment": "Spray Streptocycline (500 ppm) + Copper Oxychloride (2.5g/L) or 2-Bromo-2-nitropropane-1,3-diol (Bacterinol, 0.5g/L).",
        "prevention": "Plant disease-free tissue culture saplings; strictly sterilize secateurs with formalin.",
        "general_guidance": "Rains and high humidity trigger explosive bacterial development."
    },

    # BANANA
    "banana_sigatoka": {
        "crop": "Banana",
        "disease_name": "Banana Sigatoka Leaf Spot",
        "disease_code": "banana_sigatoka",
        "scientific_name": "Pseudocercospora musae",
        "symptoms": "Small reddish-brown streaks parallel to leaf veins that expand into spindle spots with gray centers and black margins.",
        "organic_treatment": "Deleaf diseased leaves and destroy; spray mineral oil emulsion (1%).",
        "chemical_treatment": "Spray Propiconazole 25% EC (1ml/L) or Carbendazim (1g/L) mixed with mineral oil.",
        "prevention": "Ensure proper drainage; avoid waterlogging; maintain plant spacing.",
        "general_guidance": "Accelerates during wet monsoon seasons."
    },

    # CITRUS
    "citrus_canker": {
        "crop": "Citrus / Lemon",
        "disease_name": "Citrus Canker",
        "disease_code": "citrus_canker",
        "scientific_name": "Xanthomonas citri subsp. citri",
        "symptoms": "Raised, corky, rough brownish blisters with prominent oily water-soaked yellow halos on leaves, twigs, and fruit skin.",
        "organic_treatment": "Prune cankered twigs before monsoon flush; spray Neem oil (5ml/L) to control leaf miner larvae.",
        "chemical_treatment": "Spray Copper Oxychloride (2.5g/L) + Streptocycline (100 ppm, 1g/10L water).",
        "prevention": "Control citrus leaf miner (Phyllocnistis citrella) whose leaf tunnels allow bacterial entry.",
        "general_guidance": "Wind-driven rain spreads bacteria rapidly between trees."
    },

    # UNIVERSAL HEALTHY LEAF
    "healthy_leaf": {
        "crop": "General Crop",
        "disease_name": "Healthy Leaf (No Disease Detected)",
        "disease_code": "healthy_leaf",
        "scientific_name": "N/A",
        "symptoms": "Vibrant green foliage with smooth uniform leaf surface. No lesions, discoloration, wilting, or fungal pustules detected.",
        "organic_treatment": "Maintain regular watering schedule and organic compost application. Continue monitoring weekly.",
        "chemical_treatment": "No chemical treatment required. Avoid unnecessary pesticide application to preserve beneficial insects.",
        "prevention": "Maintain soil health, crop rotation, balanced NPK fertilization, and proper field drainage.",
        "general_guidance": "Crop is healthy and thriving. Keep recording routine observations."
    }
}

ALL_DISEASES = list(DISEASE_KNOWLEDGE_BASE.values())

def get_crop_cultivation_info(crop_name: str) -> dict:
    for key, val in CROP_CULTIVATION_KB.items():
        if key.lower() in crop_name.lower() or crop_name.lower() in key.lower():
            return val
    return CROP_CULTIVATION_KB.get("General Crop", {})

def get_disease_by_code(code: str) -> dict:
    info = DISEASE_KNOWLEDGE_BASE.get(code, DISEASE_KNOWLEDGE_BASE["healthy_leaf"])
    crop_name = info.get("crop", "General Crop")
    cult_info = get_crop_cultivation_info(crop_name)
    
    result: Dict[str, Any] = dict(info)
    result["plant_info"] = {
        "common_name": cult_info.get("common_name", crop_name),
        "scientific_name": info.get("scientific_name") or cult_info.get("scientific_name", "Plantae"),
        "family": cult_info.get("family", "Agronomic Variety"),
        "growth_cycle": cult_info.get("growth_cycle", "Seasonal Annual")
    }
    result["cultivation"] = {
        "soil": cult_info.get("soil", "Well-drained fertile agricultural soil."),
        "sunlight": cult_info.get("sunlight", "Direct sunlight 6 to 8 hours daily."),
        "sowing": cult_info.get("sowing", "Follow regional agricultural planting calendar."),
        "transplanting": cult_info.get("transplanting", "Standard agricultural row spacing."),
        "irrigation": cult_info.get("irrigation", "Irrigate according to soil moisture and crop stage."),
        "fertilization": cult_info.get("fertilization", "Apply balanced NPK according to soil test.")
    }
    result["harvesting"] = {
        "indicators": cult_info.get("harvest_indicators", "Crop attains physiological harvest maturity."),
        "estimated_period": cult_info.get("estimated_period", "90 - 150 days.")
    }
    return result
