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
    },
    "banana": {
        "common_name": "Banana",
        "scientific_name": "Musa acuminata / Musa balbisiana",
        "plant_type": "Perennial Monocot Giant Herbaceous Crop",
        "soil": "Deep, rich, fertile, well-drained alluvial or clay loam soil rich in organic matter. Soil depth minimum 1 meter. Extremely sensitive to waterlogging and salinity.",
        "pH": "6.0 to 7.5 (optimum 6.5).",
        "climate": "Warm, humid tropical climate with high humidity (>60%) and protection from strong winds.",
        "temperature": "Optimum growing temperature: 25°C to 30°C. Below 15°C growth halts; frost causes severe leaf necrosis.",
        "rainfall": "Requires 1500 mm to 2000 mm rainfall annually or equivalent high-frequency drip irrigation.",
        "irrigation": "Very high water requirement (15-20 liters/plant/day in winter, 25-30 liters/plant/day in summer). Drip irrigation with daily scheduling is recommended. Avoid standing water to prevent root rot.",
        "planting": "Plant healthy sword suckers (1.5-2.0 kg) or tissue culture (TC) plantlets (45-60 days old) in 0.6m x 0.6m x 0.6m pits treated with Carbofuran / Chlorpyrifos and FYM.",
        "spacing": "Grand Naine: 1.8m x 1.8m (3086 plants/ha) or 1.5m x 1.5m. Robusta / Dwarf Cavendish: 1.5m x 1.5m. High density paired row: 1.2m x 1.2m x 2.0m.",
        "growth_stages": [
            "Vegetative phase / shooting of leaves (0 to 6 months)",
            "Shooting / Inflorescence emergence (6 to 8 months)",
            "Bunch emergence and bract opening (8 to 9 months)",
            "Fruit development and finger filling (9 to 11 months)",
            "Bunch maturity and harvesting (11 to 13 months)"
        ],
        "fertilizer": "Grand Naine fertigation schedule: 200g N, 60g P2O5, 300g K2O per plant over 36 weeks. Apply 100% P basal, high N during vegetative phase (weeks 1-20), and switch to high Potassium (K) during bunch emergence and finger filling (weeks 21-36). Foliar spray of Potassium Sulphate (0.5%) on bunch improves finger length and luster.",
        "pests": [
            "Banana Pseudostem Borer (Odoiporus longicollis) — larvae tunnel into pseudostem causing jelly-like exudation and lodging.",
            "Banana Rhizome Weevil (Cosmopolites sordidus) — tunnels inside corm weakening root anchorage.",
            "Banana Aphid (Pentalonia nigronervosa) — vector of destructive Banana Bunchy Top Virus (BBTV)."
        ],
        "diseases": [
            "Sigatoka Leaf Spot (Mycosphaerella musicola / fijiensis) — yellow/brown spindle spots coalescing into leaf blight.",
            "Panama Wilt (Fusarium oxysporum f. sp. cubense / TR4) — vascular wilt, yellowing of lower leaves, longitudinal pseudostem splitting.",
            "Banana Bunchy Top Virus (BBTV) — dark green 'dot-dash' streaks along secondary leaf veins, leaves become narrow, upright, and bunched at apex."
        ],
        "prevention": "Use virus-indexed tissue-cultured plantlets. Desucker regularly leaving only one healthy follower ratoon sucker per mother plant. Cover developing bunches with perforated blue polyethylene sleeves (skirting bags).",
        "harvesting": "Harvest when bunch angles round off, dried floral remnants drop easily, and fingers turn light green (75-80% maturity for export/distant transit; full maturity for local market).",
        "post_harvest": "De-hand bunches with curved knife, wash in alum/chlorinated water tank to remove latex, treat crown with Azoxystrobin (0.1%), pack in corrugated boxes with foam liners, store at 13°C-14°C at 90-95% RH."
    },
    "grape": {
        "common_name": "Grape (Grapevine)",
        "scientific_name": "Vitis vinifera",
        "plant_type": "Perennial Deciduous Woody Vine",
        "soil": "Well-drained sandy loam, gravelly loam, or red sandy soil with good water permeability. High sensitivity to waterlogging, salinity (EC > 1.5 dS/m), and high exchangeable sodium (ESP > 15%).",
        "pH": "6.5 to 7.5.",
        "climate": "Subtropical and Mediterranean dry climate. Requires hot dry summers and cool dry winters without rain during berry maturation to prevent fungal outbreaks.",
        "temperature": "Optimum: 25°C to 35°C during vegetative growth and ripening. Extreme humidity with rain during ripening causes berry cracking and rotting.",
        "rainfall": "500 mm to 700 mm. Strict dry period required from fruit set to harvest.",
        "irrigation": "Drip irrigation based on pan evaporation. Foundation pruning (April): High irrigation (25-30 L/vine/day) for canopy development. Forward fruit pruning (Oct): Regulated deficit irrigation (15-20 L/vine/day) after berry set. Withhold irrigation 8-10 days before harvest to build Brix sugar levels.",
        "planting": "Rooted cuttings grafted onto Dogridge or 110R nematode/salinity resistant rootstocks planted in 1m x 1m x 1m pits.",
        "spacing": "Y-trellis / Bower (Pandal) system: 3.0m row-to-row, 1.8m vine-to-vine.",
        "growth_stages": [
            "April Back Pruning (Foundation pruning for canes)",
            "October Forward Pruning (Fruit bud pruning)",
            "Sprouting and Panicle emergence (Oct-Nov)",
            "Flowering / Cap fall & fruit set (Nov-Dec)",
            "Berry development (4-8mm stage, GA3 thinning) (Dec-Jan)",
            "Veraison (color change / softening) (Jan-Feb)",
            "Harvest maturity (18-20° Brix) (Feb-April)"
        ],
        "fertilizer": "Annual vine nutrition (Bower system): 300g N, 200g P2O5, 400g K2O per vine per year. Apply 70% N and 50% P post-April pruning; apply 30% N, 50% P, and 100% K post-October pruning. Foliar Calcium Chloride (0.3%) and Boron (0.1%) sprays prevent berry cracking and enhance shelf life.",
        "pests": [
            "Grape Thrips (Scirtothrips dorsalis) — scrape berries causing scab-like corky russeting.",
            "Mealybug (Maconellicoccus hirsutus) — infests bunch clusters secreting honeydew and sooty mold.",
            "Flea Beetle (Scelodonta strigicollis) — feeds on sprouting buds in October causing shoot blindness."
        ],
        "diseases": [
            "Downy Mildew (Plasmopara viticola) — yellow oily lesions on upper leaf surface, white downy growth on lower surface.",
            "Powdery Mildew (Uncinula necator) — ash-gray powdery coating on leaves and berries causing berry splitting.",
            "Anthracnose / Bird's Eye Spot (Elsinoe ampelina) — dark sunken circular spots with grey centers on leaves and berries."
        ],
        "prevention": "Prune vines carefully to maintain open, aerated canopy. Dip bunches in GA3 (Gibberellic Acid) at 10-15 ppm at 4mm stage for elongation and thinning. Maintain strict prophylactic spray schedule before rain events.",
        "harvesting": "Harvest when berries develop uniform cultivar color, seed turns dark brown, and TSS reaches 18-20° Brix with acidity 0.5-0.6%. Clip bunches early in morning using grape snips.",
        "post_harvest": "Pre-cool within 4 hours to 0°C to 2°C. Place dual-release SO2 (Sulfur Dioxide) grape guard pads in ventilated boxes to prevent Botrytis gray mold. Store at 0°C with 90-95% RH."
    },
    "pomegranate": {
        "common_name": "Pomegranate",
        "scientific_name": "Punica granatum",
        "plant_type": "Perennial Deciduous/Semi-Evergreen Shrub/Fruit Tree",
        "soil": "Well-drained light to medium black soils, red loamy, or alluvial soils. Tolerates moderate salinity and alkaline conditions up to pH 8.0.",
        "pH": "6.5 to 8.0.",
        "climate": "Semi-arid dry climate with hot dry summers and mild winters. Requires dry weather during flowering and fruit ripening.",
        "temperature": "Optimum: 25°C to 38°C. High sunshine improves fruit rind color and aril sweetness.",
        "rainfall": "500 mm to 700 mm. Heavy rains during fruit ripening cause severe fruit cracking and bacterial blight.",
        "irrigation": "Drip irrigation: 15-20 liters/plant/day during fruit development. Practice 'Bahar treatment' (stress withholding water for 40-50 days) before Hasta (Sept-Oct) or Ambe Bahar (Jan-Feb) to induce synchronous flowering.",
        "planting": "Plant air-layered (goottee) or hardwood cuttings in 0.6m x 0.6m x 0.6m pits during onset of monsoon.",
        "spacing": "4.5m x 3.0m (740 plants/ha) or 4.0m x 3.0m (833 plants/ha).",
        "growth_stages": [
            "Water stress period (Bahar induction)",
            "Pruning & light irrigation resumption",
            "Profuse vegetative flush and flowering",
            "Fruit set and calyx thinning",
            "Fruit enlargement and aril filling",
            "Rind color development & maturity (135-150 days post-bloom)"
        ],
        "fertilizer": "Per bearing tree (5+ years): 625g N, 250g P2O5, 500g K2O along with 30 kg well-rotted FYM. Apply 50% N + full P + 50% K at bahar initiation; apply remaining 50% N and 50% K 45 days after fruit set. Spray Micronutrient mixture (Fe, Zn, B) 0.3% twice during fruit growth.",
        "pests": [
            "Anar Butterfly / Fruit Borer (Deudorix isocrates) — caterpillar bores into fruit making circular entry hole and causing offensive smelling internal rot.",
            "Thrips (Scirtothrips dorsalis) — causes corky scabbing on fruit surface.",
            "Shot Hole Borer (Xylosandrus compactus) — bores into main stem transmitting wilt fungus."
        ],
        "diseases": [
            "Bacterial Blight / Telya (Xanthomonas axonopodis pv. punicae) — water-soaked oily dark spots on leaves, nodal stem cankers, and prominent oily triangular 'Y-shaped' cracked spots on fruits.",
            "Fruit Rot / Anthracnose (Colletotrichum gloeosporioides) — sunken circular brown spots on rind.",
            "Cercospora Leaf Spot (Cercospora punicae) — light brown spots on leaves."
        ],
        "prevention": "Prune infected twigs 5 cm below infection and burn immediately. Bag individual developing fruits with butter paper or non-woven bags to protect against fruit borer and bacterial blight. Follow strict orchard sanitation.",
        "harvesting": "Harvest 135-150 days after flowering when fruit makes a metallic ringing sound on tapping, rind turns crimson red/yellowish pink, and calyx lobes curl inwards.",
        "post_harvest": "Grade by size/weight (Super: >350g, King: 300-350g). Wash in chlorinated water (100 ppm), dry, pack in 3-4 kg boxes. Store at 6°C-7°C with 90-95% RH. Shelf life: 2 months."
    },
    "groundnut": {
        "common_name": "Groundnut (Peanut)",
        "scientific_name": "Arachis hypogaea",
        "plant_type": "Annual Legume Oilseed Crop",
        "soil": "Well-drained loose, friable sandy loam or light red sandy soil rich in calcium and organic matter. Compact heavy clay soils severely restrict peg penetration and pod development.",
        "pH": "6.0 to 7.0.",
        "climate": "Warm, sunny tropical and subtropical climate with frost-free growing season.",
        "temperature": "Optimum: 25°C to 30°C. Temperature below 20°C delays germination and flowering.",
        "rainfall": "500 mm to 700 mm evenly distributed throughout vegetative and pegging stages.",
        "irrigation": "Critical irrigation stages: Flowering (25-30 DAS), Pegging (40-50 DAS — MOST CRITICAL: soil must be loose and moist for gynophore penetration), and Pod development (60-70 DAS). Avoid moisture stress during pegging.",
        "planting": "Sow healthy certified kernels (100-120 kg/ha for bunch type; 80-90 kg/ha for spreading type) treated with Rhizobium leguminosarum + Trichoderma viride.",
        "spacing": "Bunch varieties (e.g. TAG-24, JL-24): 30 cm x 10 cm. Spreading varieties: 45 cm x 15 cm. Sow at 4-5 cm depth.",
        "growth_stages": [
            "Germination & seedling emergence (0 to 10 days)",
            "Vegetative branching (10 to 25 days)",
            "Flowering (25 to 40 days)",
            "Pegging & gynophore soil penetration (40 to 60 days)",
            "Pod formation & seed filling (60 to 90 days)",
            "Pod maturity and harvest (90 to 120 days)"
        ],
        "fertilizer": "NPK 25:50:0 to 25:50:20 kg/ha. CRITICAL: Apply Gypsum (Calcium Sulfate) @ 400-500 kg/ha at flowering/pegging stage (35-40 DAS) directly to the root zone. Calcium is essential for pod shell hardening and preventing 'pop' (empty seedless pods), while Sulfur boosts oil synthesis.",
        "pests": [
            "Leaf Miner (Aproaerema modicella) — larvae mine inside leaves making blisters and webbing leaves together.",
            "White Grub (Holotrichia consanguinea) — subterranean grubs feed on roots causing sudden plant wilting in patches.",
            "Aphids & Thrips — transmit Peanut Bud Necrosis Virus (PBNV)."
        ],
        "diseases": [
            "Tikka Disease / Leaf Spot (Cercospora arachidicola - Early Tikka; Cercosporidium personatum - Late Tikka) — circular dark brown spots surrounded by yellow halos causing severe defoliation.",
            "Rust (Puccinia arachidis) — orange-brown powdery pustules on lower leaf surface.",
            "Collar Rot (Aspergillus niger) — rotting of collar region near soil level leading to seedling death."
        ],
        "prevention": "Rotate with non-host cereals (pearl millet, sorghum). Deep summer plowing to destroy white grub pupae. Seed treatment with Thiram + Carbendazim (2g/kg) or Trichoderma (10g/kg).",
        "harvesting": "Harvest when 75-80% of pods show internal shell blackening/browning, foliage turns yellowish, and kernels separate freely from shell.",
        "post_harvest": "Dry uprooted vines in field for 2-3 days, strip pods, and sun-dry pods on clean tarpaulins until moisture drops below 8-9% to prevent toxic Aflatoxin (Aspergillus flavus) development during storage."
    },
    "chickpea": {
        "common_name": "Chickpea (Gram / Bengal Gram)",
        "scientific_name": "Cicer arietinum",
        "plant_type": "Annual Rabi Legume Pulse Crop",
        "soil": "Well-drained deep clay loam, silt loam, or black cotton soil with good water retention capacity. Highly sensitive to waterlogging, poor aeration, and soil salinity.",
        "pH": "6.5 to 7.8.",
        "climate": "Cool, dry winter climate during vegetative growth, followed by warm sunny weather during seed ripening. Strict requirement for frost-free conditions during flowering.",
        "temperature": "Optimum: 18°C to 26°C. High temperature (>32°C) or heavy fog/cloudy weather at flowering causes severe flower drop.",
        "rainfall": "400 mm to 600 mm. Highly drought-tolerant pulse grown predominantly under residual soil moisture in Rabi.",
        "irrigation": "Low water requirement. 1 to 2 protective irrigations: 1st at pre-flowering branching stage (30-35 DAS), and 2nd at early pod development stage (60-65 DAS). NEVER irrigate during peak flowering as it promotes excessive vegetative growth and flower drop.",
        "planting": "Sow certified seeds (Desi: 65-75 kg/ha; Kabuli: 100-120 kg/ha) treated with Rhizobium and PSB culture at 6-8 cm depth during October to mid-November.",
        "spacing": "Desi types: 30 cm x 10 cm. Kabuli types: 45 cm x 10 cm.",
        "growth_stages": [
            "Emergence & seedling stage (0 to 15 days)",
            "Vegetative branching (15 to 40 days)",
            "Nipping / apical shoot pinching (30-35 days for lateral branching)",
            "Flower initiation and blooming (40 to 65 days)",
            "Pod set & green seed filling (65 to 90 days)",
            "Pod yellowing and maturity (90 to 115 days)"
        ],
        "fertilizer": "NPK 20:40:20 kg/ha with 20 kg/ha elemental Sulfur as basal. Being a nodulated legume, it fixes its own Nitrogen (60-80% of requirement). Foliar spray of 2% Urea or 1% 19:19:19 at pod filling stage boosts grain size and yield.",
        "pests": [
            "Gram Pod Borer (Helicoverpa armigera) — devastating green/brown caterpillar that bores into pods and eats developing seeds.",
            "Cutworm (Agrotis ipsilon) — cuts young seedlings at soil surface during night."
        ],
        "diseases": [
            "Fusarium Wilt (Fusarium oxysporum f. sp. ciceris) — drooping of upper leaves, vascular browning in split stem root, rapid plant death in patches.",
            "Dry Root Rot (Rhizoctonia bataticola) — roots become brittle and dark black, plant dries up prematurely under moisture stress.",
            "Ascochyta Blight (Ascochyta rabiei) — circular sunken brown spots with concentric pycnidia on leaves and pods."
        ],
        "prevention": "Deep summer plowing. Crop rotation with wheat, mustard, or sorghum. Practice 'Nipping' (pinching off apical top 2-3 cm shoots at 30-35 DAS) to encourage profuse lateral flowering branches.",
        "harvesting": "Harvest when 90% of pods turn golden-yellow/brown, leaves dry and drop off, and seeds rattle inside pods.",
        "post_harvest": "Sun-dry harvested plants on threshing floor for 3-4 days. Thresh with tractor/bullock or pulse thresher. Dry seeds to 9-10% moisture before storing in clean airtight bags with neem leaves."
    },
    "papaya": {
        "common_name": "Papaya",
        "scientific_name": "Carica papaya",
        "plant_type": "Fast-Growing Semi-Woody Herbaceous Fruit Tree",
        "soil": "Rich, deep, fertile sandy loam or alluvial soil with exceptional drainage. Minimum soil depth 1 meter. Extremely susceptible to 'wet feet' (waterlogging causes stem rot within 24-48 hours).",
        "pH": "6.0 to 7.0.",
        "climate": "Warm, sunny tropical and subtropical climate free from frost and strong winds.",
        "temperature": "Optimum: 25°C to 35°C. Temperatures below 10°C stunt fruit growth and affect sugar accumulation.",
        "rainfall": "1000 mm to 1500 mm well-distributed.",
        "irrigation": "Irrigate through drip or ring basin method (never allow water to touch the main stem trunk). Irrigate every 5-6 days in winter and 2-3 days in summer. Maintain consistent soil moisture.",
        "planting": "Raise seedlings in polybags. Transplant 45-day-old vigorous seedlings in 0.5m x 0.5m x 0.5m pits during June-Sept. For dioecious varieties, plant 2-3 seedlings per pit and rogue out excess male plants at flowering (maintain 1 male per 10 female trees). Gynodioecious varieties (Red Lady 786, Taiwan 786) are bisexual/hermaphrodite and need 1 seedling per pit.",
        "spacing": "2.0m x 2.0m (2500 plants/ha) or 1.8m x 1.8m.",
        "growth_stages": [
            "Seedling & vegetative establishment (0 to 3 months)",
            "Flower bud initiation and sex determination (3 to 4 months)",
            "Fruit set and column enlargement (4 to 6 months)",
            "Fruit filling and ripening (7 to 10 months)",
            "Continuous harvesting phase (10 to 24 months)"
        ],
        "fertilizer": "Per plant per year: 250g N, 250g P2O5, 500g K2O applied in 6 bimonthly splits. Apply Borax (5g/plant) to prevent bumpy deformed fruits. Zinc Sulfate (0.5%) foliar spray improves chlorophyll and fruit size.",
        "pests": [
            "Aphids (Aphis gossypii) — primary sap-sucking vector for Papaya Ringspot Virus (PRSV).",
            "Red Spider Mites (Tetranychus cinnabarinus) — web under leaf surfaces causing yellow speckling.",
            "Whitefly & Mealybug — suck sap and secrete honeydew causing sooty mold."
        ],
        "diseases": [
            "Papaya Ringspot Virus (PRSV) — mosaic mottling on leaves, shoestring distortion, water-soaked dark green rings on fruits and stems.",
            "Damping-Off & Foot Rot / Collar Rot (Pythium aphanidermatum / Phytophthora nicotianae) — rotting of stem at soil level causing tree collapse.",
            "Anthracnose (Colletotrichum gloeosporioides) — sunken circular brown spots on ripening fruit."
        ],
        "prevention": "Raise border barrier crops of 3-4 rows of maize or sorghum to block aphid vectors. Build 20 cm elevated mounds/ridges around trunks to prevent collar contact with irrigation water. Spray systemic insecticides and Neem oil proactively.",
        "harvesting": "Harvest when fruit skin color changes from dark green to slight yellow at the blossom apex (color break stage). Twist gently or cut with sharp knife retaining 0.5 cm stalk.",
        "post_harvest": "Wash, treat with Carbendazim (0.1%) dip, wrap in paper, pack in foam-cushioned ventilated cartons. Store at 10°C-12°C with 85-90% RH."
    },
    "turmeric": {
        "common_name": "Turmeric (Haldi)",
        "scientific_name": "Curcuma longa",
        "plant_type": "Perennial Rhizomatous Cash & Spice Crop",
        "soil": "Deep, fertile, well-drained loamy, sandy loam, or alluvial soil rich in humus and organic matter. Soil must be friable to allow unhindered underground rhizome expansion.",
        "pH": "6.0 to 7.5.",
        "climate": "Warm, humid tropical climate with abundant sunshine and warm temperatures during rhizome development.",
        "temperature": "Optimum: 20°C to 35°C. High humidity (70-90%) accelerates vegetative tillering.",
        "rainfall": "1500 mm to 2000 mm or equivalent irrigation.",
        "irrigation": "Irrigate immediately after planting. Irrigate every 6-8 days in medium soils. Critical periods: Rhizome initiation (60-90 DAS) and Rhizome development/bulking (120-180 DAS). Withhold irrigation 15-20 days before harvest.",
        "planting": "Plant healthy mother rhizomes or primary finger rhizomes (35-45g weight, 20-25 q/ha) treated with Quinalphos + Mancozeb on raised beds or broad bed furrows (BBF) in May-June.",
        "spacing": "Raised beds: 30 cm row-to-row, 20 cm plant-to-plant on 1.2m wide beds.",
        "growth_stages": [
            "Sprouting & vegetative emergence (0 to 45 days)",
            "Active tillering and pseudostem development (45 to 90 days)",
            "Rhizome initiation (90 to 120 days)",
            "Rhizome bulking & curcumin accumulation (120 to 210 days)",
            "Foliage yellowing, drying, and harvest maturity (210 to 270 days)"
        ],
        "fertilizer": "NPK 150:60:150 kg/ha along with 25-30 tonnes/ha FYM. Apply full P as basal. Apply Nitrogen and Potassium in 3 splits at 30, 60, and 90 DAS along with earthing up. Apply Ferrous Sulfate (15 kg/ha) and Zinc Sulfate (25 kg/ha) to prevent interveinal chlorosis.",
        "pests": [
            "Shoot Borer (Conogethes punctiferalis) — caterpillar bores into pseudostem causing central leaf drying ('dead heart').",
            "Rhizome Scale (Aspidiella hartii) — white encrustations on stored and growing rhizomes.",
            "Thrips (Panchaetothrips indicus) — leaf rolling and silvering."
        ],
        "diseases": [
            "Rhizome Rot / Soft Rot (Pythium aphanidermatum) — water-soaked soft rotting of rhizomes with foul smell, foliage turns yellow and collapses.",
            "Leaf Spot (Colletotrichum capsici) — brown elliptical spots with grey centers on leaves.",
            "Leaf Blotch (Taphrina maculans) — reddish-brown small spots on both leaf surfaces."
        ],
        "prevention": "Provide thick organic mulch (green leaves / paddy straw @ 10-12 t/ha) immediately after planting and at 45 & 90 DAS for moisture conservation and weed control. Soil drenching with Trichoderma harzianum or Copper Oxychloride for rhizome rot prevention.",
        "harvesting": "Harvest when leaves turn yellow, dry, and wither completely (7.5 to 9 months after planting). Dig up rhizome clumps carefully without bruising using tractor diggers or manual spades.",
        "post_harvest": "Separate mother rhizomes from finger rhizomes. Boil fingers in water for 45-60 minutes until soft (curcuma curing), sun-dry for 10-15 days to 8-10% moisture, and polish mechanically in polishing drums to impart bright yellow color."
    },
    "apple": {
        "common_name": "Apple",
        "scientific_name": "Malus domestica",
        "plant_type": "Temperate Deciduous Fruit Tree",
        "soil": "Deep, well-drained, fertile loamy soil rich in organic matter (depth >1.5m). Free from rocky hardpans and water stagnation.",
        "pH": "5.5 to 6.8 (slightly acidic).",
        "climate": "Cool temperate climate with distinct winter chilling (requires 800-1200 chilling hours below 7°C for breaking bud dormancy).",
        "temperature": "Optimum: 21°C to 24°C during growing season. Severe frost during blossom period causes near-total fruit drop.",
        "rainfall": "1000 mm to 1250 mm evenly distributed.",
        "irrigation": "Critical irrigation stages: Sprouting to fruit set, fruit enlargement, and 20 days prior to harvest. Drip irrigation at 20-25 L/tree/day during fruit swelling.",
        "planting": "Plant grafted 1-year-old whips (on M9 / MM106 rootstocks) in 1m x 1m x 1m pits filled with topsoil, 40kg FYM, and 500g SSP in Dec-Feb.",
        "spacing": "Standard: 6m x 6m (278 trees/ha). High Density (HDP on M9): 3m x 1m (3333 trees/ha) with trellis wire support.",
        "growth_stages": [
            "Winter bud dormancy (Nov-Feb)",
            "Silver tip & green tip (March)",
            "Pink bud & full bloom (April)",
            "Petal fall and fruit set (May)",
            "Fruit enlargement and cell expansion (June-July)",
            "Color development and harvesting (Aug-Oct)"
        ],
        "fertilizer": "Per mature bearing tree: 700g N, 350g P2O5, 700g K2O along with 40-50 kg FYM. Apply full P, full K, and 50% N in winter; top-dress remaining 50% N post-petal fall. Foliar sprays of 0.2% Borax and 0.4% Calcium Chloride prevent bitter pit and corking.",
        "pests": [
            "San Jose Scale (Quadraspidiotus perniciosus) — ash-gray encrustations on twigs and red rings on fruits.",
            "Woolly Apple Aphid (Eriosoma lanigerum) — white cottony masses on branches and galls on roots.",
            "Codling Moth (Cydia pomonella) — bores into fruit core leaving frass at calyx."
        ],
        "diseases": [
            "Apple Scab (Venturia inaequalis) — olive-green velvety spots turning black and corky on leaves and fruits.",
            "Powdery Mildew (Podosphaera leucotricha) — white powdery growth on terminal shoots causing rosette distortion.",
            "Alternaria Leaf Blotch (Alternaria mali) — circular brown spots with purple margins on leaves causing summer defoliation."
        ],
        "prevention": "Spray dormant spray oil (Horticultural mineral oil @ 2%) in January to kill overwintering scale insects. Destroy fallen leaves with 5% urea spray in autumn to disrupt apple scab pseudothecia.",
        "harvesting": "Harvest when ground color changes from green to yellow, starch conversion index reaches 3-4, and fruit separates easily with upward twist.",
        "post_harvest": "Pre-cool immediately to 4°C. Treat with 1-MCP (1 ppm) for long storage. Store in Controlled Atmosphere (CA) at 0°C to 1°C with 1.5% O2 and 1-2% CO2 with 90-95% RH. Storage life: 6-8 months."
    },
    "guava": {
        "common_name": "Guava (Amrood / Peru)",
        "scientific_name": "Psidium guajava",
        "plant_type": "Subtropical / Tropical Evergreen Fruit Tree",
        "soil": "Hardy crop; performs well on deep alluvial, red loamy, or medium black soils. Tolerates moderate salinity and sodicity up to pH 8.5.",
        "pH": "6.0 to 8.2.",
        "climate": "Tropical and subtropical climate. Hot summers and cool frost-free winters promote high sweetness and aroma.",
        "temperature": "Optimum: 23°C to 28°C.",
        "rainfall": "1000 mm to 2000 mm; highly drought tolerant once established.",
        "irrigation": "Irrigate every 8-10 days in winter, 4-6 days in summer. Drip irrigation saves 40% water. Practice Bahar water withholding in May to induce high-quality winter crop (Mrig Bahar).",
        "planting": "Plant air-layered or grafted saplings (L-49 / Sardar, Allahabad Safeda, Taiwan Pink) in 0.75m x 0.75m x 0.75m pits in July-August.",
        "spacing": "Traditional: 6m x 6m (278 plants/ha). High Density / Meadow Orchard: 2m x 1m (5000 plants/ha) or 3m x 2m with regular canopy topping.",
        "growth_stages": [
            "Vegetative shoot pruning & bahar initiation (May)",
            "Sprouting and flower bud emergence (June-July)",
            "Fruit set (pea to marble stage) (July-August)",
            "Fruit development and bagging (Sept-Oct)",
            "Winter harvest maturity (Nov-Jan)"
        ],
        "fertilizer": "Per bearing tree (5+ years): 500g N, 200g P2O5, 500g K2O with 25 kg FYM. Apply 50% N + full P + 50% K in June; apply remaining 50% N and 50% K in September. Spray Zinc Sulfate (0.4%) + Boron (0.2%) during flowering.",
        "pests": [
            "Fruit Fly (Bactrocera correcta) — oviposits in ripening fruit causing internal maggots and soft rotting.",
            "Mealybug & Tea Mosquito Bug — suck sap from tender shoots causing corky scab on young fruits."
        ],
        "diseases": [
            "Guava Wilt (Fusarium oxysporum f. sp. psidii) — yellowing and drooping of leaves, severe root necrosis, rapid tree death in alkaline soils.",
            "Anthracnose / Fruit Canker (Pestalotiopsis psidii / Colletotrichum) — brown circular spots with raised corky margins on fruit."
        ],
        "prevention": "Prune Meadow Orchard trees at 60 cm height annually. Bag individual green fruits with non-woven / foam bags 40 days after fruit set. Drench root zone with Trichoderma harzianum (25g/tree) + Pseudomonas fluorescens to prevent Fusarium wilt.",
        "harvesting": "Harvest when fruit skin color transitions from dark green to light yellowish-green. Harvest with stalks intact using hand clippers.",
        "post_harvest": "Grade by size (A: >200g, B: 150-200g). Store at 8°C-10°C with 85-90% RH. Shelf life: 2-3 weeks."
    },
    "pigeonpea": {
        "common_name": "Pigeonpea (Red Gram / Tur / Arhar)",
        "scientific_name": "Cajanus cajan",
        "plant_type": "Semi-Perennial / Annual Deep-Rooted Legume Pulse",
        "soil": "Deep, well-drained medium black cotton soils, clay loam, or red sandy loam. Extremely sensitive to waterlogging at all growth stages.",
        "pH": "6.5 to 7.8.",
        "climate": "Warm tropical climate with sunny conditions during vegetative phase and dry sunny weather during pod filling and maturity.",
        "temperature": "Optimum: 25°C to 35°C. Freezes easily below 10°C.",
        "rainfall": "600 mm to 1000 mm. Highly drought-tolerant due to deep taproot system.",
        "irrigation": "Protective irrigations at (1) Flower bud initiation (70-80 DAS) and (2) Pod filling stage (100-110 DAS) boost seed yield by 40-50%.",
        "planting": "Sow certified seeds (12-15 kg/ha sole; 5-7 kg/ha intercropped with soybean/cotton in 4:2 or 6:1 ratio) treated with Rhizobium + Trichoderma.",
        "spacing": "Sole crop (Wilt-resistant varieties like BDN-711, BSMR-736, Maruti): 90 cm x 20 cm or 120 cm x 30 cm on broad bed furrows (BBF).",
        "growth_stages": [
            "Emergence & slow early vegetative phase (0 to 45 days)",
            "Active branching & canopy expansion (45 to 90 days)",
            "Profuse flower bud initiation (90 to 120 days)",
            "Pod setting & green grain filling (120 to 150 days)",
            "Pod browning, leaf drying, and harvest maturity (150 to 180 days)"
        ],
        "fertilizer": "NPK 25:50:0 kg/ha along with 20 kg/ha Sulfur as basal. Fixes up to 40 kg N/ha into soil. Foliar spray of 2% DAP or 1% 19:19:19 + 0.2% Borax at 50% flowering enhances pod set and reduces flower drop.",
        "pests": [
            "Gram Pod Borer (Helicoverpa armigera) — feeds on flower buds and chews circular holes in pods.",
            "Pod Fly (Melanagromyza obtusa) — maggot feeds invisibly inside grain causing damaged unmarketable seeds.",
            "Plume Moth (Exelastis atomosa) — feeds on flower petals and tender pods."
        ],
        "diseases": [
            "Fusarium Wilt (Fusarium udum) — purple-black streak on stem xylem, unilateral branch drooping and death.",
            "Sterility Mosaic Disease (SMD / Pigeonpea green plague) — transmitted by Eriophyid mite (Aceria cajani); bushy vegetative growth, pale mosaic leaves, complete absence of flowers/pods.",
            "Phytophthora Stem Blight (Phytophthora cajani) — water-soaked brown lesions on main stem causing stem breaking."
        ],
        "prevention": "Grow SMD & wilt-resistant cultivars (BSMR-736, BDN-711, ICPL-87119). Spray Fenazaquin 10% EC (1 ml/L) or Wettable Sulfur (2.5 g/L) to control vector mites. Install 10 pheromone traps/ha for Helicoverpa.",
        "harvesting": "Harvest when 80-85% of pods turn dark brown/straw-colored and rattle when shaken.",
        "post_harvest": "Sun-dry plants for 3-5 days, thresh with pulse thresher, dry seeds to 9-10% moisture before bagging with neem leaf layers."
    },
    "brinjal": {
        "common_name": "Brinjal (Eggplant / Aubergine)",
        "scientific_name": "Solanum melongena",
        "plant_type": "Warm-Season Solanaceous Vegetable",
        "soil": "Deep, fertile, well-drained sandy loam to clay loam rich in organic matter. Free from root-knot nematode infestation.",
        "pH": "6.0 to 7.0.",
        "climate": "Warm tropical climate with extended frost-free sunny period.",
        "temperature": "Optimum: 22°C to 30°C.",
        "rainfall": "Requires 600 mm to 1000 mm or regular drip irrigation.",
        "irrigation": "Irrigate every 3-4 days in summer, 6-8 days in winter. Moisture stress at fruit set causes fruit drop and bitterness.",
        "planting": "Transplant 30-35 day-old sturdy seedlings (300-400 g seed/ha) in raised beds during Kharif (June-July), Rabi (Sept-Oct), or Summer (Jan-Feb).",
        "spacing": "Hybrids: 90 cm x 60 cm or 75 cm x 75 cm.",
        "growth_stages": [
            "Nursery & transplanting (0 to 35 days)",
            "Vegetative branching (35 to 60 days)",
            "Continuous flowering and fruit set (60 to 120 days)",
            "Multiple harvest picking cycles (75 to 150 days)"
        ],
        "fertilizer": "NPK 100:50:50 kg/ha with 25 t/ha FYM. Apply 50% N + full P + full K as basal. Top-dress remaining Nitrogen in 2 equal splits at 30 and 60 days after transplanting.",
        "pests": [
            "Shoot & Fruit Borer (Leucinodes orbonalis) — caterpillar bores into growing shoots causing wilting ('dead hearts') and bores into fruits leaving frass-filled holes.",
            "Jassids & Whiteflies — suck sap causing leaf curl, hopper burn, and transmission of Little Leaf phytoplasma.",
            "Epilachna Beetle — grubs skeletonize leaves leaving lace-like appearance."
        ],
        "diseases": [
            "Phomopsis Blight & Fruit Rot (Phomopsis vexans) — circular dark brown spots with concentric pycnidia on leaves and soft brown rotting of fruits.",
            "Little Leaf of Brinjal (Phytoplasma) — transmitted by leafhoppers (Hishimonus phycitis); leaves become extremely small, narrow, soft, bushy with zero fruit set.",
            "Damping-Off & Collar Rot (Pythium / Rhizoctonia) — seedling collapse at nursery level."
        ],
        "prevention": "Clip and destroy wilted shoot tips weekly along with inside larvae. Install 15-20 pheromone traps (Lucinlure)/ha. Spray Emamectin Benzoate 5% SG (0.4 g/L) or Chlorantraniliprole 18.5% SC (0.3 ml/L) for borer control. Rogue out Little Leaf affected plants immediately.",
        "harvesting": "Harvest when fruits attain full cultivar size and bright glossy color before seeds harden and flesh turns spongy.",
        "post_harvest": "Wipe with clean soft cloth, grade by size and color, pack in ventilated CFB boxes. Store at 10°C-12°C with 85-90% RH. Shelf life: 7-10 days."
    },
    "garlic": {
        "common_name": "Garlic (Lasun / Lahsun)",
        "scientific_name": "Allium sativum",
        "plant_type": "Rabi Bulbous Cash Crop / Spice",
        "soil": "Fertile, loose, friable, well-drained sandy loam or silt loam rich in organic matter. Compact heavy clay soils cause deformed, undersized, discolored bulbs.",
        "pH": "6.0 to 7.5.",
        "climate": "Cool dry winter climate during bulb initiation and vegetative phase, followed by warm sunny dry weather during bulb maturity.",
        "temperature": "Optimum vegetative: 13°C to 24°C; Bulb development requires 20°C to 28°C with >10-12 hours photoperiod.",
        "rainfall": "Low to medium rainfall (350-500 mm). High humidity promotes foliar blight.",
        "irrigation": "Shallow-rooted crop requiring frequent light irrigations (every 6-8 days in medium soils). Stop irrigation strictly 10-15 days before harvest to allow outer wrapper scales to dry and cure.",
        "planting": "Plant healthy, bold, disease-free cloves from outer rings of bulbs (500-600 kg cloves/ha) vertically with root end pointing downwards at 2-3 cm depth in October-November.",
        "spacing": "15 cm row-to-row, 10 cm clove-to-clove on flat or raised beds.",
        "growth_stages": [
            "Sprouting & emergence (0 to 15 days)",
            "Vegetative leaf production (15 to 60 days)",
            "Bulb initiation & clove differentiation (60 to 90 days)",
            "Bulb enlargement & allicin accumulation (90 to 125 days)",
            "Top leaf yellowing, neck fall, and harvest maturity (125 to 140 days)"
        ],
        "fertilizer": "NPK 100:50:50 kg/ha with 30-40 kg/ha elemental Sulfur and 20 tonnes FYM. Sulfur is critical for garlic pungency and allicin synthesis. Apply full P, full K, full S, and 50% N at planting. Top-dress remaining Nitrogen in 2 splits at 30 and 45 DAS. Avoid applying Nitrogen after 60 DAS to prevent splitting of bulbs.",
        "pests": [
            "Thrips (Thrips tabaci) — scrape leaves causing silvery white streaks, leaf curling, and distortion.",
            "Mites & Maggots — attack roots and stored bulbs."
        ],
        "diseases": [
            "Purple Blotch (Alternaria porri) — purplish-brown sunken lesions on leaves causing premature foliage drying.",
            "Stemphylium Leaf Blight (Stemphylium vesicarium) — small yellow to orange flecks expanding into elongated patches.",
            "Basal Rot / Bulb Rot (Fusarium oxysporum) — rotting of roots and basal plate with white mycelial growth."
        ],
        "prevention": "Seed clove treatment with Carbendazim + Mancozeb (2g/kg). Spray Mancozeb 75% WP (2.5 g/L) or Tebuconazole 25.9% EC (1 ml/L) mixed with sticking agent. Install blue sticky traps for thrips monitoring.",
        "harvesting": "Harvest when 60-70% of tops turn yellow, dry, and collapse (neck fall stage). Uproot plants carefully without bruising bulbs.",
        "post_harvest": "Field cure under shade with leaves intact for 4-6 days (windrow method) until neck constricts tightly. Cut pseudo-stems leaving 2.5 cm neck. Store in dry, well-ventilated slatted wooden crates or mesh bags. Storage life: 6-8 months."
    },
    "watermelon": {
        "common_name": "Watermelon (Tarbuj / Kalingad)",
        "scientific_name": "Citrullus lanatus",
        "plant_type": "Warm-Season Annual Cucurbitaceous Vine",
        "soil": "Deep, fertile, well-drained sandy loam, alluvial, or riverbed soils rich in organic matter. Highly sensitive to waterlogging and soil compaction.",
        "pH": "6.0 to 7.0.",
        "climate": "Warm, dry sunny climate with long days and high sunshine hours. Excess rainfall during fruit development causes fungal foliar blights and reduces sweetness.",
        "temperature": "Optimum germination: 25°C to 30°C. Optimum vegetative & fruit growth: 28°C to 35°C.",
        "rainfall": "Low rainfall; grown predominantly with drip irrigation and silver-black plastic mulch.",
        "irrigation": "Irrigate through drip lines daily. Critical stages: Vine running, flowering, and fruit enlargement. Reduce irrigation 7-10 days before harvest to concentrate sugars (Brix >11-12°).",
        "planting": "Sow certified hybrid seeds (Sugar Baby, Max, Black Star @ 1.5-2.0 kg/ha) on raised beds covered with 25-micron silver-black plastic mulch in Dec-Feb.",
        "spacing": "Raised beds 2.0m apart; 45-60 cm plant-to-plant on beds with inline drip tubing.",
        "growth_stages": [
            "Germination & 4-leaf stage (0 to 15 days)",
            "Vine running and lateral branching (15 to 40 days)",
            "Male and female flowering / bee pollination (40 to 55 days)",
            "Fruit development & rind expansion (55 to 80 days)",
            "Maturity and harvest (80 to 95 days)"
        ],
        "fertilizer": "NPK 150:80:120 kg/ha fertigated through drip lines over 10 weeks. High Phosphorus at planting, balanced NPK during vine growth, and high Potassium (0:0:50 @ 5-7 kg/ha/week) during fruit swelling. Foliar Calcium Nitrate (4g/L) and Borax (1g/L) prevent blossom end rot and fruit cracking.",
        "pests": [
            "Fruit Fly (Bactrocera cucurbitae) — punctures young ovaries and developing fruits causing fruit curvature, rotting, and drop.",
            "Red Pumpkin Beetle (Aulacophora foveicollis) — feeds voraciously on cotyledons and leaves of young seedlings.",
            "Aphids & Thrips — transmit Watermelon Mosaic Virus (WMV)."
        ],
        "diseases": [
            "Downy Mildew (Pseudoperonospora cubensis) — angular bright yellow spots bounded by veins on upper leaf surface, purplish mold beneath.",
            "Powdery Mildew (Podosphaera xanthii) — white talc-like patches on leaves and stems.",
            "Fusarium Wilt & Gummy Stem Blight — sudden vine collapse with amber-colored gummy exudation at collar region."
        ],
        "prevention": "Install 15 cue-lure fruit fly traps per hectare. Use silver-black mulch to repel aphids and thrips. Avoid overhead watering.",
        "harvesting": "Harvest when the tendril nearest to fruit stem dries completely to brown wire, the ground spot turns creamy yellow, and the fruit gives a dull hollow thud sound when tapped with knuckles.",
        "post_harvest": "Harvest early in morning with 2 cm stem intact. Do not stack higher than 4-5 layers in transit. Store at 10°C-15°C with 85-90% RH. Shelf life: 2-3 weeks."
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
        "rice": "rice",
        "corn": "maize",
        "maize": "maize",
        "pepper": "chilli",
        "capsicum": "chilli",
        "mirchi": "chilli",
        "bhindi": "okra",
        "okra": "okra",
        "cane": "sugarcane",
        "sugarcane": "sugarcane",
        "aam": "mango",
        "amba": "mango",
        "mango": "mango",
        "kanda": "onion",
        "pyaz": "onion",
        "onion": "onion",
        "batata": "potato",
        "aloo": "potato",
        "potato": "potato",
        "kapas": "cotton",
        "cotton": "cotton",
        "soyabean": "soybean",
        "soybean": "soybean",
        "kela": "banana",
        "keli": "banana",
        "banana": "banana",
        "draksh": "grape",
        "draksha": "grape",
        "grapes": "grape",
        "grape": "grape",
        "angur": "grape",
        "dalimb": "pomegranate",
        "anar": "pomegranate",
        "pomegranate": "pomegranate",
        "bhuimug": "groundnut",
        "mungfali": "groundnut",
        "peanut": "groundnut",
        "groundnut": "groundnut",
        "chana": "chickpea",
        "harbara": "chickpea",
        "gram": "chickpea",
        "chickpea": "chickpea",
        "papai": "papaya",
        "papita": "papaya",
        "papaya": "papaya",
        "haldi": "turmeric",
        "halad": "turmeric",
        "turmeric": "turmeric",
        "apple": "apple",
        "safarchand": "apple",
        "guava": "guava",
        "amrood": "guava",
        "peru": "guava",
        "pigeonpea": "pigeonpea",
        "tur": "pigeonpea",
        "arhar": "pigeonpea",
        "toor": "pigeonpea",
        "brinjal": "brinjal",
        "eggplant": "brinjal",
        "baingan": "brinjal",
        "vangi": "brinjal",
        "garlic": "garlic",
        "lasun": "garlic",
        "lahsun": "garlic",
        "watermelon": "watermelon",
        "tarbuj": "watermelon",
        "kalingad": "watermelon"
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
