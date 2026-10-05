"""
AgroScan AI — Agricultural Intent & Entity Classification Service
Classifies user queries into 25+ agricultural domains, extracts botanical/pathological entities,
and resolves plant and disease context across multi-turn sessions.
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from app.knowledge.plants_data import PLANTS_KNOWLEDGE_BASE, get_plant_data
from app.knowledge.diseases_data import DISEASES_KNOWLEDGE_BASE, get_disease_data

class AgriculturalIntent:
    SOIL = "SOIL"
    IRRIGATION = "IRRIGATION"
    FERTILIZER = "FERTILIZER"
    NUTRITION = "NUTRITION"
    HARVESTING = "HARVESTING"
    PLANTING = "PLANTING"
    GROWTH_STAGE = "GROWTH_STAGE"
    DISEASE_SYMPTOMS = "DISEASE_SYMPTOMS"
    DISEASE_CAUSE = "DISEASE_CAUSE"
    DISEASE_PREVENTION = "DISEASE_PREVENTION"
    DISEASE_TREATMENT = "DISEASE_TREATMENT"
    DISEASE_TRANSMISSION = "DISEASE_TRANSMISSION"
    DISEASE_IDENTIFICATION = "DISEASE_IDENTIFICATION"
    DISEASE_EXPLANATION = "DISEASE_EXPLANATION"
    PLANT_IDENTIFICATION = "PLANT_IDENTIFICATION"
    PEST = "PEST"
    PEST_MANAGEMENT = "PEST_MANAGEMENT"
    WEATHER = "WEATHER"
    WEATHER_DISEASE_RISK = "WEATHER_DISEASE_RISK"
    RAINFALL_IMPACT = "RAINFALL_IMPACT"
    HUMIDITY_IMPACT = "HUMIDITY_IMPACT"
    TEMPERATURE_IMPACT = "TEMPERATURE_IMPACT"
    LOCATION_ADVICE = "LOCATION_ADVICE"
    REGIONAL_SUITABILITY = "REGIONAL_SUITABILITY"
    SCAN_EXPLANATION = "SCAN_EXPLANATION"
    CONFIDENCE_EXPLANATION = "CONFIDENCE_EXPLANATION"
    IMAGE_QUERY = "IMAGE_QUERY"
    CROP_MANAGEMENT = "CROP_MANAGEMENT"
    GENERAL_AGRICULTURE = "GENERAL_AGRICULTURE"
    SAFETY_ADVICE = "SAFETY_ADVICE"
    CLARIFICATION_NEEDED = "CLARIFICATION_NEEDED"
    GENERAL = "GENERAL"

class IntentService:
    """Classifies user queries into domain-specific agricultural intents and entities."""

    INTENT_PATTERNS = [
        # Explicit Disease Identification
        (
            AgriculturalIntent.DISEASE_IDENTIFICATION,
            [
                r"\b(?:what disease|which disease|identify disease|name the disease|what infection|diagnose|diagnosis|disease does my)\b",
                r"(?:कोणता रोग|काय रोग|रोगाचे नाव|रोग कोणता|रोगाची ओळख|रोगाचे निदान)"
            ]
        ),

        # Scan & Image Explanation
        (
            AgriculturalIntent.SCAN_EXPLANATION,
            [
                r"\b(?:explain|tell me about|understand|details of|summary of).*(?:scan|result|prediction|detection|analysis)\b",
                r"\bexplain my scan\b",
                r"(?:स्कॅन|निकाल|तपासणी).*(?:समजावून सांगा|स्पष्टीकरण|सांगा)"
            ]
        ),
        (
            AgriculturalIntent.CONFIDENCE_EXPLANATION,
            [
                r"\b(?:confidence|accuracy|sure|probability|certainty)\b",
                r"(?:अचूकता|विश्वासार्हता|खात्री)"
            ]
        ),
        (
            AgriculturalIntent.IMAGE_QUERY,
            [
                r"\b(?:this image|in the photo|this picture|uploaded leaf|leaf image)\b",
                r"(?:या फोटोमध्ये|या चित्रात|अपलोड केलेले छायाचित्र)"
            ]
        ),

        # Weather & Outbreak Risk
        (
            AgriculturalIntent.WEATHER_DISEASE_RISK,
            [
                r"\bweather.*(?:risk|disease|outbreak|fungus|blight|spread|increase)\b",
                r"\b(?:tomorrow|forecast|rain|humidity|cloudy|weather).*(?:increase|cause|risk|outbreak|favor)\b",
                r"\b(?:risk|outbreak).*weather\b",
                r"हवामान.*(?:रोग|धोका|बुरशी|प्रादुर्भाव|वाढेल)",
                r"रोग.*हवामान",
                r"उद्याचे हवामान"
            ]
        ),
        (
            AgriculturalIntent.WEATHER,
            [
                r"\b(?:weather|rain|temperature|humidity|forecast|rainfall|climate)\b",
                r"(?:हवामान|पाऊस|तापमान|आर्द्रता|पावसाळा)"
            ]
        ),

        # Disease Transmission & Spread
        (
            AgriculturalIntent.DISEASE_TRANSMISSION,
            [
                r"\b(?:spread|transmit|transmission|contagious|infect nearby|spread to|other plants|airborne|wind-borne)\b",
                r"(?:पसरेल|पसरू शकतो|इतर झाडांवर|संसर्ग|प्रसार)"
            ]
        ),

        # Disease Causes & Pathology
        (
            AgriculturalIntent.DISEASE_CAUSE,
            [
                r"\b(?:cause|causes|why|pathogen|fungus|bacterium|virus|oomycete|origin|source)\b.*\b(?:disease|blight|mildew|rot|rust|spot|yellow|curl)\b",
                r"\bwhy are.*(?:turning yellow|leaves yellow|spots|dropping|drying|yellow)\b",
                r"\bwhat causes\b",
                r"(?:पाने पिवळी|पिवळी का|पिवळे पडणे|रोगाचे कारण|रोग का होतो)"
            ]
        ),

        # Disease Prevention & Cultural Controls
        (
            AgriculturalIntent.DISEASE_PREVENTION,
            [
                r"\b(?:prevent|prevention|preventive|avoid|protect|protection|stop spreading|sanitize|prophylactic)\b",
                r"(?:प्रतिबंध|संरक्षण|प्रसार रोखणे|रोग टाळणे|पसरू नये|प्रतिबंधक)"
            ]
        ),

        # Disease Symptoms & Identification
        (
            AgriculturalIntent.DISEASE_SYMPTOMS,
            [
                r"\b(?:symptom|symptoms|sign|signs|look like|appearance|spots|rings|lesion|mold|powder|identify)\b",
                r"(?:लक्षणे|चिन्हे|डाग|बुरशी|पानांवर काय दिसते|कसे ओळखावे)"
            ]
        ),

        # Disease Treatment & Chemical / Bio Management
        (
            AgriculturalIntent.DISEASE_TREATMENT,
            [
                r"\b(?:treat|treatment|cure|control|manage|management|spray|spraying|fungicide|pesticide|remedy|neem oil|dosage|dose|medicine)\b",
                r"(?:उपचार|नियंत्रण|फवारणी|औषध|कीटकनाशक|बुरशीनाशक|कडुनिंब|डोस)"
            ]
        ),

        # Soil & pH
        (
            AgriculturalIntent.SOIL,
            [
                r"\b(?:soil|land|ph|acidity|alkalinity|saline|sodic|salinity|sodicity|gypsum|reclaim|reclamation|alkali|loam|clay|sandy|alluvial|black soil|tilth|hardpan)\b",
                r"(?:माती|जमीन|सामू|खारवट|चोपण|जिप्सम|काळी माती|तांबडी माती|गाळाची माती|सुपीकता)"
            ]
        ),

        # Irrigation & Water
        (
            AgriculturalIntent.IRRIGATION,
            [
                r"\b(?:water|irrigate|irrigation|watering|how often.*water|how much water|drip|sprinkler|moisture|vafsa|drainage)\b",
                r"(?:पाणी|सिंचन|ठिबक|तुषार|वाफसा|पाण्याचे नियोजन|पाणी व्यवस्थापन|पाणी कधी द्यावे|पाणी किती|पाणी द्यावे)"
            ]
        ),

        # Fertilizer & Nutrition
        (
            AgriculturalIntent.FERTILIZER,
            [
                r"\b(?:fertilizer|fertilisation|fertilization|npk|urea|nano urea|dap|potash|fym|manure|compost|jeevamrut|beejamrut|neemastra|dashparni|bio-stimulant|biostimulant|humic|seaweed|slurry)\b",
                r"(?:खत|खते|युरिया|नॅनो युरिया|डीएपी|पोटॅश|शेणखत|गांडूळ खत|जीवामृत|बीजामृत|दशपर्णी|ह्युमिक|सेंद्रिय खत)"
            ]
        ),
        (
            AgriculturalIntent.NUTRITION,
            [
                r"\b(?:nutrient|nutrition|deficiency|zinc|boron|calcium|magnesium|chlorosis|micronutrient)\b",
                r"(?:अन्नद्रव्य|सूक्ष्म अन्नद्रव्य|कमतरता|झिंक|बोरॉन|कॅल्शियम)"
            ]
        ),

        # Harvesting & Post-Harvest
        (
            AgriculturalIntent.HARVESTING,
            [
                r"\b(?:harvest|harvested|harvesting|picking|maturity|yield|ripe|ripening|post-harvest|curing|storage)\b",
                r"(?:काढणी|तोडणी|पक्वता|उत्पादन|साठवणूक|काढणीची वेळ)"
            ]
        ),

        # Planting & Sowing
        (
            AgriculturalIntent.PLANTING,
            [
                r"\b(?:how to plant|planting|sow|sowing|seed|seedling|nursery|transplant|transplanting|spacing|seed rate)\b",
                r"(?:लागवड|पेरणी|बियाणे|रोपे|रोपवाटिका|पुनर्लागवड|अंतर)"
            ]
        ),

        # Growth Stages
        (
            AgriculturalIntent.GROWTH_STAGE,
            [
                r"\b(?:growth stage|stage|tillering|flowering|bloom|tasseling|silking|vegetative|panicle)\b",
                r"(?:वाढीची अवस्था|फुटवे|फुलधारणा|बहर|दाणे भरणे)"
            ]
        ),

        # General Pests
        (
            AgriculturalIntent.PEST,
            [
                r"\b(?:pest|pests|insect|insects|caterpillar|borer|aphid|whitefly|thrips|mite|hopper|worm)\b",
                r"(?:कीड|किडी|अळी|मावा|तुडतुडे|पांढरी माशी|फुलकिडे|खोंड)"
            ]
        ),

        # General Agriculture Concepts
        (
            AgriculturalIntent.GENERAL_AGRICULTURE,
            [
                r"\b(?:crop rotation|photosynthesis|ipm|integrated pest management|green manure|organic farming|intercropping|mulching)\b",
                r"(?:पिकांची फेरपालट|प्रकाशसंश्लेषण|सेंद्रिय शेती|आंतरपीक|हिरवळीचे खत)"
            ]
        ),

        # Crop Management & Pruning
        (
            AgriculturalIntent.CROP_MANAGEMENT,
            [
                r"\b(?:prune|pruning|trellis|trellising|staking|weeding|earthing up|intercrop)\b",
                r"(?:छाटणी|बांधणी|तण व्यवस्थापन|भर लावणे)"
            ]
        ),

        # Non-Agri / Math / Greetings
        (
            AgriculturalIntent.GENERAL,
            [
                r"\b(?:hello|hi|hey|namaste|good morning|who are you|2\+2|what is 2\+2)\b",
                r"(?:नमस्कार|हॅलो|शुभ सकाळ)"
            ]
        )
    ]

    @classmethod
    def detect_intent(cls, query: str) -> str:
        """Classify query into an AgriculturalIntent."""
        if not query or not query.strip():
            return AgriculturalIntent.GENERAL

        q_lower = query.lower().strip()

        # Check in prioritized order
        for intent, patterns in cls.INTENT_PATTERNS:
            for pat in patterns:
                if re.search(pat, q_lower):
                    return intent

        # Fallback heuristics
        if any(w in q_lower for w in ["what disease", "disease does", "which disease", "काय रोग", "कोणता रोग"]):
            return AgriculturalIntent.DISEASE_IDENTIFICATION
        if any(w in q_lower for w in ["disease", "blight", "rot", "mildew", "spot", "रोग", "करपा"]):
            return AgriculturalIntent.DISEASE_IDENTIFICATION
        if any(w in q_lower for w in ["crop", "plant", "grow", "cultivation", "शेती", "पीक"]):
            return AgriculturalIntent.CROP_MANAGEMENT

        return AgriculturalIntent.GENERAL_AGRICULTURE

    @classmethod
    def extract_entities(cls, query: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract explicit plant and disease entities from the query string."""
        if not query:
            return (None, None)

        q_lower = query.lower().strip()
        matched_plant = None
        matched_disease = None

        # 1. Match Plant
        for key, pdata in PLANTS_KNOWLEDGE_BASE.items():
            cname = pdata["common_name"].lower()
            sname = pdata["scientific_name"].lower()
            if key in q_lower or cname in q_lower or sname in q_lower:
                matched_plant = pdata["common_name"]
                break

        # Check vernacular names if still None
        if not matched_plant:
            vernacular_map = {
                "आंबा": "Mango", "आंब्यावर": "Mango", "aam": "Mango", "mango": "Mango",
                "ऊस": "Sugarcane", "उसात": "Sugarcane", "उसावर": "Sugarcane", "उसाचे": "Sugarcane", "उसाच्या": "Sugarcane", "ganna": "Sugarcane", "sugarcane": "Sugarcane",
                "टोमॅटो": "Tomato", "टोमॅटोवर": "Tomato", "tomato": "Tomato", "tamatar": "Tomato",
                "बटाटा": "Potato", "बटाट्यावर": "Potato", "batata": "Potato", "aloo": "Potato", "potato": "Potato",
                "कापूस": "Cotton", "कपाशी": "Cotton", "कपाशीवर": "Cotton", "कपाशीवरील": "Cotton", "कपाशीच्या": "Cotton", "कपाशीत": "Cotton", "kapas": "Cotton", "cotton": "Cotton",
                "भात": "Rice (Paddy)", "भातावर": "Rice (Paddy)", "भातात": "Rice (Paddy)", "धान": "Rice (Paddy)", "धनावर": "Rice (Paddy)", "rice": "Rice (Paddy)", "paddy": "Rice (Paddy)",
                "गहू": "Wheat", "गव्हावर": "Wheat", "गव्हात": "Wheat", "gehun": "Wheat", "wheat": "Wheat",
                "मका": "Maize (Corn)", "मक्यावर": "Maize (Corn)", "मक्यात": "Maize (Corn)", "makka": "Maize (Corn)", "corn": "Maize (Corn)", "maize": "Maize (Corn)",
                "मिरची": "Chilli (Pepper)", "मिरचीवर": "Chilli (Pepper)", "मिरचीत": "Chilli (Pepper)", "mirchi": "Chilli (Pepper)", "chilli": "Chilli (Pepper)",
                "कांदा": "Onion", "कांद्यावर": "Onion", "कांद्यात": "Onion", "kanda": "Onion", "pyaj": "Onion", "onion": "Onion",
                "सोयाबीन": "Soybean", "सोयाबीनवर": "Soybean", "सोयाबीनमध्ये": "Soybean", "soybean": "Soybean",
                "डाळिंब": "Pomegranate", "डाळिंबावर": "Pomegranate", "डाळिंबात": "Pomegranate", "dalimb": "Pomegranate", "anar": "Pomegranate", "pomegranate": "Pomegranate",
                "केळी": "Banana", "केळीवर": "Banana", "केळीत": "Banana", "kela": "Banana", "keli": "Banana", "banana": "Banana",
                "द्राक्षे": "Grape", "द्राक्ष": "Grape", "द्राक्षांवर": "Grape", "द्राक्षबागेत": "Grape", "draksh": "Grape", "grapes": "Grape", "angur": "Grape",
                "भूईमूग": "Groundnut", "भुईमूग": "Groundnut", "भुईमुगावर": "Groundnut", "bhuimug": "Groundnut", "mungfali": "Groundnut", "peanut": "Groundnut", "groundnut": "Groundnut",
                "हरभरा": "Chickpea (Gram)", "हरभऱ्यावर": "Chickpea (Gram)", "harbara": "Chickpea (Gram)", "chana": "Chickpea (Gram)", "chickpea": "Chickpea (Gram)",
                "पपई": "Papaya", "पपईवर": "Papaya", "papai": "Papaya", "papita": "Papaya", "papaya": "Papaya",
                "हळद": "Turmeric", "हळदीवर": "Turmeric", "halad": "Turmeric", "haldi": "Turmeric", "turmeric": "Turmeric",
                "आले": "Ginger", "आल्यात": "Ginger", "ale": "Ginger", "adrak": "Ginger", "ginger": "Ginger",
                "सफरचंद": "Apple", "safarchand": "Apple", "apple": "Apple",
                "पेरू": "Guava", "पेरूवर": "Guava", "peru": "Guava", "amrood": "Guava", "guava": "Guava",
                "तूर": "Pigeonpea (Red Gram)", "तुरीवर": "Pigeonpea (Red Gram)", "tur": "Pigeonpea (Red Gram)", "arhar": "Pigeonpea (Red Gram)", "pigeonpea": "Pigeonpea (Red Gram)",
                "वांगी": "Brinjal (Eggplant)", "वांग्यावर": "Brinjal (Eggplant)", "vangi": "Brinjal (Eggplant)", "baingan": "Brinjal (Eggplant)", "brinjal": "Brinjal (Eggplant)",
                "लसूण": "Garlic", "लसणावर": "Garlic", "lasun": "Garlic", "lahsun": "Garlic", "garlic": "Garlic",
                "कलिंगड": "Watermelon", "कलिंगडावर": "Watermelon", "kalingad": "Watermelon", "tarbuj": "Watermelon", "watermelon": "Watermelon",
                "लिंबू": "Citrus (Lemon / Lime)", "लिंबावर": "Citrus (Lemon / Lime)", "limbu": "Citrus (Lemon / Lime)", "citrus": "Citrus (Lemon / Lime)", "lemon": "Citrus (Lemon / Lime)"
            }
            for vname, mapped in vernacular_map.items():
                if vname in q_lower:
                    matched_plant = mapped
                    break

        # 2. Match Disease
        for key, ddata in DISEASES_KNOWLEDGE_BASE.items():
            dname = ddata["disease_name"].lower()
            dsname = ddata["scientific_name"].lower()
            if key in q_lower or dname in q_lower or dsname in q_lower:
                matched_disease = ddata["disease_name"]
                break

        if not matched_disease:
            disease_vernacular = {
                "powdery mildew": "Powdery Mildew",
                "भुरी": "Powdery Mildew",
                "anthracnose": "Anthracnose / Fruit Rot / Dieback",
                "करपा": "Early Blight",
                "तांबोरा": "Rust",
                "rust": "Rust",
                "early blight": "Early Blight",
                "late blight": "Late Blight",
                "blast": "Rice Blast / Leaf & Neck Blast",
                "red rot": "Red Rot of Sugarcane",
                "smut": "Sugarcane Smut",
                "काणी": "Sugarcane Smut",
                "purple blotch": "Purple Blotch of Onion & Garlic",
                "leaf curl": "Chilli / Tomato Leaf Curl Virus",
                "तेल्या": "Pomegranate Bacterial Blight / Telya",
                "telya": "Pomegranate Bacterial Blight / Telya",
                "sigatoka": "Sigatoka Leaf Spot",
                "सिगाटोका": "Sigatoka Leaf Spot",
                "panama": "Panama Wilt",
                "पनामा": "Panama Wilt",
                "downy": "Downy Mildew of Grapes",
                "डाउनी": "Downy Mildew of Grapes",
                "tikka": "Tikka Disease / Cercospora Leaf Spot",
                "टिक्का": "Tikka Disease / Cercospora Leaf Spot",
                "मर": "Fusarium Wilt",
                "blossom end rot": "Blossom End Rot (BER)",
                "ber": "Blossom End Rot (BER)",
                "deficiency": "Crop Nutrient Deficiencies",
                "chlorosis": "Crop Nutrient Deficiencies",
                "apple scab": "Apple Scab",
                "scab": "Apple Scab",
                "guava wilt": "Guava Wilt",
                "पेरू मर": "Guava Wilt",
                "वांज रोग": "Pigeonpea Sterility Mosaic Disease (SMD)",
                "sterility mosaic": "Pigeonpea Sterility Mosaic Disease (SMD)",
                "damping off": "Damping-Off in Seedlings & Nurseries",
                "रोपांची मर": "Damping-Off in Seedlings & Nurseries",
                "nematode": "Root-Knot Nematode Infestation",
                "सूत्रकृमी": "Root-Knot Nematode Infestation",
                "गाठी": "Root-Knot Nematode Infestation",
                "citrus canker": "Citrus Bacterial Canker",
                "खैरा": "Citrus Bacterial Canker",
                "दहिया": "Bacterial Blight of Cotton / Grey Mildew (Dahiya)",
                "बोंडअळी": "Bollworm Infestation (Cotton Pink & American Bollworm)",
                "खोडकिडा": "Stem Borer Infestation"
            }
            for dv, mapped_d in disease_vernacular.items():
                if dv in q_lower:
                    matched_disease = mapped_d
                    break

        return (matched_plant, matched_disease)

    @classmethod
    def resolve_context(
        cls,
        query: str,
        scan_context: Optional[Dict[str, Any]],
        manual_plant: Optional[str],
        conversation_history: Optional[List[Dict[str, str]]]
    ) -> Dict[str, Any]:
        intent = cls.detect_intent(query)
        q_plant, q_disease = cls.extract_entities(query)

        resolved_plant = q_plant
        resolved_disease = q_disease
        context_source = "query" if q_plant else "none"

        # Check if scan context is genuine
        has_valid_scan = bool(
            scan_context and
            scan_context.get("valid_plant_image", True) and
            (scan_context.get("crop_detected") or scan_context.get("plantName"))
        )

        # If query has no plant, check active scan context
        if not resolved_plant and has_valid_scan and scan_context:
            resolved_plant = scan_context.get("crop_detected") or scan_context.get("plantName")
            context_source = "scan"

        # If still no plant, check manual plant selection
        if not resolved_plant and manual_plant:
            resolved_plant = manual_plant
            context_source = "manual"

        # If still no plant, scan previous conversation turns for context
        if not resolved_plant and conversation_history:
            for turn in reversed(conversation_history[-4:]):
                hist_text = turn.get("content", "")
                h_plant, h_disease = cls.extract_entities(hist_text)
                if h_plant:
                    resolved_plant = h_plant
                    context_source = "conversation_history"
                    if not resolved_disease and h_disease:
                        resolved_disease = h_disease
                    break

        # If query has no disease, resolve disease ONLY when intent is pathology-related
        is_pathology_intent = intent in [
            AgriculturalIntent.DISEASE_IDENTIFICATION,
            AgriculturalIntent.DISEASE_EXPLANATION,
            AgriculturalIntent.DISEASE_SYMPTOMS,
            AgriculturalIntent.DISEASE_CAUSE,
            AgriculturalIntent.DISEASE_PREVENTION,
            AgriculturalIntent.DISEASE_TREATMENT,
            AgriculturalIntent.DISEASE_TRANSMISSION,
            AgriculturalIntent.WEATHER_DISEASE_RISK,
            AgriculturalIntent.SCAN_EXPLANATION
        ]

        if not resolved_disease and is_pathology_intent:
            if has_valid_scan and scan_context and scan_context.get("disease_name"):
                resolved_disease = scan_context.get("disease_name")
            elif conversation_history:
                for turn in reversed(conversation_history[-4:]):
                    hist_text = turn.get("content", "")
                    _, h_disease = cls.extract_entities(hist_text)
                    if h_disease:
                        resolved_disease = h_disease
                        break

        # If intent is purely agronomic (Irrigation, Fertilizer, Soil, Harvesting, Sowing),
        # DO NOT inject or prioritize disease context
        if intent in [
            AgriculturalIntent.IRRIGATION,
            AgriculturalIntent.FERTILIZER,
            AgriculturalIntent.SOIL,
            AgriculturalIntent.HARVESTING,
            AgriculturalIntent.PLANTING,
            AgriculturalIntent.GROWTH_STAGE
        ] and not q_disease:
            resolved_disease = None

        return {
            "intent": intent,
            "plant": resolved_plant,
            "disease": resolved_disease,
            "context_source": context_source,
            "raw_query": query
        }
