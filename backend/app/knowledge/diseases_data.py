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
        "disease_name": "Bacterial Blight of Cotton / Grey Mildew (Dahiya) / Black Arm",
        "scientific_name": "Xanthomonas citri pv. malvacearum / Ramularia areola",
        "pathogen_type": "Gram-negative Rod Bacterium & Ascomycete Fungus",
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
    },
    "sigatoka_leaf_spot": {
        "disease_name": "Sigatoka Leaf Spot (Yellow & Black Sigatoka)",
        "scientific_name": "Mycosphaerella musicola (Yellow) / Pseudocercospora fijiensis (Black)",
        "pathogen_type": "Ascomycete Foliar Fungus",
        "host_plants": ["Banana", "Plantain"],
        "symptoms": "Tiny chlorotic yellowish-green streaks appearing parallel to leaf veins on 3rd or 4th leaf. Streaks enlarge into elliptical brown or black spindle-shaped spots with distinctive light gray sunken centers and dark brown margins. Surrounding tissue turns yellow, dries up, and extensive spot coalescing causes premature leaf scorch and bunch defoliation.",
        "visual_symptoms": [
            "Linear yellowish spots progressing into dark brown cigar-shaped lesions with ash-gray centers",
            "Extensive leaf burning and drying from margin inwards",
            "Premature ripening of underdeveloped, undersized banana fingers on the tree"
        ],
        "causes": "Airborne ascospores and water-splashed conidia produced in necrotic leaf tissue.",
        "favorable_conditions": "High temperature (25°C to 30°C), relative humidity >85%, and frequent rainy spells. Extended leaf wetness >12 hours triggers rapid infection.",
        "spread_conditions": "Wind-borne ascospores for long distances; splashing raindrops and infected suckers for local spread.",
        "prevention": "Maintain proper plant spacing (1.8m x 1.8m) to facilitate sunlight and air circulation. De-leaf (surgically prune) heavily infected leaves (having >50% necrotic area) and incinerate or bury them. Ensure deep furrow drainage to prevent water stagnation.",
        "cultural_control": "Apply mineral agricultural spray oil (Banana spray oil @ 10 L/ha) to inhibit mycelial expansion. Avoid overhead sprinkler irrigation.",
        "biological_control": "Foliar spray of Bacillus subtilis (5 g/L) or Pseudomonas fluorescens (10 g/L). Spray cold-pressed Neem oil (5 ml/L) emulsified with detergent.",
        "chemical_management": "Systemic fungicides: Propiconazole 25% EC (1.0 ml/L), Difenoconazole 25% EC (0.5 to 1.0 ml/L), or Azoxystrobin 23% SC (1.0 ml/L) mixed with mineral spray oil (1%). Rotate with contact protectant Mancozeb 75% WP (2.5 g/L) or Copper Oxychloride 50% WP (2.5 g/L) to prevent fungicide resistance.",
        "safety_notes": "Alternate chemical groups (FRAC 3 and FRAC 11) to prevent fungal resistance. Follow 14-day PHI.",
        "when_to_seek_expert_help": "When younger leaves (leaves 1 and 2) show active necrotic lesions before shooting stage."
    },
    "panama_wilt": {
        "disease_name": "Panama Wilt (Fusarium Wilt / TR4)",
        "scientific_name": "Fusarium oxysporum f. sp. cubense (Foc Race 1 & Tropical Race 4)",
        "pathogen_type": "Soil-Borne Vascular Fungus (Chlamydospore Producer)",
        "host_plants": ["Banana (Grand Naine, Robusta, Rasthali, Ney Poovan)"],
        "symptoms": "Yellowing of the margins of older lower leaves progressing upwards. Petioles buckle and collapse at the junction with the pseudostem, forming a characteristic 'skirt' of dead leaves hanging around the pseudostem. Splitting of the pseudostem base longitudinally. When the corm/rhizome is cut transversely, prominent reddish-brown to black vascular discoloration rings are visible.",
        "visual_symptoms": [
            "Distinct yellowing of lower leaf margins progressing to whole leaf necrosis",
            "Buckled petioles hanging down around the trunk (skirt effect)",
            "Dark red, brown, or purplish-black discoloration in xylem vascular bundles of split pseudostem and corm"
        ],
        "causes": "Fusarium chlamydospores surviving in soil for over 20-30 years. Pathogen invades roots through lateral root junctions or nematode wounds and blocks vascular water transport.",
        "favorable_conditions": "Warm soil temperatures (24°C to 28°C), acidic soils (pH < 6.0), poor soil drainage, and presence of root-knot or lesion nematodes.",
        "spread_conditions": "Contaminated suckers/planting material, runoff water, tractor tires, farm footwear, and infected machetes.",
        "prevention": "Strict phytosanitary quarantine. Plant certified tissue-cultured banana plantlets only. Never use suckers from infested fields. Raise soil pH above 7.0 using lime/dolomite.",
        "cultural_control": "Crop rotation with paddy (flooding fields for 3-4 months drastically reduces chlamydospore survival) or sugarcane. Grow resistant/tolerant cultivars where TR4 is present.",
        "biological_control": "Soil enrichment with Trichoderma viride / harzianum (5 kg/ha) enriched in Farm Yard Manure (FYM) applied around root zones. Dip plantlet roots in Pseudomonas fluorescens slurry before planting.",
        "chemical_management": "Soil-borne vascular wilt cannot be cured by foliar sprays. Infected plants must be injected with 2% Carbendazim (10 ml per plant corm injection) and drenched with Copper Oxychloride (3 g/L) to prevent spread to adjacent healthy mats.",
        "safety_notes": "Eradicate severely diseased mats by uprooting, chopping, and burning, followed by lime drenching (500g lime per pit). Disinfect farm tools with 2% bleach.",
        "when_to_seek_expert_help": "Report suspected Tropical Race 4 (TR4) symptoms immediately to ICAR-NRCB (National Research Centre for Banana) or district agriculture department."
    },
    "bacterial_blight_pomegranate": {
        "disease_name": "Pomegranate Bacterial Blight / Telya",
        "scientific_name": "Xanthomonas axonopodis pv. punicae",
        "pathogen_type": "Gram-Negative Vascular & Foliar Bacterium",
        "host_plants": ["Pomegranate (Bhagwa, Arakta, Ganesh)"],
        "symptoms": "Water-soaked dark brown circular to angular oily spots on leaves surrounded by yellow halos. On stems and nodal regions, dark brown to black cankers develop causing shoot dieback and branch breaking. On fruits, characteristic oily dark brown triangular or L-shaped/Y-shaped cracking lesions appear on rind, ruining fruit market value.",
        "visual_symptoms": [
            "Dark brown oily spots with translucent water-soaked borders on foliage",
            "Nodal black cankers on main branches that snap easily under crop load",
            "Brownish-black star-shaped / Y-shaped cracking oily lesions on pomegranate rind"
        ],
        "causes": "Bacterium surviving in stem cankers, dormant buds, fallen leaves, and mummified fruits. Enters through stomata, hydathodes, and pruning wounds.",
        "favorable_conditions": "Cloudy, rainy weather with intermittent warm temperatures (28°C to 35°C) and high relative humidity (>75%) during Mrig/Hasta Bahar.",
        "spread_conditions": "Rain splashes, pruning secateurs, infected air-layered saplings, and overhead irrigation.",
        "prevention": "Prune all infected shoots 5-10 cm below cankers during dry weather; paste cut ends immediately with Bordeaux paste (10%). Disinfect secateurs with 1% Sodium Hypochlorite after every single cut. Bag developing fruits with butter paper covers.",
        "cultural_control": "Adopt Hasta Bahar (flowering Sept-Oct) or Ambe Bahar (Jan-Feb) to escape peak monsoon humidity. Clean orchard floor thoroughly.",
        "biological_control": "Foliar spray of Pseudomonas fluorescens (5 g/L) or Bacillus subtilis (5 g/L). Spray cold-pressed Neem seed kernel extract (NSKE 5%).",
        "chemical_management": "Prophylactic & curative bactericide schedule: Spray Streptocycline / Streptomycin Sulfate 90% + Tetracycline Hydrochloride 10% (0.5 g/L) mixed with Copper Oxychloride 50% WP (2.0 to 2.5 g/L) or Copper Hydroxide (2.0 g/L) at 10-12 day intervals during high risk rainy spells.",
        "safety_notes": "Do not exceed antibiotic dosage (0.5g/L) to prevent bacterial resistance and chemical residue. Observe 21-day PHI.",
        "when_to_seek_expert_help": "When nodal stem cankers develop on primary scaffold limbs or when fruit lesions appear in >10% of orchard."
    },
    "downy_mildew_grapes": {
        "disease_name": "Downy Mildew of Grapes",
        "scientific_name": "Plasmopara viticola",
        "pathogen_type": "Oomycete Biotrophic Water Mold",
        "host_plants": ["Grapes (Thompson Seedless, Sharad Seedless, Bangalore Blue, Flame Seedless)"],
        "symptoms": "Yellowish, translucent oily lesions ('oil spots') on the upper surface of leaves. Corresponding lower leaf surface develops dense, white cottony downy growth (sporangia) during humid mornings. Infected young shoots and flower clusters turn brown, curl like a shepherd's crook, and dry up. Infected berries turn leathery, brown, shrivel, and drop.",
        "visual_symptoms": [
            "Yellow oily translucent spots on upper leaf blade",
            "White delicate downy mold carpet on lower leaf surface directly beneath oil spots",
            "Dried, twisted flower clusters (shepherd's crook symptom) and shriveled brown berries"
        ],
        "causes": "Oospores overwintering in fallen leaves on soil. Releases swimming zoospores in presence of free moisture and rain.",
        "favorable_conditions": "The '3-10 Rule': Temperature >10°C, rainfall >10 mm within 24-48 hours, and young shoots >10 cm long with high humidity (>85%).",
        "spread_conditions": "Wind-blown sporangia and splashing rain drops in saturated wet vineyards.",
        "prevention": "Maintain open canopy via shoot thinning and leaf stripping around bunch zone to accelerate drying. Install drip irrigation and avoid wetting foliage.",
        "cultural_control": "Bury fallen leaves during winter cultivation. Apply balanced fertilization avoiding excessive nitrogen.",
        "biological_control": "Spray Trichoderma viride (5 g/L) or Ampelomyces quisqualis. Spray Potassium Phosphonate (Phytoalexin inducer) @ 3.0 ml/L.",
        "chemical_management": "Prophylactic protectants before rain: Bordeaux mixture 1% or Mancozeb 75% WP (2.5 g/L) or Copper Hydroxide (2 g/L). Curative systemic post-infection: Dimethomorph 50% WP (1.0 g/L), Metalaxyl-M + Mancozeb (2.5 g/L), Cymoxanil 8% + Mancozeb 64% WP (2.0 g/L), or Mandipropamid 23.4% SC (0.8 ml/L).",
        "safety_notes": "Spray systemic fungicides within 24-48 hours of rain event for curative kick-back action. Observe 30-day PHI for export grapes.",
        "when_to_seek_expert_help": "If white downy growth appears on flower clusters prior to cap fall or during 4-6mm berry stage."
    },
    "tikka_disease": {
        "disease_name": "Tikka Disease / Cercospora Leaf Spot",
        "scientific_name": "Cercospora arachidicola (Early Tikka) & Cercosporidium personatum (Late Tikka)",
        "pathogen_type": "Ascomycete Foliar Fungus",
        "host_plants": ["Groundnut (Peanut)"],
        "symptoms": "Early Tikka: Sub-circular dark brown spots with prominent bright yellow halos appearing 3-4 weeks after sowing on upper leaf surface. Late Tikka: Smaller circular nearly black carbonaceous spots on lower leaf surfaces without distinct yellow halos appearing 6-8 weeks after sowing. Severe infection causes massive premature leaf defoliation, leaving bare stems and leading to lightweight underdeveloped pods.",
        "visual_symptoms": [
            "Circular brown spots with yellow halos on upper leaves (Early Tikka)",
            "Intense dark black spots packed on lower leaf surface (Late Tikka)",
            "Severe leaf drop leading to bare upright stems and small hollow pods"
        ],
        "causes": "Fungus surviving in infected groundnut crop residues and seed pods. Dispersed by wind, splashing rain, and insects.",
        "favorable_conditions": "Warm humid conditions (25°C to 30°C) with prolonged relative humidity (>80%) and dew formation.",
        "spread_conditions": "Wind-borne conidia and rain splash.",
        "prevention": "Seed treatment with Carbendazim + Mancozeb (2g/kg seed). Crop rotation with sorghum, maize, or pearl millet. Burn or deeply plow infected crop stubble.",
        "cultural_control": "Intercropping groundnut with pearl millet (Bajra) or pigeonpea (Tur) in 4:1 ratio to reduce spore dispersion.",
        "biological_control": "Spray Trichoderma harzianum (5g/L) or Neem Seed Kernel Extract (NSKE 5%) or 3% Neem oil.",
        "chemical_management": "Apply Carbendazim 12% + Mancozeb 63% WP (Saaf @ 2 g/L) or Hexaconazole 5% EC (1.5 ml/L) or Tebuconazole 25.9% EC (1.0 ml/L) or Chlorothalonil 75% WP (2.0 g/L) at first appearance of leaf spots; repeat after 14 days if humid weather persists.",
        "safety_notes": "Wear protective gear during spraying. Follow 14-day PHI before harvesting fodder for dairy cattle.",
        "when_to_seek_expert_help": "When defoliation exceeds 25% of canopy during pod filling stage (50-70 DAS)."
    },
    "fusarium_wilt_chickpea": {
        "disease_name": "Chickpea Fusarium Wilt",
        "scientific_name": "Fusarium oxysporum f. sp. ciceris",
        "pathogen_type": "Soil-Borne Vascular Wilt Fungus",
        "host_plants": ["Chickpea (Bengal Gram / Chana / Harbara)"],
        "symptoms": "Sudden drooping and drying of leaves starting from the top branches without prior yellowing (in early wilt at seedling stage) or progressive yellowing and drying of leaves (in late wilt at flowering/pod stage). When the main taproot and collar stem are split longitudinally, internal vascular xylem strands show dark brown to black continuous discoloration.",
        "visual_symptoms": [
            "Drooping and downward curling of top leaflets in sunny afternoons",
            "Entire plant dries up and turns dull olive-green or light straw colored in patches",
            "Internal dark brown vascular xylem discoloration visible upon splitting the taproot"
        ],
        "causes": "Chlamydospores surviving in soil for 6-10 years and on internal seed tissues. Pathogen penetrates roots and chokes water transport.",
        "favorable_conditions": "Warm soil temperatures (25°C to 30°C) combined with dry topsoil and moisture stress in root zone.",
        "spread_conditions": "Infested field soil, farm machinery, irrigation runoff, and infected non-certified seeds.",
        "prevention": "Use wilt-resistant chickpea varieties (e.g. Digvijay, Vijay, JG-11, JAKI 9218, Vishal). Deep summer plowing during May-June to expose fungal spores to solar heat.",
        "cultural_control": "Rotate chickpea with non-hosts like wheat, mustard, barley, or sorghum for 3 years. Avoid deep sowing (>8-10 cm). Intercrop with linseed or mustard.",
        "biological_control": "Seed bio-priming: Treat 1 kg chickpea seed with 10g Trichoderma viride / harzianum + 10g Pseudomonas fluorescens + 25g Rhizobium culture. Mix 5 kg Trichoderma in 500 kg FYM and broadcast in furrow at sowing.",
        "chemical_management": "Seed dressing with Carbendazim 50% WP (1g/kg) + Thiram 75% WP (2g/kg) or Carboxin 37.5% + Thiram 37.5% DS (Vitavax Power @ 2g/kg seed). Note: Chemical foliar sprays cannot cure vascular wilt once inside root system.",
        "safety_notes": "Uproot and burn wilted plants from field to prevent localized chlamydospore concentration in soil.",
        "when_to_seek_expert_help": "When wilt mortality patches exceed 10% of field stand during early vegetative phase."
    },
    "blossom_end_rot": {
        "disease_name": "Blossom End Rot (BER)",
        "scientific_name": "Abiotic Physiological Disorder (Calcium Deficiency & Water Stress)",
        "pathogen_type": "Non-Pathogenic Physiological Nutritional Disorder",
        "host_plants": ["Tomato", "Chilli / Bell Pepper", "Brinjal (Eggplant)", "Watermelon"],
        "symptoms": "Begins as a small, water-soaked, light brownish sunken lesion at the blossom end (distal tip opposite to stem) of developing green fruits. As the fruit expands, the spot enlarges, becomes dark brown to pitch black, leathery, flat or concave, and dry. Secondary saprophytic black molds (such as Alternaria) often colonize the dead leathery patch.",
        "visual_symptoms": [
            "Sunken, flat, leathery, circular black or dark brown patch strictly at the bottom blossom end of the fruit",
            "Firm dry leather texture on the lesion, unlike soft rotting caused by bacterial soft rot",
            "Foliage of the plant often remains perfectly green and vigorous"
        ],
        "causes": "Localized deficiency of Calcium (Ca²⁺) in rapidly expanding fruit cells, triggered by fluctuating soil moisture (cycles of severe drought followed by over-irrigation), high soil salinity/EC, excessive ammonium (NH4+) or potassium (K+) fertilizer competing with calcium uptake, or damaged root systems.",
        "favorable_conditions": "Hot, dry, windy weather with high transpiration rates where water and calcium are pulled exclusively into leaves rather than expanding fruits.",
        "spread_conditions": "Non-infectious; does not spread from plant to plant.",
        "prevention": "Maintain uniform, consistent soil moisture through root-zone drip irrigation and plastic/organic mulching. Never allow soil to alternate between bone dry and waterlogged.",
        "cultural_control": "Apply Agricultural Lime or Gypsum based on soil test before planting. Avoid excess nitrogen (especially Ammonium Nitrate or Urea); use Nitrate-based nitrogen (Calcium Nitrate). Avoid deep mechanical hoeing close to plant stems to prevent root pruning.",
        "biological_control": "Incorporate rich vermicompost and mycorrhizal fungi (VAM) into soil to enhance root surface area for calcium absorption.",
        "chemical_management": "Foliar application: Spray Calcium Nitrate (Ca(NO3)2 @ 4.0 to 5.0 g/L) or Chelated Calcium (EDTA-Ca @ 1.0 to 1.5 g/L) mixed with Boron (0.5 g/L). Apply 2-3 foliar sprays starting from early flowering and initial pea-sized fruit set stage at 7-10 day intervals.",
        "safety_notes": "Foliar calcium must be directed specifically at young expanding fruit clusters, as calcium is immobile in plant phloem and does not readily translocate from leaves to fruits.",
        "when_to_seek_expert_help": "When more than 15% of first-truss fruit harvest shows sunken blossom end rot lesions."
    },
    "nutrient_deficiencies": {
        "disease_name": "Crop Nutrient Deficiencies (N, P, K, Zn, Fe, Ca, Mg, B)",
        "scientific_name": "Nutritional & Abiotic Imbalances",
        "pathogen_type": "Abiotic Physiological Nutrient Disorders",
        "host_plants": ["All Agricultural Crops, Fruits, and Vegetables"],
        "symptoms": "Diagnostic visual symptoms categorized by nutrient mobility in plant tissues: (1) Older / Lower Leaves First: Nitrogen (uniform pale yellow chlorosis), Phosphorus (purple/bronze leaf margins, stunted roots), Potassium (marginal leaf scorch, firing, tip burning), Magnesium (interveinal chlorosis on older leaves with green veins). (2) Younger / Top Leaves First: Iron (complete bleached ivory-yellow interveinal chlorosis on top new shoots), Zinc ('little leaf', rosette shoots, white bud in maize, brown blotches in rice), Calcium (blossom end rot, distorted hooked growing tips), Boron (brittle leaves, hollow stem, cracked deformed fruit with internal browning).",
        "visual_symptoms": [
            "Nitrogen (N): General yellowing starting from bottom mature leaves progressing upwards",
            "Potassium (K): Burnt, scorched leaf margins and tips on older leaves",
            "Iron (Fe): Bright yellow/white new leaves with crisp dark green veins in alkaline soils",
            "Zinc (Zn): Mottled interveinal chlorosis and rosette dwarfing of top leaves",
            "Boron (B): Cracking of fruits, hollow heart in cauliflower/radish, internal cork in apples"
        ],
        "causes": "Imbalanced fertilization, unfavorable soil pH (<5.5 locks P/Ca/Mg; >7.5 locks Fe/Zn/Mn/B), waterlogging, or excessive single-nutrient application causing antagonistic competition.",
        "favorable_conditions": "Calcareous, high pH sodic soils (induce Fe/Zn deficiency); coarse sandy leaching soils (induce N/K/B/Mg deficiency).",
        "spread_conditions": "Non-infectious abiotic disorder.",
        "prevention": "Conduct regular soil testing (Soil Health Card). Maintain soil pH between 6.2 and 7.2. Apply 10-15 tonnes/ha organic manure/compost to buffer micronutrient availability.",
        "cultural_control": "Green manuring with Sunnhemp or Dhaincha. Fertigation through drip lines with balanced water-soluble grades (19:19:19, 12:61:00, 0:0:50).",
        "biological_control": "Apply Phosphate Solubilizing Bacteria (PSB), Potash Mobilizing Bacteria (KMB), and Zinc Solubilizing Bacteria (ZSB) in soil.",
        "chemical_management": "Corrective foliar sprays: Nitrogen: 1-2% Urea foliar spray. Potassium: 1% Potassium Nitrate (13:0:45) or SOP (0:0:50). Iron: Chelated Iron Fe-EDTA 12% (1.0 g/L) or Ferrous Sulfate (5 g/L) + Citric Acid (1 g/L). Zinc: Chelated Zinc Zn-EDTA 12% (1.0 g/L) or Zinc Sulfate 21% (3-5 g/L). Boron: Solubor / Borax (1.0 to 1.5 g/L). Calcium: Calcium Nitrate (4-5 g/L). Magnesium: Magnesium Sulfate (5-10 g/L).",
        "safety_notes": "Avoid foliar spraying during intense midday sunshine to prevent leaf scorch. Always dissolve citric acid when mixing ferrous sulfate to maintain Fe²⁺ active state.",
        "when_to_seek_expert_help": "When entire crop canopy shows persistent chlorosis despite regular irrigation and basal NPK application."
    },
    "apple_scab": {
        "disease_name": "Apple Scab",
        "scientific_name": "Venturia inaequalis",
        "pathogen_type": "Ascomycete Hemibiotrophic Fungus",
        "host_plants": ["Apple", "Crabapple", "Pear"],
        "symptoms": "Olive-green to dull brown velvety spots on upper leaf surfaces, becoming dark brown, raised, and corky. Infected leaves curl, become distorted, and drop prematurely. On young fruits, circular olive-brown velvety lesions expand, become corky, crack deeply, and misshape the fruit, making it unmarketable.",
        "visual_symptoms": [
            "Olive-green to black velvety spots on leaves and fruit skin",
            "Severe corky cracking and deformation of apple fruits",
            "Premature summer defoliation leading to fruit drop"
        ],
        "causes": "Overwinters in fallen infected leaves as pseudothecia. Ascospores released in spring during rainy bud-break period.",
        "favorable_conditions": "Cool wet weather (16°C to 24°C) with extended leaf wetness (>9 hours following rain).",
        "spread_conditions": "Wind-borne ascospores in spring; rain-splashed conidia during summer.",
        "prevention": "Autumn sanitation: Spray fallen leaves with 5% Urea to accelerate leaf decay and destroy pseudothecia. Prune tree canopy to allow sunlight and rapid air drying.",
        "cultural_control": "Plant scab-resistant cultivars (e.g. Prima, Priscilla, Florina).",
        "biological_control": "Spray Bacillus subtilis (5 g/L) or Trichoderma viride (5 g/L) at bud break.",
        "chemical_management": "Prophylactic protectants: Mancozeb 75% WP (2.5 g/L), Captan 50% WP (2.5 g/L), or Dodine 65% WP (1.0 g/L) from green tip to pink bud stage. Curative post-infection: Difenoconazole 25% EC (0.5 ml/L), Hexaconazole 5% EC (1.0 ml/L), or Kresoxim-methyl 44.3% SC (0.5 ml/L) within 48-72 hours of rain infection period.",
        "safety_notes": "Strictly observe 30-day PHI for export quality apples. Alternate chemical classes to prevent triazole resistance.",
        "when_to_seek_expert_help": "When scab lesions appear on developing fruitlets at petal fall stage."
    },
    "guava_wilt": {
        "disease_name": "Guava Wilt",
        "scientific_name": "Fusarium oxysporum f. sp. psidii / Fusarium solani",
        "pathogen_type": "Soil-Borne Vascular Wilt Fungus",
        "host_plants": ["Guava (Psidium guajava)"],
        "symptoms": "Yellowing and slight drooping of leaves on one side of the plant (unilateral wilting) progressing to the entire tree. Leaves turn dark reddish-brown and shed rapidly. Complete drying of twigs, bark peeling, and vascular xylem browning visible when roots or stems are split longitudinally.",
        "visual_symptoms": [
            "Sudden wilting and drying of tree foliage in patches across orchard",
            "Reddish-yellow discoloration of mature foliage followed by total leaf drop",
            "Dark brown internal vascular discoloration of roots and lower trunk"
        ],
        "causes": "Soil-inhabiting fungus surviving for years in soil. Pathogen penetrates through root tips and nematode wounds, choking water transport.",
        "favorable_conditions": "High soil pH (7.5 - 8.5), heavy poorly drained soils, high root-knot nematode population, and rainy monsoon season (July-Sept).",
        "spread_conditions": "Infested nursery saplings, irrigation runoff, and root-grafting between neighboring trees.",
        "prevention": "Ensure good soil drainage. Treat nursery potting mix with Trichoderma harzianum. Plant resistant rootstocks like Psidium cattleianum (Strawberry Guava) or Psidium friedrichsthalianum (Chinese Guava).",
        "cultural_control": "Incorporate 10 kg neem cake per pit along with 50g Trichoderma. Avoid intercropping with solanaceous crops.",
        "biological_control": "Soil drenching around tree basin with Trichoderma harzianum (25-50 g/tree) enriched in 5 kg FYM + 250g mustard cake twice a year (June & October).",
        "chemical_management": "Drench root zone of surrounding trees immediately with Carbendazim 50% WP (2 g/L) or Copper Oxychloride 50% WP (3 g/L) along with Streptocycline (0.2 g/L). Uproot and burn dead trees; treat pit with 500g lime.",
        "safety_notes": "Chemical sprays cannot cure vascularly clogged trees; early root drenching of perimeter trees is critical.",
        "when_to_seek_expert_help": "When more than 5% of bearing orchard trees exhibit sudden unilateral leaf wilting."
    },
    "sterility_mosaic_pigeonpea": {
        "disease_name": "Pigeonpea Sterility Mosaic Disease (SMD)",
        "scientific_name": "Pigeonpea Sterility Mosaic Emaravirus (PPSMV)",
        "pathogen_type": "Segmented Negative-Sense RNA Plant Virus",
        "host_plants": ["Pigeonpea (Red Gram / Tur / Arhar)"],
        "symptoms": "Referred to as the 'Green Plague of Tur'. Affected plants develop bushy, dwarfed, excessive vegetative branching. Leaves become small, pale yellow with light green mosaic mottling, and exhibit downward curling. Infected plants suffer partial or total sterility (complete absence of flowers and pods), remaining green until harvest while yielding zero grain.",
        "visual_symptoms": [
            "Bushy, stunted dark/pale green foliage with profuse vegetative branching",
            "Mosaic chlorotic mottling on small leaflets",
            "Total absence of floral buds and pods on affected branches"
        ],
        "causes": "Virus transmitted obligately by microscopic Eriophyid mites (Aceria cajani) carried across fields by wind currents.",
        "favorable_conditions": "Cloudy humid weather and temperatures between 25°C to 30°C promoting mite vector multiplication.",
        "spread_conditions": "Wind-borne mite vectors and infected perennial pigeonpea ratoon plants.",
        "prevention": "Cultivate certified SMD-resistant varieties (BSMR-736, BSMR-853, BDN-711, ICPL-87119 / Asha). Rogue out and destroy infected bushy plants during early vegetative stage (30-45 DAS).",
        "cultural_control": "Avoid keeping ratoon pigeonpea crops during off-season as they act as perennial mite reservoirs.",
        "biological_control": "Foliar spray of cold-pressed Neem oil (5 ml/L) or NSKE 5% at 30 and 45 DAS to suppress mite populations.",
        "chemical_management": "Spray acaricides at first sign of mite infestation: Fenazaquin 10% EC (1.5 ml/L), Propargite 57% EC (2.0 ml/L), or Wettable Sulphur 80% WP (3.0 g/L) directed under leaf surfaces. Repeat after 15 days.",
        "safety_notes": "Early vector control before flowering is mandatory, as viral damage cannot be reversed after floral initiation.",
        "when_to_seek_expert_help": "When mosaic symptoms and bushy growth appear in >10% of field stand before 60 DAS."
    },
    "damping_off_nursery": {
        "disease_name": "Damping-Off in Seedlings & Nurseries",
        "scientific_name": "Pythium aphanidermatum / Rhizoctonia solani / Phytophthora spp.",
        "pathogen_type": "Soil-Borne Oomycete & Fungal Complex",
        "host_plants": ["Tomato", "Chilli", "Brinjal", "Cabbage", "Cauliflower", "Papaya", "Onion"],
        "symptoms": "Pre-emergence Damping-Off: Seeds rot and disintegrate in soil before germinating, leading to patchy seedling emergence. Post-emergence Damping-Off: Water-soaked, brown, constricted lesion develops at the ground level (collar region) of young succulent seedlings. The stem softens, rots, and topples over flat on the soil surface within 24-48 hours while the upper leaves are still green.",
        "visual_symptoms": [
            "Patchy empty gaps in nursery raised beds",
            "Water-soaked pinching/constriction at seedling collar line causing seedlings to fall over",
            "Cottony white mycelial web covering toppled dead seedlings in dense moist nurseries"
        ],
        "causes": "Soil-borne resting oospores and sclerotia activated by excessive moisture and poor seedbed drainage.",
        "favorable_conditions": "Overcrowded nursery sowing, excessive watering, cloudy humid weather, heavy clay soil, and temperatures between 24°C to 30°C.",
        "spread_conditions": "Infested nursery soil, contaminated irrigation water, and unsterilized seed trays/pro-trays.",
        "prevention": "Raise nursery seedlings on 15 cm elevated raised beds or in sterile cocopeat pro-trays under shade nets. Practice solarization of nursery beds with transparent polythene film (25-50 micron) for 30-40 days in May-June.",
        "cultural_control": "Thin sowing (avoid dense broadcast seed scattering). Ensure strict drainage; avoid overhead sprinkler flooding.",
        "biological_control": "Seed bio-priming with Trichoderma viride (10 g/kg seed). Mix 1 kg Trichoderma in 50 kg well-rotted FYM and incorporate into nursery topsoil.",
        "chemical_management": "Seed treatment: Thiram 75% WP (2 g/kg) or Metalaxyl 35% WS (2 g/kg). Soil drenching at seedling emergence: Copper Oxychloride 50% WP (2.5 g/L) or Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ @ 2.0 g/L) applied along nursery lines.",
        "safety_notes": "Avoid excessive watering after drenching. Ensure seedling trays drain freely.",
        "when_to_seek_expert_help": "When seedling mortality exceeds 15% in commercial nursery pro-trays."
    },
    "root_knot_nematode": {
        "disease_name": "Root-Knot Nematode Infestation",
        "scientific_name": "Meloidogyne incognita / Meloidogyne javanica",
        "pathogen_type": "Sedentary Microscopic Endoparasitic Nematode",
        "host_plants": ["Tomato", "Chilli", "Brinjal", "Pomegranate", "Banana", "Okra", "Watermelon", "Polyhouse Crops"],
        "symptoms": "Above-ground symptoms: Stunted unthrifty growth, chlorotic pale yellow leaves, daytime wilting even with adequate soil moisture, poor flowering, and drastic yield drop. Below-ground root symptoms: Roots develop distinctive swollen knots, galls, and club-like swellings, losing fibrous feeder root architecture.",
        "visual_symptoms": [
            "Distinct swollen galls and bumpy knots along the entire root system upon uprooting",
            "Daytime drooping of foliage under bright sunshine recovering at night",
            "Stunted chlorotic growth in circular field patches"
        ],
        "causes": "Second-stage infective juveniles (J2) penetrate root vascular cylinders and establish feeding giant cells.",
        "favorable_conditions": "Sandy, light-textured warm soils (25°C to 32°C) with continuous solanaceous or cucurbit cultivation.",
        "spread_conditions": "Infested soil, nursery saplings, runoff water, and tillage equipment.",
        "prevention": "Deep summer plowing to expose nematodes to sun desiccation. Trap cropping with African Marigold (Tagetes erecta) which exudes alpha-terthienyl nematicidal root compounds.",
        "cultural_control": "Crop rotation with non-host cereals (maize, sorghum, pearl millet). Soil solarization of nursery beds.",
        "biological_control": "Apply Paecilomyces lilacinus / Purpureocillium lilacinum (2.5-5.0 kg/ha enriched in FYM/neem cake) — nematode egg-parasitic bio-fungus. Apply Pochonia chlamydosporia or Pseudomonas fluorescens.",
        "chemical_management": "Apply Neem Cake (1-2 tonnes/ha) as basal. For severe polyhouse/field infestation: Apply Fluensulfone 2% GR (Nimitz @ 10 kg/acre) or Drench with Fluopyram 34.48% SC (Velum Prime @ 1.0-1.5 L/ha) through drip lines before planting.",
        "safety_notes": "Strictly observe 30-day PHI. Fluopyram must be applied directly to root zone via drip.",
        "when_to_seek_expert_help": "When galling index exceeds Grade 4 (>50% roots with heavy galls) in drip-irrigated crops."
    },
    "citrus_canker": {
        "disease_name": "Citrus Bacterial Canker",
        "scientific_name": "Xanthomonas axonopodis pv. citri",
        "pathogen_type": "Gram-Negative Plant Pathogenic Bacterium",
        "host_plants": ["Acid Lime (Kagzi Lime)", "Sweet Orange (Mosambi)", "Mandarin (Nagpur Orange)", "Grapefruit"],
        "symptoms": "Characteristic corky, raised, rough, crater-like canker lesions with oily translucent margins surrounded by prominent bright yellow chlorotic halos on leaves, twigs, thorns, and fruit rinds. Severe leaf and fruit drop and twig dieback.",
        "visual_symptoms": [
            "Raised blister-like corky brown crater lesions with yellow halos on leaves",
            "Rough, scabby, dark brown corky eruptions across citrus fruit skin",
            "Extensive premature defoliation and severe unmarketability of fruit"
        ],
        "causes": "Bacterium surviving in old twig cankers and leaf lesions. Enters via stomata and citrus leaf miner (Phyllocnistis citrella) feeding mines.",
        "favorable_conditions": "Warm rainy weather (28°C to 35°C) with heavy wind-driven rain showers during flush periods.",
        "spread_conditions": "Wind-blown rain, infected pruning secateurs, and leaf miner insect wounds.",
        "prevention": "Plant windbreaks around citrus orchards. Prune and burn all canker-affected twigs before new flush; paste cut surfaces with Bordeaux paste (10%).",
        "cultural_control": "Control citrus leaf miner actively during new vegetative flush with Imidacloprid 17.8% SL (0.4 ml/L) or Neem oil (5 ml/L) to prevent bacterial entry wounds.",
        "biological_control": "Spray Bacillus subtilis (5 g/L) or Pseudomonas fluorescens (10 g/L).",
        "chemical_management": "Spray Copper Oxychloride 50% WP (2.5 g/L) or Bordeaux Mixture (1%) combined with Streptocycline / Plantomycin (0.1 to 0.2 g/L or 100-200 ppm) at 15-day intervals during new vegetative flush and fruit development stages.",
        "safety_notes": "Do not exceed antibiotic dose to avoid phytotoxicity and bacterial resistance.",
        "when_to_seek_expert_help": "When fruit lesions develop on more than 20% of developing lime/orange crop."
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
        "bacterial blight": "bacterial_blight_cotton",
        "dahiya": "bacterial_blight_cotton",
        "grey mildew": "bacterial_blight_cotton",
        "cotton blight": "bacterial_blight_cotton",
        "sigatoka": "sigatoka_leaf_spot",
        "yellow sigatoka": "sigatoka_leaf_spot",
        "black sigatoka": "sigatoka_leaf_spot",
        "panama": "panama_wilt",
        "panama wilt": "panama_wilt",
        "telya": "bacterial_blight_pomegranate",
        "pomegranate blight": "bacterial_blight_pomegranate",
        "downy": "downy_mildew_grapes",
        "downy mildew": "downy_mildew_grapes",
        "tikka": "tikka_disease",
        "cercospora": "tikka_disease",
        "chickpea wilt": "fusarium_wilt_chickpea",
        "harbara wilt": "fusarium_wilt_chickpea",
        "blossom end rot": "blossom_end_rot",
        "ber": "blossom_end_rot",
        "deficiency": "nutrient_deficiencies",
        "chlorosis": "nutrient_deficiencies",
        "yellow leaves": "nutrient_deficiencies",
        "calcium deficiency": "nutrient_deficiencies",
        "iron deficiency": "nutrient_deficiencies",
        "zinc deficiency": "nutrient_deficiencies",
        "apple scab": "apple_scab",
        "scab": "apple_scab",
        "guava wilt": "guava_wilt",
        "sterility mosaic": "sterility_mosaic_pigeonpea",
        "smd": "sterility_mosaic_pigeonpea",
        "tur wilt": "sterility_mosaic_pigeonpea",
        "damping off": "damping_off_nursery",
        "damping-off": "damping_off_nursery",
        "nursery rot": "damping_off_nursery",
        "nematode": "root_knot_nematode",
        "root knot": "root_knot_nematode",
        "root galls": "root_knot_nematode",
        "citrus canker": "citrus_canker",
        "canker": "citrus_canker",
        "lemon canker": "citrus_canker"
    }
    
    for kw in sorted(keywords_map.keys(), key=len, reverse=True):
        target_key = keywords_map[kw]
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
