"""
AgroScan AI — Structured Plant & Crop Knowledge Base
Contains scientific, agronomic, soil, irrigation, fertilizer, disease, pest, and harvesting data
for major Indian crops, fruits, vegetables, and plantation trees.
"""

from typing import Dict, Any, List, Optional

PLANTS_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "mango": {
        "common_name": "Mango",
        "scientific_name": "Mangifera indica",
        "plant_type": "Perennial Fruit Tree",
        "soil": "Deep, rich, well-drained alluvial, red loamy, or laterite soil with good water permeability. Minimum soil depth should be 2 to 2.5 meters. Avoid shallow soils with rocky hardpan or waterlogged heavy clays.",
        "pH": "5.5 to 7.5 (slightly acidic to neutral).",
        "climate": "Tropical and subtropical climate with distinct dry period for flowering. Performs best in frost-free regions with high sunshine.",
        "temperature": "Optimum growing temperature: 24°C to 30°C. Tolerates up to 45°C during summer, but temperatures below 10°C severely impede flowering and fruit set.",
        "rainfall": "Annual rainfall of 750 mm to 2500 mm. Requires a dry spell of 2 to 3 months prior to flowering to induce flower bud differentiation.",
        "irrigation": "Young non-bearing trees: Irrigate every 3-5 days in summer and 8-10 days in winter. Bearing trees: Irrigate every 10-15 days from fruit set until maturity. CRITICAL: Withhold irrigation for 2-3 months prior to flowering (Nov-Dec in India) to promote profuse flowering; resume irrigation only after fruit set.",
        "planting": "Plant grafted saplings (Veneer/Epicotyl grafting) in 1m x 1m x 1m pits filled with topsoil, 50kg FYM, and 1kg Single Superphosphate during onset of monsoon (July-August).",
        "spacing": "Traditional spacing: 10m x 10m (100 trees/ha). High Density Planting (HDP): 5m x 5m (400 trees/ha) or Ultra High Density (UHDP): 3m x 2m (1600 trees/ha) with regular canopy pruning.",
        "growth_stages": [
            "Vegetative flush (post-harvest prune flush)",
            "Bud dormancy & differentiation (dry winter spell)",
            "Panicle emergence & flowering (Jan-March)",
            "Fruit set (pea and marble stage)",
            "Fruit development & maturation (April-June)",
            "Harvest maturity & post-harvest flush"
        ],
        "fertilizer": "Bearing tree (10+ years): 1000g N, 500g P2O5, 1000g K2O per tree per year. Apply in two splits: 50% post-harvest (July-Aug) with 50kg FYM/compost, and 50% during fruit development (Feb-March). Foliar spray of 0.2% Borax and 0.5% Zinc Sulfate at panicle emergence prevents blossom drop and improves fruit retention.",
        "pests": [
            "Mango Hopper (Idioscopus spp.) — sucks sap from tender panicles causing blossom blight and sooty mold.",
            "Fruit Fly (Bactrocera dorsalis) — lays eggs under ripening fruit skin causing internal maggots and rotting.",
            "Stem Borer (Batocera rufomaculata) — bores into trunk causing branch wilting and frass accumulation.",
            "Mealybug (Drosicha mangiferae) — crawls up trunk during Dec-Jan and attacks panicles."
        ],
        "diseases": [
            "Powdery Mildew (Oidium mangiferae) — white powdery coating on panicles causing blossom drop.",
            "Anthracnose (Colletotrichum gloeosporioides) — black sunken spots on leaves, flowers, and developing fruits.",
            "Dieback (Lasiodiplodia theobromae) — drying of twigs from top downwards with brown discoloration."
        ],
        "prevention": "Prune overlapping and dead branches annually after harvest to ensure sunlight penetration. Band tree trunks with 30cm polythene grease bands in December to block mealybug nymphs. Practice orchard sanitation by clearing dropped panicles and mummified fruits.",
        "harvesting": "Harvest when fruits attain physiological maturity: shoulders swell above the stem attachment, pit around pedicel deepens, skin color lightens from dark green to olive/yellowish green, and specific gravity reaches 1.01-1.02. Harvest with 1-2 cm pedicel attached using pole harvesters with nylon catching nets to prevent latex burn and impact injury.",
        "post_harvest": "Wash fruits in clean water to remove latex sap. De-sap for 4 hours. Hot water treatment at 48°C for 5 minutes prevents Anthracnose and fruit fly infestation. Store at 12°C - 13°C with 85-90% relative humidity. Shelf life: 2-3 weeks."
    },
    "sugarcane": {
        "common_name": "Sugarcane",
        "scientific_name": "Saccharum officinarum",
        "plant_type": "Perennial Cash Crop / Grass",
        "soil": "Deep, well-drained, fertile loamy or clay loam soil rich in organic matter. Soil depth should be at least 60 cm to allow vigorous root system. Avoid saline, alkaline, or waterlogged soils.",
        "pH": "6.5 to 7.5 (tolerates 6.0 to 8.0).",
        "climate": "Warm, sunny, humid tropical climate during vegetative growth, transitioning to a dry, sunny, cool period during ripening and sugar accumulation.",
        "temperature": "Optimum germination: 27°C to 32°C. Optimum vegetative growth: 28°C to 35°C. Temperatures below 15°C slow elongation and below 10°C induce growth arrest.",
        "rainfall": "Requires 1500 mm to 2500 mm rainfall annually or equivalent irrigation.",
        "irrigation": "Water-intensive crop (1500-2000 mm water requirement). Formative stage: irrigate every 6-8 days in summer. Grand growth stage: irrigate every 10-12 days. Ripening stage: irrigate every 15-20 days. Critical: Withhold irrigation 20-25 days before harvest to concentrate sucrose content in stalks.",
        "planting": "Plant 3-budded setts (35,000-40,000 setts/ha) treated with Carbendazim (1g/L) in 20-25 cm deep furrows. Planting seasons: Adsali (July-August, 16-18 months), Pre-seasonal (Oct-Nov, 14-15 months), Suru (Jan-Feb, 12 months).",
        "spacing": "Single row: 90 cm to 120 cm row-to-row. Paired row / Trench method: 60 cm - 120 cm - 60 cm for drip line installation and intercropping.",
        "growth_stages": [
            "Germination phase (0 to 35 days)",
            "Tillering / Formative phase (35 to 120 days)",
            "Grand growth phase (120 to 270 days)",
            "Ripening & maturation phase (270 to 360+ days)"
        ],
        "fertilizer": "Suru crop recommended NPK: 250:115:115 kg/ha. Apply full P2O5 and 50% K2O as basal at planting. Nitrogen applied in split doses: 10% at planting, 40% at 6-8 weeks (tillering), 10% at 12-14 weeks, and 40% at final earthing up (120-150 days) along with remaining 50% K2O. Incorporate 25 tonnes/ha FYM and 5kg/ha Acetobacter bio-fertilizer.",
        "pests": [
            "Early Shoot Borer (Chilo infuscatellus) — causes 'dead heart' in 1-3 month old shoots.",
            "Top Borer (Scirpophaga excerptalis) — damages apical growing point causing bunchy top.",
            "Pyrilla / Leafhopper (Pyrilla perpusilla) — sucks sap and secretes honeydew leading to sooty mold.",
            "White Grub (Holotrichia consanguinea) — feeds on root system causing lodging and plant death."
        ],
        "diseases": [
            "Red Rot (Colletotrichum falcatum) — third and fourth leaves wither, stalks show internal longitudinal red reddening with white cross-bands and alcohol smell.",
            "Smut (Sporisorium scitamineum) — produces long whip-like black dusty structure from apical shoot.",
            "Wilt (Cephalosporium sacchari) — gradual drying of crown and hollow pith discoloration.",
            "Grassy Shoot Disease (Phytoplasma) — profuse stunted tillers giving bushy grassy appearance."
        ],
        "prevention": "Use certified disease-free setts from heat-treated nurseries. Hot water treatment of setts at 50°C for 2 hours eliminates red rot and grassy shoot pathogen. Practice trash mulching (3-4 t/ha) after earthing up to conserve soil moisture and suppress shoot borer. Avoid continuous ratoon in red-rot infested fields.",
        "harvesting": "Harvest when crop reaches physiological maturity: brix reading on hand refractometer reaches 18-20%, lower leaves dry out, and vegetative growth ceases. Cut stalks flush with ground level with sharp cane knife; underground portion contains highest sucrose concentration.",
        "post_harvest": "Transport harvested cane to sugar mill within 24-48 hours to minimize post-harvest sucrose inversion and sugar recovery loss."
    },
    "tomato": {
        "common_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "plant_type": "Annual Solanaceous Vegetable",
        "soil": "Well-drained, fertile sandy loam to clay loam rich in organic matter. Avoid poorly drained waterlogged soils which promote bacterial wilt and damping-off.",
        "pH": "6.0 to 6.8 (ideal for nutrient uptake).",
        "climate": "Warm temperate and subtropical climate. Sensitive to severe frost and continuous rain during flowering.",
        "temperature": "Optimum daytime temp: 21°C to 28°C; nighttime temp: 15°C to 20°C. Temperatures above 35°C cause blossom drop and poor fruit setting.",
        "rainfall": "Requires 600 mm to 1200 mm evenly distributed throughout the growing season.",
        "irrigation": "Drip irrigation is strongly recommended. Irrigate at 3-5 day intervals depending on soil type. Maintain uniform moisture; erratic alternating dry and wet cycles induce Blossom End Rot and fruit cracking. Avoid overhead sprinkler irrigation to keep foliage dry.",
        "planting": "Sow seeds (400-500g/ha for open-pollinated, 150-200g/ha for hybrids) in raised nursery beds. Transplant 25-30 day old sturdy seedlings with 4-5 true leaves into main field.",
        "spacing": "Determinate varieties: 60 cm x 45 cm. Indeterminate (trellised) hybrids: 90 cm x 45 cm or 120 cm x 60 cm paired rows.",
        "growth_stages": [
            "Nursery & seedling establishment (0 to 30 days)",
            "Vegetative growth & branching (30 to 50 days)",
            "Flowering & fruit setting (50 to 75 days)",
            "Fruit enlargement & color break (75 to 100 days)",
            "Harvesting period (100 to 140 days)"
        ],
        "fertilizer": "NPK 120:60:60 kg/ha for varieties; 180:100:150 kg/ha for high-yielding hybrids. Apply 50% N, full P, and 50% K as basal dose with 20 t/ha FYM. Top-dress remaining Nitrogen and Potash in two equal splits at 30 and 50 days after transplanting. Foliar spray of Calcium Nitrate (0.5%) and Boron (0.1%) during fruit development prevents blossom end rot.",
        "pests": [
            "Tomato Fruit Borer (Helicoverpa armigera) — bores into green and ripening fruits.",
            "Whitefly (Bemisia tabaci) — vector for Tomato Yellow Leaf Curl Virus (TYLCV).",
            "Leaf Miner (Liriomyza trifolii) — creates serpentine white mines on leaves.",
            "Spider Mites (Tetranychus urticae) — causes speckled bronzing under leaves in dry weather."
        ],
        "diseases": [
            "Early Blight (Alternaria solani) — concentric target-board dark brown spots on lower leaves.",
            "Late Blight (Phytophthora infestans) — water-soaked dark lesions with white mold in cool humid weather.",
            "Bacterial Wilt (Ralstonia solanacearum) — sudden rapid green wilting without initial yellowing.",
            "Tomato Yellow Leaf Curl Virus (TYLCV) — severe leaf curling, chlorosis, and stunted bushy growth."
        ],
        "prevention": "Stake plants off the ground with bamboo trellising. Remove lower suckers and bottom leaves up to 30 cm above soil to prevent soil-splash pathogens. Use reflective silver-black mulching. Practice 3-year crop rotation with non-solanaceous crops (e.g. cereals, pulses).",
        "harvesting": "Harvest at mature green, breaker stage (10% pink at blossom end), or turning/pink stage depending on transport distance. Pick manually with calyx intact every 3-4 days.",
        "post_harvest": "Sort and grade by size and color. Store breaker/pink stage tomatoes at 12°C - 15°C with 85-90% RH (never store unripe tomatoes below 10°C to avoid chilling injury). Shelf life: 2-3 weeks."
    },
    "potato": {
        "common_name": "Potato",
        "scientific_name": "Solanum tuberosum",
        "plant_type": "Annual Tuber Crop",
        "soil": "Loose, friable, well-aerated sandy loam or loamy soil rich in organic matter. Free from stones and hard clods to permit unrestricted tuber expansion.",
        "pH": "5.2 to 6.4 (slightly acidic soil suppresses Common Scab).",
        "climate": "Cool season crop. Requires cool nights and sunny moderate days.",
        "temperature": "Vegetative stage: 20°C to 24°C. Tuber initiation and bulking: 16°C to 20°C. Tuberization stops completely when night temperatures exceed 24°C.",
        "rainfall": "500 mm to 700 mm evenly distributed throughout the 90-110 day cycle.",
        "irrigation": "Total water requirement: 400-500 mm. Irrigate lightly after planting. Maintain 65-75% available soil moisture during tuber initiation and bulking (every 8-10 days). Stop irrigation 10-12 days before harvest to allow skin curing in the soil.",
        "planting": "Plant certified, sprouted disease-free seed tubers (35-45 mm diameter, 40-50g weight) 5-7 cm deep on ridges during October-November in North/Central Indian plains.",
        "spacing": "60 cm between ridges, 20 cm between seed tubers within the furrow.",
        "growth_stages": [
            "Sprout development and emergence (0 to 20 days)",
            "Vegetative canopy growth (20 to 45 days)",
            "Tuber initiation / Stolons (45 to 60 days)",
            "Tuber bulking phase (60 to 85 days)",
            "Maturation & vine senescence (85 to 105 days)"
        ],
        "fertilizer": "NPK 120:80:100 kg/ha with 25 t/ha well-rotted FYM. Apply full P2O5 and full K2O with 50% Nitrogen as basal at planting. Top-dress remaining 50% Nitrogen at earthing up (30-35 days after planting).",
        "pests": [
            "Potato Tuber Moth (Phthorimaea operculella) — mines leaves in field and bores into stored tubers.",
            "Aphids (Myzus persicae) — transmits viral diseases (PVY, PLRV).",
            "Cutworms (Agrotis ipsilon) — cuts young seedlings at soil level at night."
        ],
        "diseases": [
            "Late Blight (Phytophthora infestans) — devastating water-soaked necrotic lesions on foliage and dry rot in tubers.",
            "Early Blight (Alternaria solani) — brown angular spots with target rings.",
            "Black Scurf (Rhizoctonia solani) — black sclerotial encrustations on tuber skin.",
            "Common Scab (Streptomyces scabies) — corky raised or pitted lesions on tuber skin."
        ],
        "prevention": "Perform thorough earthing-up at 30 and 45 days to keep tubers well-covered with soil (prevents greening and tuber moth oviposition). Treat seed tubers with Mancozeb (2.5g/L) or Trichoderma before planting. Practice dehaulming (cutting vines) 10-12 days before digging.",
        "harvesting": "Dehaulm when crop reaches physiological maturity (85-100 days). Allow tubers to cure underground for 10-12 days so skin thickens. Dig carefully during dry weather using tractor-drawn diggers or hand spades.",
        "post_harvest": "Cure harvested tubers in cool, dark, well-ventilated shed for 10-15 days at 15-20°C to heal minor bruises. Store in commercial cold storage at 4°C - 7°C with 90-95% RH for seed potatoes or 8-10°C with CIPC sprout inhibitor for table/processing potatoes."
    },
    "cotton": {
        "common_name": "Cotton",
        "scientific_name": "Gossypium hirsutum",
        "plant_type": "Annual / Perennial Fiber Cash Crop",
        "soil": "Deep, fertile black clay soils (Vertisols) with high water-holding capacity or well-drained alluvial loams with minimum depth of 90 cm.",
        "pH": "6.5 to 8.0.",
        "climate": "Warm, sunny, semi-arid tropical and subtropical climate with long frost-free growing period (180-200 days).",
        "temperature": "Germination: 20°C to 28°C. Vegetative and boll growth: 25°C to 35°C. Excessive heat above 40°C during flowering causes flower and square shed.",
        "rainfall": "600 mm to 1000 mm during vegetative period, followed by dry weather during boll opening and harvesting.",
        "irrigation": "Critical irrigation stages: Flowering/Square formation and Boll development. Avoid waterlogging during seedling stage and excessive irrigation during late maturity to prevent vegetative regrowth.",
        "planting": "Dibble acid-delinted seeds treated with Imidacloprid (5g/kg) and Trichoderma (10g/kg) at 3-4 cm depth upon onset of monsoon (June-July).",
        "spacing": "Bt Cotton Hybrids: 90 cm x 60 cm or 120 cm x 45 cm. High Density Planting System (HDPS): 60 cm x 15 cm or 75 cm x 10 cm.",
        "growth_stages": [
            "Germination and seedling stage (0 to 30 days)",
            "Squaring / floral bud initiation (30 to 60 days)",
            "Flowering and boll formation (60 to 110 days)",
            "Boll bursting and fiber maturation (110 to 160 days)",
            "Picking and harvest flushes (160 to 200 days)"
        ],
        "fertilizer": "NPK 120:60:60 kg/ha for rainfed Bt hybrids; 150:75:75 kg/ha under irrigation. Apply 20% N, full P, and 50% K as basal. Remaining Nitrogen applied in 3 equal splits (square initiation, flowering, boll development). Foliar spray of 2% Urea or 1% 13-0-45 (Potassium Nitrate) and 0.5% Magnesium Sulfate during peak boll formation prevents leaf reddening.",
        "pests": [
            "Pink Bollworm (Pectinophora gossypiella) — larva enters young bolls, rosette flowers, causes internal lint staining.",
            "Whitefly (Bemisia tabaci) — vector for Cotton Leaf Curl Virus (CLCuV).",
            "Thrips & Jassids / Leafhoppers (Amrasca biguttula) — causes leaf curling, downward hopper burn."
        ],
        "diseases": [
            "Bacterial Blight / Black Arm (Xanthomonas citri pv. malvacearum) — angular water-soaked leaf spots and black stem lesions.",
            "Alternaria Leaf Spot (Alternaria macrospora) — necrotic brown spots with purple margins.",
            "Fusarium and Verticillium Wilt — vascular browning and progressive wilting."
        ],
        "prevention": "Install pheromone traps (5/ha for monitoring, 20/ha for mass trapping of Pink Bollworm). Grow non-Bt refuge crops around Bt plots. Terminate crop by December-January (avoid extending to summer) to break Pink Bollworm lifecycle.",
        "harvesting": "Pick fully burst, clean bolls manually after dew has dried in the morning. Pick in 3-4 rounds at 15-20 day intervals. Keep picked seed cotton free from dried bracts and leaf trash.",
        "post_harvest": "Dry picked cotton under shade to reduce moisture content below 8-9% before storage and ginning."
    },
    "rice": {
        "common_name": "Rice (Paddy)",
        "scientific_name": "Oryza sativa",
        "plant_type": "Annual Cereal / Semi-aquatic Crop",
        "soil": "Heavy clay or clay loam soils with high water retention and impermeable subsoil hardpan (prevents deep percolation).",
        "pH": "5.5 to 7.0.",
        "climate": "Hot, humid tropical climate with abundant sunshine and continuous warm water supply.",
        "temperature": "Optimum growing temp: 22°C to 32°C. Panicle initiation requires >20°C; extreme temp (>35°C or <15°C) during flowering causes spikelet sterility.",
        "rainfall": "1200 mm to 2000 mm during crop cycle (or equivalent assured canal/tube-well irrigation).",
        "irrigation": "Maintain 2-5 cm shallow standing water during tillering and panicle development. Alternate Wetting and Drying (AWD) saves 25-30% water without reducing yield. Drain field 10 days prior to harvest.",
        "planting": "Transplant 21-25 day old nursery seedlings (2-3 seedlings per hill) in well-puddled leveled fields during June-July (Kharif) or Dec-Jan (Rabi). Direct Seeded Rice (DSR) using zero-till seed drills is practiced in water-scarce regions.",
        "spacing": "20 cm row-to-row, 15 cm hill-to-hill.",
        "growth_stages": [
            "Nursery & transplanting (0 to 25 days)",
            "Active tillering (25 to 55 days)",
            "Panicle initiation & booting (55 to 80 days)",
            "Flowering and heading (80 to 95 days)",
            "Milking, dough, and grain maturity (95 to 130 days)"
        ],
        "fertilizer": "NPK 120:60:40 kg/ha with 25 kg/ha Zinc Sulfate. Apply full P2O5 and 50% K2O as basal during puddling. Nitrogen applied in 3 equal splits: basal, maximum tillering, and panicle initiation.",
        "pests": [
            "Yellow Stem Borer (Scirpophaga incertulas) — causes 'dead heart' at tillering and 'white earhead' at flowering.",
            "Brown Planthopper (Nilaparvata lugens) — causes circular 'hopper burn' patches in dense canopies.",
            "Gall Midge (Orseolia oryzae) — transforms tillers into hollow tubular 'silver shoots'."
        ],
        "diseases": [
            "Rice Blast (Magnaporthe oryzae) — spindle-shaped lesions on leaves and black rot of panicle neck (Neck Blast).",
            "Bacterial Leaf Blight (Xanthomonas oryzae) — undulating yellow wavy margins running down leaf blades.",
            "Sheath Blight (Rhizoctonia solani) — snake-skin oval grayish lesions on leaf sheaths near water line."
        ],
        "prevention": "Avoid excessive nitrogen top-dressing. Maintain field drainage intervals. Treat seeds with Carbendazim (2g/kg) or Pseudomonas fluorescens (10g/kg). Clip seedling leaf tips before transplanting to remove stem borer egg masses.",
        "harvesting": "Harvest when 85-90% of panicles turn golden yellow and grain moisture drops to 20-22%. Cut close to ground with combine harvester or sickle.",
        "post_harvest": "Thresh promptly and sun-dry grains on clean tarpaulin to reach 12-14% storage moisture to prevent storage fungi and yellowing."
    },
    "wheat": {
        "common_name": "Wheat",
        "scientific_name": "Triticum aestivum",
        "plant_type": "Annual Rabi Cereal",
        "soil": "Well-drained fertile loam, silt loam, or clay loam soils with good tilth and organic matter.",
        "pH": "6.0 to 7.5.",
        "climate": "Cool winter growing season followed by bright, warm, dry weather during grain filling and ripening.",
        "temperature": "Germination: 20°C to 25°C. Tillering: 15°C to 20°C. Grain filling: 20°C to 23°C. High heat (>30°C) during terminal grain fill causes terminal heat stress and shriveling.",
        "rainfall": "350 mm to 550 mm total water requirement.",
        "irrigation": "Requires 5 to 6 critical irrigations: 1) Crown Root Initiation (CRI at 20-25 days — MOST CRITICAL), 2) Tillering (40-45 days), 3) Late jointing (60-65 days), 4) Flowering (80-85 days), 5) Milking (100-105 days), 6) Dough stage (115-120 days).",
        "planting": "Sow certified seeds (100 kg/ha for timely sowing, 125 kg/ha for late sowing) with seed drill 4-5 cm deep in moist soil during November.",
        "spacing": "20 cm to 22.5 cm between rows.",
        "growth_stages": [
            "Crown Root Initiation (CRI) (20-25 days)",
            "Tillering phase (30-50 days)",
            "Jointing and stem elongation (50-75 days)",
            "Booting and heading/anthesis (75-95 days)",
            "Grain filling and maturity (95-130 days)"
        ],
        "fertilizer": "NPK 120:60:40 kg/ha with 25 kg/ha Zinc Sulfate. Apply full P, full K, and 50% N as basal at sowing. Top-dress remaining 50% Nitrogen in two equal splits after 1st irrigation (CRI) and 2nd irrigation.",
        "pests": [
            "Wheat Aphid (Sitobion avenae) — sucks sap from earheads during grain filling.",
            "Termites (Odontotermes obesus) — damages seedlings in light soils.",
            "Armyworm (Mythimna separata) — feeds on leaves and panicles at night."
        ],
        "diseases": [
            "Yellow / Stripe Rust (Puccinia striiformis) — linear yellow powdery stripes on leaves in cool humid zones.",
            "Brown / Leaf Rust (Puccinia triticina) — scattered orange-brown pustules on leaf surface.",
            "Loose Smut (Ustilago tritici) — entire earhead transformed into black powdery mass of chlamydospores.",
            "Karnal Bunt (Tilletia indica) — partial conversion of kernels into black foul-smelling powder."
        ],
        "prevention": "Sow rust-resistant varieties. Treat seed with Carboxin (2g/kg). Avoid delayed sowing past November 25 to evade terminal heat stress and late rust infections.",
        "harvesting": "Harvest when straw turns yellow-dry, kernels become hard, and moisture drops below 14%. Thresh with mechanical thresher or combine.",
        "post_harvest": "Dry grain to 10-12% moisture before storage in airtight metal bins or silos treated with aluminum phosphide for weevil protection."
    },
    "chilli": {
        "common_name": "Chilli (Pepper)",
        "scientific_name": "Capsicum annuum",
        "plant_type": "Annual / Biennial Solanaceous Spice Vegetable",
        "soil": "Well-drained, fertile sandy loam, clay loam, or red loamy soil. Sensitive to poor drainage and water stagnation.",
        "pH": "6.0 to 7.0.",
        "climate": "Warm humid tropical climate during vegetative growth, dry climate during fruit maturation.",
        "temperature": "Optimum temp: 20°C to 30°C. Cold weather (<10°C) stops growth; extreme heat (>38°C) causes heavy flower and fruit drop.",
        "rainfall": "600 mm to 1000 mm.",
        "irrigation": "Maintain light, frequent drip irrigations at 4-6 day intervals. Avoid flooding to prevent collar rot (Phytophthora) and wilt.",
        "planting": "Transplant 35-40 day nursery seedlings (1.0-1.5 kg seeds/ha for open varieties, 200-250g/ha for hybrids) on raised beds with drip irrigation.",
        "spacing": "60 cm x 45 cm or 75 cm x 60 cm.",
        "growth_stages": [
            "Nursery & transplanting (0 to 40 days)",
            "Vegetative branching (40 to 70 days)",
            "Flowering & fruit set (70 to 100 days)",
            "Green chilli picking / Red ripening (100 to 180 days)"
        ],
        "fertilizer": "NPK 100:50:50 kg/ha for varieties; 150:75:75 kg/ha for hybrids with 25 t/ha FYM. Apply 50% N, full P, and full K as basal. Split remaining N in two top-dressings at 30 and 60 days after transplanting.",
        "pests": [
            "Chilli Thrips (Scirtothrips dorsalis) — upward boat-shaped leaf curling and brown scarred fruits.",
            "Yellow Mite (Polyphagotarsonemus latus) — downward inverted-cup curling of leaves.",
            "Fruit Borer (Helicoverpa armigera) — feeds on developing pods.",
            "Aphids and Whiteflies — vectors of virus complexes."
        ],
        "diseases": [
            "Anthracnose / Dieback / Fruit Rot (Colletotrichum capsici) — circular sunken necrotic spots on ripe fruits with concentric black acervuli.",
            "Chilli Leaf Curl Virus (Begomovirus) — puckering, severe stunting, and bushy crown.",
            "Powdery Mildew (Leveillula taurica) — white powdery growth on leaf undersides with yellow patches above."
        ],
        "prevention": "Install blue sticky traps (for thrips) and yellow sticky traps (for whiteflies). Intercrop with 2 rows of maize or marigold as border barrier crops. Treat seed with Trichoderma (10g/kg).",
        "harvesting": "Pick green chillies at firm mature stage every 7-10 days. For dry red chilli, allow pods to turn deep uniform red on the plant before picking.",
        "post_harvest": "Dry red chillies on clean cement drying floors or solar polyhouse driers to 10% moisture content. Retains bright red color and capsaicin content."
    },
    "onion": {
        "common_name": "Onion",
        "scientific_name": "Allium cepa",
        "plant_type": "Biennial Herbaceous Bulb Crop",
        "soil": "Deep, friable, well-drained loamy to sandy loam soil rich in organic matter. Free from compact hardpan to allow uniform bulb expansion.",
        "pH": "6.0 to 7.2 (sensitive to acidic soils below pH 6.0).",
        "climate": "Mild cool climate during vegetative growth, warm dry weather during bulb development and maturity.",
        "temperature": "Vegetative stage: 13°C to 24°C. Bulb formation: 16°C to 25°C. Bulb maturity: 25°C to 32°C.",
        "rainfall": "650 mm to 800 mm evenly distributed.",
        "irrigation": "Shallow root system requires frequent light irrigations (every 5-7 days in summer, 8-10 days in winter). CRITICAL: Stop irrigation 10-15 days before harvest to allow neck drying and prevent bulb rot during storage.",
        "planting": "Kharif crop: Sow nursery in May-June, transplant in July-August. Late Kharif (Rangada): Sow in Aug-Sept, transplant in Oct-Nov. Rabi crop: Sow in Oct-Nov, transplant in Dec-Jan. Seed rate: 8-10 kg/ha.",
        "spacing": "15 cm row-to-row, 10 cm plant-to-plant on flat beds or broad bed furrows (BBF).",
        "growth_stages": [
            "Nursery seedling stage (0 to 45 days)",
            "Vegetative leaf growth (45 to 80 days)",
            "Bulb initiation & enlargement (80 to 120 days)",
            "Neck fall and maturity (120 to 140 days)"
        ],
        "fertilizer": "NPK 100:50:50 kg/ha + 30 kg/ha Sulfur with 20 t/ha FYM. Apply 50% N, full P, full K, and full S as basal at transplanting. Top-dress remaining Nitrogen in two equal splits at 30 and 45 days. Avoid nitrogen application after 60 days (causes thick necks and poor storage).",
        "pests": [
            "Onion Thrips (Thrips tabaci) — silvery white patches on leaf blades causing blast appearance.",
            "Onion Maggot (Delia antiqua) — bores into base of developing bulbs causing rotting."
        ],
        "diseases": [
            "Purple Blotch (Alternaria porri) — small water-soaked lesions that turn dark purple-brown with concentric zones.",
            "Stemphylium Leaf Blight (Stemphylium vesicarium) — small yellow to orange flecks expanding into elongated patches.",
            "Basal Rot (Fusarium oxysporum f. sp. cepae) — yellowing and dying back of leaves from tips; rotting of bulb base."
        ],
        "prevention": "Ensure good drainage. Spray Mancozeb (2.5g/L) with sticking agent (Triton/liquid soap 1ml/L) preventively during cloudy, humid weather. Practice 3-year crop rotation.",
        "harvesting": "Harvest when 50% of tops have naturally fallen over (neck fall) and dried. Pull bulbs gently on dry sunny day.",
        "post_harvest": "Field cure under shade with leaves covering bulbs for 3-5 days, then clip tops leaving 2.5 cm neck. Further shade cure in ventilated storage structures (chawls) for 10-15 days. Store in well-ventilated bamboo/wooden structures at ambient temp (25-30°C) with 65-70% RH."
    },
    "soybean": {
        "common_name": "Soybean",
        "scientific_name": "Glycine max",
        "plant_type": "Annual Legume Oilseed Crop",
        "soil": "Fertile, well-drained loamy to clay loam soils with good organic carbon content. Neutral pH.",
        "pH": "6.5 to 7.5.",
        "climate": "Warm and moist tropical to subtropical climate.",
        "temperature": "Optimum: 20°C to 30°C. Below 15°C retards growth and above 38°C causes flower drop.",
        "rainfall": "600 mm to 900 mm during Kharif season.",
        "irrigation": "Primarily rainfed in India; protective irrigation required if dry spell occurs during flowering or pod-filling stage.",
        "planting": "Sow treated seeds (65-75 kg/ha) with seed drill at 3-4 cm depth with onset of monsoon (June 15 - July 10).",
        "spacing": "45 cm row spacing, 5-7 cm plant spacing.",
        "growth_stages": [
            "Emergence & unifoliate leaf (0 to 10 days)",
            "Vegetative branching (10 to 35 days)",
            "Flowering (R1-R2) (35 to 55 days)",
            "Pod development & seed filling (R3-R6) (55 to 85 days)",
            "Leaf yellowing & physiological maturity (R7-R8) (85 to 105 days)"
        ],
        "fertilizer": "NPK 20:60:40:20 (N:P2O5:K2O:S kg/ha). Soybean fixes own atmospheric nitrogen via root nodule bacteria. Inoculate seeds with Bradyrhizobium japonicum (5g/kg) and PSB (5g/kg) before sowing.",
        "pests": [
            "Girdle Beetle (Obereopsis brevis) — cuts two parallel rings around stem causing wilting above ring.",
            "Tobacco Caterpillar (Spodoptera litura) — defoliates leaves during vegetative stage.",
            "Stem Fly (Melanagromyza sojae) — mines into stem pith of young seedlings."
        ],
        "diseases": [
            "Yellow Mosaic Virus (YMV) — bright yellow patches on leaves transmitted by whiteflies.",
            "Soybean Rust (Phakopsora pachyrhizi) — tiny brown-red pustules on leaf undersides causing rapid defoliation.",
            "Charcoal Rot (Macrophomina phaseolina) — black micro-sclerotia inside split stems during dry hot spell."
        ],
        "prevention": "Use YMV-resistant varieties (e.g. JS 335, JS 93-05, NRC 37). Spray Neem oil (5ml/L) to control whitefly vector. Avoid waterlogging in flat fields by installing broad bed furrows (BBF).",
        "harvesting": "Harvest when 95% of pods turn golden brown, leaves drop off, and seed rattles in pod (moisture 13-15%).",
        "post_harvest": "Thresh at low cylinder speed (350-400 RPM) to prevent seed coat splitting. Store clean seeds at 10-12% moisture."
    },
    "maize": {
        "common_name": "Maize (Corn)",
        "scientific_name": "Zea mays",
        "plant_type": "Annual C4 Cereal Grain",
        "soil": "Deep, fertile, well-drained sandy loam to silt loam soil rich in organic matter. Free from salinity and waterlogging.",
        "pH": "6.0 to 7.2.",
        "climate": "Warm temperate and tropical climate with abundant sunshine.",
        "temperature": "Optimum growing temp: 20°C to 30°C. Germination requires >15°C.",
        "rainfall": "500 mm to 800 mm well-distributed during growth cycle.",
        "irrigation": "Critical irrigation stages: Knee-high stage, Tasseling/Silking (MOST CRITICAL — moisture stress causes pollination failure), and Grain filling (Dough stage).",
        "planting": "Sow certified hybrid seeds (20 kg/ha) on ridges or flat beds 4-5 cm deep during June-July (Kharif) or Oct-Nov (Rabi).",
        "spacing": "60 cm row-to-row, 20 cm plant-to-plant.",
        "growth_stages": [
            "Seedling emergence (0 to 15 days)",
            "Knee-high vegetative phase (15 to 40 days)",
            "Tasseling and silking / pollination (40 to 65 days)",
            "Milking & dough grain development (65 to 90 days)",
            "Black layer formation and maturity (90 to 110 days)"
        ],
        "fertilizer": "NPK 120:60:50 kg/ha with 25 kg/ha Zinc Sulfate. Apply full P, full K, and 33% N as basal. Top-dress remaining Nitrogen in two equal splits at knee-high stage (V6) and tasseling stage (VT).",
        "pests": [
            "Fall Armyworm (Spodoptera frugiperda) — destructive caterpillar feeding in leaf whorls, creates large ragged holes and frass.",
            "Maize Stem Borer (Chilo partellus) — causes 'dead heart' in young plants and pin-holes in leaves.",
            "Corn Earworm (Helicoverpa zea) — feeds on developing kernels at tip of cob."
        ],
        "diseases": [
            "Turcicum / Northern Leaf Blight (Exserohilum turcicum) — long elliptical grayish-green cigar-shaped lesions.",
            "Maydis / Southern Leaf Blight (Bipolaris maydis) — small rectangular tan lesions bounded by veins.",
            "Common Rust (Puccinia sorghi) — small golden-brown powdery pustules on both leaf surfaces."
        ],
        "prevention": "Install pheromone traps for Fall Armyworm monitoring. Apply Metarhizium anisopliae or Bacillus thuringiensis (Bt) in whorls. Seed treatment with Thiamethoxam.",
        "harvesting": "Harvest when husk leaves dry to light straw color, kernel moisture drops to 20-25%, and a black layer forms at base of grain.",
        "post_harvest": "Dry de-husked cobs in sun to 12-14% moisture before shelling with mechanical maize sheller. Store shelled grain in dry pest-proof bins."
    }
}

def get_plant_data(plant_name: str) -> Optional[Dict[str, Any]]:
    """Lookup plant profile by common or scientific name with fuzzy fallback."""
    if not plant_name:
        return None
    
    clean = plant_name.lower().strip()
    
    # Exact or substring match
    for key, data in PLANTS_KNOWLEDGE_BASE.items():
        if key in clean or clean in key:
            return data
        if data["common_name"].lower() in clean or clean in data["common_name"].lower():
            return data
        if data["scientific_name"].lower() in clean:
            return data
            
    # Alias / variant mappings
    aliases = {
        "paddy": "rice",
        "corn": "maize",
        "pepper": "chilli",
        "capsicum": "chilli",
        "bhindi": "okra",
        "cane": "sugarcane",
        "aam": "mango",
        "amba": "mango",
        "kanda": "onion",
        "batata": "potato",
        "aloo": "potato",
        "kapas": "cotton",
        "soyabean": "soybean"
    }
    
    for alias, target in aliases.items():
        if alias in clean and target in PLANTS_KNOWLEDGE_BASE:
            return PLANTS_KNOWLEDGE_BASE[target]
            
    return None

def list_all_plants() -> List[Dict[str, str]]:
    """Return all available plants with scientific names."""
    return [
        {
            "key": k,
            "common_name": v["common_name"],
            "scientific_name": v["scientific_name"],
            "plant_type": v["plant_type"]
        }
        for k, v in PLANTS_KNOWLEDGE_BASE.items()
    ]
