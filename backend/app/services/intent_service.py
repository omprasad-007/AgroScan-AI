"""
AgroScan AI — Agricultural Intent & Entity Classification Service
Classifies user queries into 18+ agricultural domains, extracts botanical/pathological entities,
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
    DISEASE_IDENTIFICATION = "DISEASE_IDENTIFICATION"
    PLANT_IDENTIFICATION = "PLANT_IDENTIFICATION"
    PEST = "PEST"
    WEATHER = "WEATHER"
    WEATHER_DISEASE_RISK = "WEATHER_DISEASE_RISK"
    CROP_MANAGEMENT = "CROP_MANAGEMENT"
    GENERAL_AGRICULTURE = "GENERAL_AGRICULTURE"
    GENERAL = "GENERAL"

class IntentService:
    """Classifies user queries into domain-specific agricultural intents and entities."""

    INTENT_PATTERNS = [
        # Weather & Outbreak Risk
        (
            AgriculturalIntent.WEATHER_DISEASE_RISK,
            [
                r"\bweather.*(?:risk|disease|outbreak|fungus|blight|spread)\b",
                r"\b(?:risk|outbreak).*weather\b",
                r"\bहवामान.*(?:रोग|धोका|बुरशी|प्रादुर्भाव)\b",
                r"\bरोग.*हवामान\b"
            ]
        ),
        (
            AgriculturalIntent.WEATHER,
            [
                r"\b(?:weather|rain|temperature|humidity|forecast|rainfall|climate)\b",
                r"\b(?:हवामान|पाऊस|तापमान|आर्द्रता|पावसाळा)\b"
            ]
        ),

        # Soil & pH
        (
            AgriculturalIntent.SOIL,
            [
                r"\b(?:soil|land|ph|acidity|alkalinity|loam|clay|sandy|alluvial|black soil|tilth|hardpan)\b",
                r"\b(?:माती|जमीन|सामू|काळी माती|तांबडी माती|गाळाची माती|सुपीकता)\b"
            ]
        ),

        # Irrigation & Water
        (
            AgriculturalIntent.IRRIGATION,
            [
                r"\b(?:water|irrigate|irrigation|watering|drip|sprinkler|moisture|vafsa|drainage)\b",
                r"\b(?:पाणी|सिंचन|ठिबक|तुषार|वाफसा|पाण्याचे नियोजन|पाणी व्यवस्थापन)\b"
            ]
        ),

        # Fertilizer & Nutrition
        (
            AgriculturalIntent.FERTILIZER,
            [
                r"\b(?:fertilizer|fertilisation|fertilization|npk|urea|dap|potash|fym|manure|compost|jeevamrut|slurry)\b",
                r"\b(?:खत|खते|युरिया|डीएपी|पोटॅश|शेणखत|गांडूळ खत|जीवामृत|सेंद्रिय खत)\b"
            ]
        ),
        (
            AgriculturalIntent.NUTRITION,
            [
                r"\b(?:nutrient|nutrition|deficiency|zinc|boron|calcium|magnesium|chlorosis|micronutrient)\b",
                r"\b(?:अन्नद्रव्य|सूक्ष्म अन्नद्रव्य|कमतरता|झिंक|बोरॉन|कॅल्शियम|पिवळे पडणे)\b"
            ]
        ),

        # Harvesting & Post-Harvest
        (
            AgriculturalIntent.HARVESTING,
            [
                r"\b(?:harvest|harvested|harvesting|picking|maturity|yield|ripe|ripening|post-harvest|curing|storage)\b",
                r"\b(?:काढणी|तोडणी|पक्वता|उत्पादन|साठवणूक|काढणीची वेळ)\b"
            ]
        ),

        # Planting & Sowing
        (
            AgriculturalIntent.PLANTING,
            [
                r"\b(?:plant|planting|sow|sowing|seed|seedling|nursery|transplant|transplanting|spacing|seed rate)\b",
                r"\b(?:लागवड|पेरणी|बियाणे|रोपे|रोपवाटिका|पुनर्लागवड|अंतर)\b"
            ]
        ),

        # Growth Stages
        (
            AgriculturalIntent.GROWTH_STAGE,
            [
                r"\b(?:growth stage|stage|tillering|flowering|bloom|tasseling|silking|vegetative|panicle)\b",
                r"\b(?:वाढीची अवस्था|फुटवे|फुलधारणा|बहर|दाणे भरणे)\b"
            ]
        ),

        # Disease Causes & Pathology
        (
            AgriculturalIntent.DISEASE_CAUSE,
            [
                r"\b(?:cause|causes|why|pathogen|fungus|bacterium|virus|oomycete|origin|source)\b.*\b(?:disease|blight|mildew|rot|rust|spot)\b",
                r"\bwhat causes\b",
                r"\bरोगाचे कारण\b",
                r"\bरोग का होतो\b"
            ]
        ),

        # Disease Symptoms & Identification
        (
            AgriculturalIntent.DISEASE_SYMPTOMS,
            [
                r"\b(?:symptom|symptoms|sign|signs|look like|appearance|spots|rings|lesion|mold|powder|identify)\b",
                r"\b(?:लक्षणे|चिन्हे|डाग|बुरशी|पानांवर काय दिसते|कसे ओळखावे)\b"
            ]
        ),

        # Disease Prevention & Cultural Controls
        (
            AgriculturalIntent.DISEASE_PREVENTION,
            [
                r"\b(?:prevent|prevention|preventive|avoid|protect|protection|stop spreading|spread|sanitize)\b",
                r"\b(?:प्रतिबंध|संरक्षण|प्रसार रोखणे|रोग टाळणे|पसरू नये)\b"
            ]
        ),

        # Disease Treatment & Chemical / Bio Management
        (
            AgriculturalIntent.DISEASE_TREATMENT,
            [
                r"\b(?:treat|treatment|cure|control|manage|management|spray|spraying|fungicide|pesticide|remedy|neem oil|dosage)\b",
                r"\b(?:उपचार|नियंत्रण|फवारणी|औषध|कीटकनाशक|बुरशीनाशक|कडुनिंब|डोस)\b"
            ]
        ),

        # General Pests
        (
            AgriculturalIntent.PEST,
            [
                r"\b(?:pest|pests|insect|insects|caterpillar|borer|aphid|whitefly|thrips|mite|hopper|worm)\b",
                r"\b(?:कीड|किडी|अळी|मावा|तुडतुडे|पांढरी माशी|फुलकिडे|खोंड)\b"
            ]
        ),

        # General Agriculture Concepts
        (
            AgriculturalIntent.GENERAL_AGRICULTURE,
            [
                r"\b(?:crop rotation|photosynthesis|ipm|integrated pest management|green manure|organic farming|intercropping|mulching)\b",
                r"\b(?:पिकांची फेरपालट|प्रकाशसंश्लेषण|सेंद्रिय शेती|आंतरपीक|हिरवळीचे खत)\b"
            ]
        ),

        # Crop Management & Pruning
        (
            AgriculturalIntent.CROP_MANAGEMENT,
            [
                r"\b(?:prune|pruning|trellis|trellising|staking|weeding|earthing up|intercrop)\b",
                r"\b(?:छाटणी|बांधणी|तण व्यवस्थापन|भर लावणे)\b"
            ]
        ),

        # Non-Agri / Math / Greetings
        (
            AgriculturalIntent.GENERAL,
            [
                r"\b(?:hello|hi|hey|namaste|good morning|who are you|2\+2|what is 2\+2)\b",
                r"\b(?:नमस्कार|हॅलो|शुभ सकाळ)\b"
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

        # Fallback heuristic
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
                "आंबा": "Mango", "aam": "Mango", "mango": "Mango",
                "ऊस": "Sugarcane", "ganna": "Sugarcane", "sugarcane": "Sugarcane",
                "टोमॅटो": "Tomato", "tomato": "Tomato", "tamatar": "Tomato",
                "बटाटा": "Potato", "batata": "Potato", "aloo": "Potato", "potato": "Potato",
                "कापूस": "Cotton", "kapas": "Cotton", "cotton": "Cotton",
                "भात": "Rice (Paddy)", "धान": "Rice (Paddy)", "rice": "Rice (Paddy)", "paddy": "Rice (Paddy)",
                "गहू": "Wheat", "gehun": "Wheat", "wheat": "Wheat",
                "मका": "Maize (Corn)", "makka": "Maize (Corn)", "corn": "Maize (Corn)", "maize": "Maize (Corn)",
                "मिरची": "Chilli (Pepper)", "mirchi": "Chilli (Pepper)", "chilli": "Chilli (Pepper)",
                "कांदा": "Onion", "kanda": "Onion", "pyaj": "Onion", "onion": "Onion",
                "सोयाबीन": "Soybean", "soybean": "Soybean"
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
                "leaf curl": "Chilli / Tomato Leaf Curl Virus"
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
        """
        Resolves active context with strict priority:
        1. Explicit entity in query (e.g. 'What soil for mango?')
        2. Real Scan Context (if present & verified)
        3. Manual Selected Plant
        4. Prior Conversation History (last mentioned plant/disease)
        5. None (General Agriculture)
        """
        intent = cls.detect_intent(query)
        q_plant, q_disease = cls.extract_entities(query)

        resolved_plant = q_plant
        resolved_disease = q_disease
        context_source = "query" if q_plant else "none"

        # If query has no plant, check active scan context
        if not resolved_plant and scan_context:
            resolved_plant = scan_context.get("crop_detected") or scan_context.get("plantName")
            if not resolved_disease:
                resolved_disease = scan_context.get("disease_name")
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

        return {
            "intent": intent,
            "plant": resolved_plant,
            "disease": resolved_disease,
            "context_source": context_source,
            "raw_query": query
        }
