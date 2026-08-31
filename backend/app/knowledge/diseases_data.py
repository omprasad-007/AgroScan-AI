"""
AgroScan AI — Structured Plant Disease & Pathology Knowledge Base
Contains scientific pathology, visual indicators, etiology, environmental triggers,
spread mechanisms, biological/organic remedies, and safe chemical management.
"""

from typing import Dict, Any, List, Optional

DISEASES_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "powdery_mildew": {
        "disease_name": "Powdery Mildew",
        "scientific_name": "Oidium mangiferae / Leveillula taurica / Erysiphe cichoracearum",
        "pathogen_type": "Ascomycete Obligate Biotrophic Fungus",
        "host_plants": ["Mango", "Chilli", "Tomato", "Wheat", "Grapes", "Cucurbits", "Peas", "Okra", "Roses"],
        "symptoms": "Superficial white to grayish-white powdery talc-like fungal patches on upper and lower leaf surfaces, tender shoots, panicles, blossoms, and young fruits. Infected leaves curl upward, become distorted, turn chlorotic, and drop prematurely. Infected blossoms turn brown, dry up, and fall, causing near-total fruit set failure.",
        "visual_symptoms": [
            "White powdery coating resembling flour dusting on floral panicles and young leaves",
            "Inflorescences turn purplish-brown and dry out without setting fruit",
            "Young developing fruits develop corky russeted surface patches and drop off"
        ],
        "causes": "Airborne fungal conidia that germinate under dry surface conditions with high ambient relative humidity. Overwinters as dormant mycelium in infected vegetative buds or as cleistothecia in plant debris.",
        "favorable_conditions": "Cool dry nights (10°C - 15°C) followed by warm days (25°C - 30°C) with morning relative humidity between 65% and 85%. Unlike most fungal pathogens, it does NOT require free water droplets on leaves to germinate.",
        "spread_conditions": "Conidia are dry and powdery, carried easily by gentle wind gusts and air currents across orchards and farm plots.",
        "prevention": "Prune dense tree canopies and overlapping branches after harvest to allow direct sunlight penetration and air movement. Avoid excessive nitrogen fertilizers which promote dense succulent vegetative growth vulnerable to spore infection.",
        "cultural_control": "Maintain clean orchard floor; collect and burn fallen infected inflorescences and leaves. In polyhouses/greenhouses, ventilate during morning hours to reduce relative humidity.",
        "biological_control": "Apply cold-pressed Neem Oil (1500–3000 ppm) at 3-5 ml/L water with a mild surfactant at panicle emergence. Spray bio-fungicides like Bacillus subtilis (5g/L) or Ampelomyces quisqualis (hyper-parasite of powdery mildew). Spray fermented sour buttermilk (1:10 dilution in water) which contains lactic acid that disrupts fungal mycelium.",
        "chemical_management": "For active or severe infections: Apply Wettable Sulphur 80% WP (2.0 to 2.5 g/L) or systemic triazoles such as Hexaconazole 5% EC (1.0 ml/L), Difenoconazole 25% EC (0.5 to 1.0 ml/L), or Dinocap 48% EC (1.0 ml/L). Apply 2-3 sprays starting from panicle emergence to fruit set stage. Note: Avoid spraying sulfur when ambient temperatures exceed 32°C to prevent sulfur leaf burn.",
        "safety_notes": "Wear protective mask and gloves while spraying. Observe standard Pre-Harvest Interval (PHI) of 14-21 days before picking edible produce. Chemical dosages must follow local agricultural university recommendations and approved product label instructions.",
        "when_to_seek_expert_help": "If white powdery growth covers more than 25% of flowering panicles during initial bloom, consult local Krishi Vigyan Kendra (KVK) or district agricultural extension officer immediately."
    },
    "anthracnose": {
        "disease_name": "Anthracnose / Fruit Rot / Dieback",
        "scientific_name": "Colletotrichum gloeosporioides / Colletotrichum capsici",
        "pathogen_type": "Ascomycete Necrotrophic Fungus",
        "host_plants": ["Mango", "Chilli", "Tomato", "Pomegranate", "Papaya", "Banana", "Grapes", "Beans", "Cotton"],
        "symptoms": "Dark brown to black circular to angular sunken necrotic spots on leaves, blossoms, and fruits. On leaves, spots expand and coalesce, causing leaf blight and shot-hole appearance. On developing and ripe fruits, prominent sunken circular dark lesions appear with concentric rings of salmon-pink to orange gelatinous spore masses in humid weather. Twigs exhibit dieback from top downwards.",
        "visual_symptoms": [
            "Sunken dark brown circular 'bullseye' spots with salmon-pink spore tendrils in wet weather",
            "Blossom blight with blackening and drop of flower panicles",
            "Tear-stain necrotic streaks on fruit skin from water dripping off infected twigs"
        ],
        "causes": "Colletotrichum fungal spores surviving in dead twigs, mummified fruits on trees, and crop residue. Dispersed by rain splashes and overhead sprinkler water.",
        "favorable_conditions": "Warm, humid, rainy weather with temperatures between 24°C and 32°C and relative humidity above 85-90%. Extended leaf wetness (longer than 10-12 hours) triggers massive spore germination.",
        "spread_conditions": "Splashing raindrops, overhead irrigation, infected pruning shears, and wind-driven rain.",
        "prevention": "Prune all dead, dried, and diseased twigs (dieback shoots) 5-10 cm below the infection zone after harvest; paint cut ends with Bordeaux paste. Clear dropped infected fruits from the orchard floor.",
        "cultural_control": "Avoid overhead sprinkler irrigation; transition to root-zone drip irrigation. Ensure proper plant spacing and trellis training to accelerate canopy drying after rains.",
        "biological_control": "Foliar spray of Trichoderma viride or Pseudomonas fluorescens (5-10 g/L). Spray cold-pressed Neem Oil (5 ml/L) mixed with Pongamia (Karanja) oil.",
        "chemical_management": "Apply protective contact fungicides before monsoon: Copper Oxychloride 50% WP (2.5 to 3.0 g/L) or Bordeaux Mixture (1%). For active systemic control: Spray Carbendazim 50% WP (1.0 g/L), Azoxystrobin 23% SC (1.0 ml/L), or Propiconazole 25% EC (1.0 ml/L) at 10-14 day intervals.",
        "safety_notes": "Maintain Pre-Harvest Interval (PHI) of 7-14 days. Do not consume heavily bruised fruits. Post-harvest hot water treatment of fruits at 48°C for 5 minutes controls latent fruit infections without chemical residue.",
        "when_to_seek_expert_help": "When fruit rot lesions appear on more than 15% of developing fruits or when dieback progresses rapidly down main scaffold limbs."
    },
    "early_blight": {
        "disease_name": "Early Blight",
        "scientific_name": "Alternaria solani",
        "pathogen_type": "Deuteromycete Necrotrophic Fungus",
        "host_plants": ["Tomato", "Potato", "Eggplant (Brinjal)", "Chilli", "Solanaceous weeds"],
        "symptoms": "Characteristic dark brown to black circular or angular spots with distinct concentric rings creating a 'target board' or 'bullseye' pattern on older lower leaves first. Surrounding leaf tissue turns chlorotic yellow, leading to premature leaf defoliation from bottom upward. On stems, dark sunken cankers form at soil level (collar rot). On fruits, sunken leathery dark spots form near the stem attachment.",
        "visual_symptoms": [
            "Concentric target-board rings within brown lesions on lower mature foliage",
            "Yellow halo surrounding brown spots with rapid premature leaf drop",
            "Dark leathery sunken lesions at the fruit stem calyx end"
        ],
        "causes": "Alternaria solani survives in infected crop debris, volunteer solanaceous plants, and weed hosts. Conidia are dispersed by wind and splashing water.",
        "favorable_conditions": "Alternating wet and dry cycles with warm temperatures (24°C to 29°C) and heavy dew or rain. Nutrient-stressed plants with low nitrogen or heavy fruit load are highly susceptible.",
        "spread_conditions": "Rain-splash from soil to lower leaves, windblown spores, and contaminated agricultural tools.",
        "prevention": "Stake plants off the ground and prune lower suckers up to 30 cm above soil to prevent soil-splash inoculum. Use silver-black reflective plastic mulch. Practice 3-year crop rotation with non-solanaceous crops.",
        "cultural_control": "Irrigate strictly via drip lines early in the morning so foliage remains dry. Remove and bury lower infected leaves as soon as first spots appear.",
        "biological_control": "Foliar spray of Bacillus subtilis (5g/L) or Trichoderma harzianum (5g/L). Spray Neem seed kernel extract (NSKE 5%) or 3000 ppm Neem oil (4 ml/L).",
        "chemical_management": "Apply preventive contact fungicides: Mancozeb 75% WP (2.0 to 2.5 g/L) or Chlorothalonil 75% WP (2.0 g/L). For systemic intervention: Spray Difenoconazole 25% EC (0.5 to 1.0 ml/L), Azoxystrobin 23% SC (1.0 ml/L), or Pyraclostrobin 20% WG (1.0 g/L).",
        "safety_notes": "Observe product label for exact Pre-Harvest Intervals (typically 3-7 days for tomato). Wear gloves and eye protection.",
        "when_to_seek_expert_help": "If target-board spots progress above mid-canopy during early flowering stage."
    },
    "late_blight": {
        "disease_name": "Late Blight",
        "scientific_name": "Phytophthora infestans",
        "pathogen_type": "Oomycete Pathogen (Water Mold)",
        "host_plants": ["Potato", "Tomato", "Eggplant"],
        "symptoms": "Extremely aggressive, rapid destructive blight. Begins as irregular water-soaked pale green or pale brown lesions on leaf tips and margins, rapidly expanding into large dark brown or purplish-black necrotic blotches. In moist humid conditions, a delicate white downy cottony fungal growth appears on the underside of leaves along the lesion margins. Stems develop dark greasy water-soaked lesions leading to total collapse of the canopy within days.",
        "visual_symptoms": [
            "Water-soaked dark greasy leaf margins with translucent borders",
            "White frosty fungal down on leaf undersides in high morning humidity",
            "Tubers exhibit dry granular brown-reddish flesh rot extending 5-15 mm below skin"
        ],
        "causes": "Phytophthora infestans oospores and sporangia surviving in infected seed tubers, volunteer potato plants, and cull piles.",
        "favorable_conditions": "Cool, moist, overcast weather with temperatures between 15°C and 22°C, relative humidity >85-90%, and continuous leaf wetness or fog for 8+ hours.",
        "spread_conditions": "Biflagellate zoospores swim in free water films on leaves and are carried over miles by cool humid wind gusts.",
        "prevention": "Plant only certified disease-free seed tubers. Destroy cull piles and volunteer potatoes before season. Perform high earthing-up (hilling) in potato to create a 10-15 cm soil barrier over tubers preventing sporangia from washing down into tubers.",
        "cultural_control": "Avoid overhead sprinkler irrigation. Ensure wide row spacing for maximum canopy aeration. Dehaulm (cut and destroy potato vines) 10-12 days before harvest.",
        "biological_control": "Preventive application of Trichoderma viride root drench (10g/L) and copper octanoate soap bio-fungicide. Bio-control is effective only before outbreak initiation.",
        "chemical_management": "Preventive / Protective: Mancozeb 75% WP (2.5 g/L), Copper Oxychloride 50% WP (2.5 g/L), or Propineb 70% WP (2.0 g/L). Curative / Systemic (apply immediately upon first local disease forecast): Cymoxanil 8% + Mancozeb 64% WP (2.5 g/L), Metalaxyl 8% + Mancozeb 64% WP (2.0 g/L), Dimethomorph 50% WP (1.0 g/L), or Fenamidone 10% + Mancozeb 50% WG (2.0 g/L).",
        "safety_notes": "Highly destructive epidemic pathogen. Chemical applications must be applied before complete canopy collapse. Strictly adhere to PHI guidelines.",
        "when_to_seek_expert_help": "Late blight is a community-level emergency. Immediately notify local agricultural extension officers upon confirming white downy mold on water-soaked lesions."
    },
    "rice_blast": {
        "disease_name": "Rice Blast / Leaf & Neck Blast",
        "scientific_name": "Magnaporthe oryzae (Pyricularia oryzae)",
        "pathogen_type": "Ascomycete Filamentous Fungus",
        "host_plants": ["Rice (Paddy)", "Finger Millet (Ragi)", "Wheat", "Barley"],
        "symptoms": "Leaf Blast: Characteristic eye-shaped or spindle-shaped lesions with grayish-white centers and dark brown or reddish-brown borders on leaf blades. Lesions enlarge, coalesce, and cause leaf withering. Collar Blast: Brown necrotic rot at the leaf collar. Node Blast: Blackened rotting nodes that easily snap. Neck Blast: Blackish rot at the base of the panicle neck; grain filling ceases, producing totally empty 'white heads' (panicle sterility).",
        "visual_symptoms": [
            "Spindle-shaped elliptical lesions with pointed ends, gray center, and brown margin",
            "Blackened panicle neck with completely choked sterile empty white grains",
            "Rotting nodes that break under light wind"
        ],
        "causes": "Magnaporthe oryzae spores surviving on crop stubble, seeds, and collateral grass hosts. Airborne conidia infect young epidermal cells via appressoria.",
        "favorable_conditions": "Temperatures between 20°C and 26°C with relative humidity >90%, nighttime dew for >10 hours, cloudy skies, and excessive nitrogen fertilization.",
        "spread_conditions": "Airborne conidia released in night hours and splashing dew.",
        "prevention": "Treat seed with Tricyclazole 75% WP (2g/kg) or Pseudomonas fluorescens (10g/kg). Avoid excessive urea top-dressing (split nitrogen into 3-4 doses). Avoid continuous water stress during tillering.",
        "cultural_control": "Burn or compost infected rice stubble. Maintain uniform 2-3 cm standing water layer in fields. Use resistant cultivars (e.g. Swarna, IR64-Blast resistant lines).",
        "biological_control": "Foliar spray of Pseudomonas fluorescens (5-10 g/L) at tillering and panicle emergence stages.",
        "chemical_management": "Spray Tricyclazole 75% WP (0.6 g/L), Isoprothiolane 40% EC (1.5 ml/L), Kasugamycin 3% SL (1.5 to 2.0 ml/L), or Azoxystrobin 18.2% + Difenoconazole 11.4% SC (1.0 ml/L) at boot leaf stage and 10% flowering stage for neck blast protection.",
        "safety_notes": "Apply sprays during early morning before midday heat. Observe standard grain PHI.",
        "when_to_seek_expert_help": "When spindle lesions cover >5% of boot leaf area or when neck blast symptoms begin at panicle emergence."
    },
    "red_rot": {
        "disease_name": "Red Rot of Sugarcane",
        "scientific_name": "Colletotrichum falcatum",
        "pathogen_type": "Fungal Vascular & Parenchymatous Pathogen",
        "host_plants": ["Sugarcane", "Sorghum"],
        "symptoms": "Known as the 'Cancer of Sugarcane'. The third or fourth leaf from the top turns yellow, withers, and dries along the margins. The entire crown droops and withers. When the infected stalk is split open longitudinally, the internal pith tissue shows prominent dull red discoloration interrupted by distinctive white cross-bands (transverse white spots) and emits an acidic fermented alcoholic/acetic odor.",
        "visual_symptoms": [
            "Internal longitudinal red pith discoloration with characteristic transverse white patches",
            "Sour alcoholic/fermented odor from split cane stalks",
            "Midrib lesions showing dark red elongated streaks with black centers on leaf blades"
        ],
        "causes": "Colletotrichum falcatum mycelium and setts infected from previous season. Enters via root primordia, borer tunnels, or node cracks.",
        "favorable_conditions": "High temperature (28°C - 35°C), high humidity, ill-drained waterlogged heavy soils, and continuous monocropping of susceptible varieties.",
        "spread_conditions": "Infected seed setts, irrigation/flood water running between cane rows, and stalk borer wounds.",
        "prevention": "Strictly plant certified disease-free setts from heat-treated nurseries. Hot water treatment (HWT) of setts at 50°C for 2 hours or moist hot air treatment (MHAT) at 54°C for 2.5 hours. Avoid taking ratoon crops in red-rot affected plots.",
        "cultural_control": "Uproot and burn entire diseased cane clumps along with underground root system immediately. Deep summer plowing. Practice 2-3 year crop rotation with paddy, green manure, or pulses.",
        "biological_control": "Dip setts in Trichoderma viride or Trichoderma harzianum suspension (10g/L) for 30 minutes before planting.",
        "chemical_management": "Sett dipping in Carbendazim 50% WP (1.0 g/L) or Thiophanate Methyl 70% WP (1.0 g/L) for 15 minutes before planting. Note: Chemical foliar sprays cannot cure internal vascular red rot once established in standing cane.",
        "safety_notes": "There is no chemical cure for internal red rot in standing stalks; prevention via sett sanitation and resistant varieties (e.g. Co 86032, Co 0238 in tolerant zones) is mandatory.",
        "when_to_seek_expert_help": "Report red rot outbreaks immediately to the sugar mill agronomy division or regional cane research station."
    },
    "sugarcane_smut": {
        "disease_name": "Sugarcane Smut",
        "scientific_name": "Sporisorium scitamineum (Ustilago scitaminea)",
        "pathogen_type": "Basidiomycete Smut Fungus",
        "host_plants": ["Sugarcane"],
        "symptoms": "Production of a prominent, unbranched, curved, whip-like black dusty structure (10 cm to over 1 meter long) arising from the apical growing shoot of the cane stalk. The whip is initially covered with a silvery-white thin peridium membrane which ruptures to expose millions of powdery black teliospores. Infected plants exhibit thin spindly stalks with small narrow leaves.",
        "visual_symptoms": [
            "Long whip-like black dusty structure emerging from the terminal shoot of the cane",
            "Silvery membrane rupturing to release dense black powdery soot spores",
            "Stunted spindly tillers with reduced inter-nodal length"
        ],
        "causes": "Sporisorium scitamineum teliospores carried by wind and infected seed setts.",
        "favorable_conditions": "Hot, dry weather (25°C - 35°C) followed by humid flushes which trigger teliospore germination on young axillary buds.",
        "spread_conditions": "Wind-borne teliospores entering lateral buds of healthy cane stalks; secondary spread through diseased setts.",
        "prevention": "Use smut-resistant cane varieties. Treat setts with hot water (50°C for 2 hours) or Triadimefon fungicide. Rogue out smut whips carefully by covering them with a wet plastic bag before cutting to prevent spore dispersal.",
        "cultural_control": "Inspect fields weekly. Never allow smut whips to shed spores in the field. Destroy rogued whips in fire away from the farm.",
        "biological_control": "Sett treatment with bio-agents (Trichoderma viride 10g/L + Pseudomonas fluorescens 10g/L).",
        "chemical_management": "Sett dipping before planting in Carbendazim 50% WP (1.0 g/L) or Triadimefon 25% WP (1.0 g/L) for 15 minutes.",
        "safety_notes": "Smut teliospores irritate respiratory tract; wear dust masks when roguing smutted canes.",
        "when_to_seek_expert_help": "When smut incidence exceeds 5% of cane stools across a plot."
    },
    "purple_blotch": {
        "disease_name": "Purple Blotch of Onion & Garlic",
        "scientific_name": "Alternaria porri",
        "pathogen_type": "Deuteromycete Fungus",
        "host_plants": ["Onion", "Garlic", "Shallots", "Leeks"],
        "symptoms": "Starts as small, water-soaked, sunken oval lesions on leaf blades and seed stalks that rapidly enlarge, turning brown with a distinctive purple or dark violet center surrounded by yellow chlorotic margins. Leaves turn yellow, collapse, and break over at the lesion point. Seed stalks break prematurely, causing severe seed crop loss.",
        "visual_symptoms": [
            "Sunken elliptical lesions with characteristic deep purple to violet center",
            "Concentric rings with dark brown sporulation within the purple lesion",
            "Breakage and lodging of leaf blades and seed stalks at the point of infection"
        ],
        "causes": "Alternaria porri mycelium surviving in onion crop residues, volunteer bulbs, and infected seed.",
        "favorable_conditions": "Warm humid weather (24°C - 30°C) with relative humidity >80-90% and continuous dew or overcast skies.",
        "spread_conditions": "Windblown airborne conidia and rain-splashes.",
        "prevention": "Ensure excellent soil drainage. Treat seed/bulbs with Thiram (2g/kg). Follow 3-year crop rotation with non-allium crops.",
        "cultural_control": "Maintain optimum plant spacing (15 cm x 10 cm). Avoid excessive nitrogen top-dressing. Keep fields free of allium weed hosts.",
        "biological_control": "Foliar spray of Trichoderma harzianum (5g/L) or Pseudomonas fluorescens (5g/L). Spray cold-pressed Neem Oil (4-5 ml/L).",
        "chemical_management": "Apply Mancozeb 75% WP (2.5 g/L) with sticking agent (Triton/liquid soap 1ml/L) preventively. For active disease: Spray Difenoconazole 25% EC (1.0 ml/L), Tebuconazole 25.9% EC (1.0 ml/L), or Azoxystrobin 23% SC (1.0 ml/L) at 10-12 day intervals.",
        "safety_notes": "Adding a wetting/sticking agent is essential because onion leaves have a waxy cuticle that repels water droplets.",
        "when_to_seek_expert_help": "When purple blotch lesions appear on seed stalks before flowering or on >10% of bulb crop canopy."
    },
    "leaf_curl_virus": {
        "disease_name": "Chilli / Tomato Leaf Curl Virus",
        "scientific_name": "Begomovirus (Geminiviridae)",
        "pathogen_type": "Plant Viral Pathogen (Circular ssDNA)",
        "host_plants": ["Chilli", "Tomato", "Papaya", "Tobacco", "Cotton", "Zinnia"],
        "symptoms": "Severe upward and downward curling and rolling of leaves, thickening of veins (vein clearing), puckering of inter-veinal lamina, blistering, extreme reduction in leaf size, and severe stunting of internodes resulting in a bushy, stunted plant. Flower buds drop off and plants produce few or deformed, small, leathery fruits.",
        "visual_symptoms": [
            "Upward boat-shaped curling and puckering of leaf lamina",
            "Extreme plant stunting with rosette, bushy appearance",
            "Thickened, brittle, dark green or chlorotic veinal network"
        ],
        "causes": "Begomovirus transmitted exclusively by the insect vector Whitefly (Bemisia tabaci). Not transmitted mechanically through sap or seed.",
        "favorable_conditions": "Dry, warm weather (28°C - 36°C) which promotes explosive whitefly population reproduction.",
        "spread_conditions": "Persistent transmission by adult female whiteflies moving between weed hosts and crops.",
        "prevention": "Install yellow sticky traps (20-25 traps/ha) at canopy height to capture whiteflies. Plant 2-3 border rows of tall barrier crops like Maize, Sorghum, or Pearl Millet around the plot.",
        "cultural_control": "Uproot and destroy virus-infected plants during the first 45 days after transplanting. Protect nursery beds with 50-mesh nylon insect nets.",
        "biological_control": "Spray cold-pressed Neem Oil 3000 ppm (5 ml/L) or Pongamia oil (5 ml/L) to deter whitefly feeding. Spray Beauveria bassiana or Verticillium lecanii (5g/L) bio-insecticide to parasitise whitefly nymphs.",
        "chemical_management": "Direct vector control: Spray systemic insecticides like Diafenthiuron 50% WP (1.0 g/L), Spiromesifen 22.9% SC (1.0 ml/L), Acetamiprid 20% SP (0.3 g/L), or Imidacloprid 17.8% SL (0.5 ml/L). Note: Antibiotics or fungicides do NOT cure viral infections; control is achieved solely by managing the insect vector.",
        "safety_notes": "Rotate chemical insecticides across different IRAC modes of action to prevent whitefly pesticide resistance.",
        "when_to_seek_expert_help": "If whitefly vector density exceeds 5-10 adults per leaf and leaf curl spreads across >10% of field."
    },
    "bacterial_blight_cotton": {
        "disease_name": "Bacterial Blight / Angular Leaf Spot / Black Arm",
        "scientific_name": "Xanthomonas citri pv. malvacearum",
        "pathogen_type": "Gram-negative Rod Bacterium",
        "host_plants": ["Cotton"],
        "symptoms": "Four distinct stages: 1) Seedling blight (water-soaked circular spots on cotyledons), 2) Angular leaf spot (small dark brown angular water-soaked spots bounded by leaf veins), 3) Black arm (dark elongated sunken black cankers on branches causing snapping and death of fruiting limbs), 4) Boll rot (sunken water-soaked brown-black spots on bolls causing stained internal lint).",
        "visual_symptoms": [
            "Angular water-soaked spots confined by leaf veinlets on underside of leaves",
            "Black elongated lesions on stems and petiole branches (Black Arm)",
            "Sunken dark lesions on green bolls staining internal fiber"
        ],
        "causes": "Xanthomonas bacterium surviving on seed fuzz, crop residue, and volunteer cotton plants.",
        "favorable_conditions": "Warm humid weather (28°C - 33°C) with relative humidity >85%, heavy monsoon rain showers, and wind-driven rain.",
        "spread_conditions": "Splashing rain droplets, irrigation water, wind-driven storms, and infected delinted seed fuzz.",
        "prevention": "Acid delinting of cotton seed with concentrated sulfuric acid (100ml/kg seed) followed by seed treatment with Streptocycline (100 ppm) + Copper Oxychloride (2g/kg).",
        "cultural_control": "Destroy cotton crop residues after final harvest. Maintain clean cultivation and weed-free borders.",
        "biological_control": "Foliar spray of Pseudomonas fluorescens (10g/L) or Bacillus subtilis (5g/L).",
        "chemical_management": "Spray Copper Oxychloride 50% WP (2.5 g/L) combined with Streptocycline / Plantomycin (0.1 to 0.2 g/L or 100-200 ppm) at 12-15 day intervals.",
        "safety_notes": "Use agricultural bactericides under prescribed safety doses. Do not exceed Streptocycline concentration to avoid phytotoxicity.",
        "when_to_seek_expert_help": "When black arm lesions appear on main stems during squaring/boll formation."
    }
}

def get_disease_data(disease_name: str) -> Optional[Dict[str, Any]]:
    """Lookup disease pathology profile by name or keyword with fuzzy matching."""
    if not disease_name:
        return None
        
    clean = disease_name.lower().strip()
    
    # Direct or substring match
    for key, data in DISEASES_KNOWLEDGE_BASE.items():
        if key in clean or clean in key:
            return data
        if data["disease_name"].lower() in clean or clean in data["disease_name"].lower():
            return data
        if data["scientific_name"].lower() in clean:
            return data
            
    # Keyword matches
    keywords_map = {
        "powdery": "powdery_mildew",
        "mildew": "powdery_mildew",
        "anthracnose": "anthracnose",
        "fruit rot": "anthracnose",
        "dieback": "anthracnose",
        "early blight": "early_blight",
        "target spot": "early_blight",
        "late blight": "late_blight",
        "phytophthora": "late_blight",
        "blast": "rice_blast",
        "neck blast": "rice_blast",
        "red rot": "red_rot",
        "smut": "sugarcane_smut",
        "purple blotch": "purple_blotch",
        "leaf curl": "leaf_curl_virus",
        "tylcv": "leaf_curl_virus",
        "black arm": "bacterial_blight_cotton",
        "bacterial blight": "bacterial_blight_cotton"
    }
    
    for kw, target_key in keywords_map.items():
        if kw in clean and target_key in DISEASES_KNOWLEDGE_BASE:
            return DISEASES_KNOWLEDGE_BASE[target_key]
            
    return None

def check_disease_plant_relevance(disease_name: str, plant_name: str) -> bool:
    """Validate if a specific disease is biologically known to infect a target plant."""
    if not disease_name or not plant_name:
        return True
        
    data = get_disease_data(disease_name)
    if not data:
        return True
        
    p_clean = plant_name.lower().strip()
    for host in data.get("host_plants", []):
        if host.lower() in p_clean or p_clean in host.lower():
            return True
            
    return False
