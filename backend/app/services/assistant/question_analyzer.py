"""
AgroScan AI — Question Analysis Pipeline
Provides structured question analysis, intent/sub-intent classification, entity resolution,
follow-up pronoun handling, and dynamic context-requirement determination.
"""

import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.knowledge.plants_data import PLANTS_KNOWLEDGE_BASE
from app.knowledge.diseases_data import DISEASES_KNOWLEDGE_BASE
from app.services.intent_service import AgriculturalIntent, IntentService

class QuestionAnalysis(BaseModel):
    original_question: str
    normalized_question: str
    language: str = "en"
    intent: str
    sub_intent: Optional[str] = None
    question_type: str = "informational"
    plant: Optional[str] = None
    crop: Optional[str] = None
    disease: Optional[str] = None
    symptoms: List[str] = Field(default_factory=list)
    pests: List[str] = Field(default_factory=list)
    growth_stage: Optional[str] = None
    requested_information: List[str] = Field(default_factory=list)
    requires_scan_context: bool = False
    requires_weather: bool = False
    requires_location: bool = False
    requires_web_research: bool = False
    requires_rag: bool = True
    requires_multi_source_verification: bool = False
    requires_safety_check: bool = False
    confidence: float = 1.0


class QuestionAnalyzer:
    """Analyzes user inputs into a structured QuestionAnalysis schema."""

    PRONOUN_PATTERNS = [
        r"\b(?:it|this|this plant|this crop|this disease|this infection|the disease|the crop|the tree)\b",
        r"\b(?:हा रोग|हे पीक|या पिकाला|या रोगावर|याचे|याची|याला)\b"
    ]

    SYMPTOM_PATTERNS = [
        ("yellow_leaves", [r"yellow\b", r"yellowing\b", r"chlorosis\b", r"पिवळे\b", r"पिवळेपणा\b"]),
        ("brown_black_spots", [r"brown spot", r"black spot", r"leaf spot", r"dark spot", r"काळे डाग", r"तपकिरी डाग"]),
        ("white_powder", [r"white powder", r"powdery", r"talc", r"पांढरी पावडर", r"भुरी"]),
        ("wilting", [r"wilt", r"droop", r"वाळणे", r"कोमेजणे"]),
        ("leaf_curl", [r"curl", r"curling", r"सुरकुत्या", r"बोकड्या"]),
        ("rot", [r"rot", r"rotting", r"decay", r"कुजणे", r"सडणे"]),
    ]

    PEST_PATTERNS = [
        ("aphid", [r"aphid", r"मावा"]),
        ("whitefly", [r"whitefly", r"पांढरी माशी"]),
        ("thrips", [r"thrip", r"फुलकिडे"]),
        ("caterpillar", [r"caterpillar", r"borer", r"armyworm", r"अळी", r"खोंड"]),
        ("mite", [r"mite", r"लाल कोळी"]),
    ]

    GROWTH_STAGE_PATTERNS = [
        ("seedling", [r"seedling", r"germination", r"nursery", r"रोपवाटिका", r"उगवण"]),
        ("vegetative", [r"vegetative", r"tillering", r"फुटवे"]),
        ("flowering", [r"flowering", r"bloom", r"blossom", r"फुलधारणा", r"मोहोर", r"बहर"]),
        ("fruiting", [r"fruiting", r"pod", r"grain filling", r"फळधारणा", r"दाणे भरणे"]),
        ("maturity_harvest", [r"harvest", r"mature", r"ripening", r"काढणी", r"पक्वता"]),
    ]

    @classmethod
    def normalize_text(cls, text: str) -> str:
        """Cleans and standardizes raw user text."""
        if not text:
            return ""
        # Remove repeated whitespace and strip
        cleaned = re.sub(r"\s+", " ", text).strip()
        return cleaned

    @classmethod
    def detect_language(cls, text: str, explicit_lang: Optional[str] = None) -> str:
        """Detects if query is in Marathi or English."""
        if explicit_lang in ["mr", "en"]:
            # If explicit Marathi is passed, verify or honor
            if explicit_lang == "mr":
                return "mr"
        
        # Check Devanagari script presence
        if any('\u0900' <= char <= '\u097F' for char in text):
            return "mr"
        return "en"

    @classmethod
    def has_referential_pronoun(cls, text: str) -> bool:
        """Checks if text contains anaphoric pronouns referencing prior context."""
        t_lower = text.lower()
        for pat in cls.PRONOUN_PATTERNS:
            if re.search(pat, t_lower):
                return True
        return False

    @classmethod
    def resolve_pronouns_from_history(
        cls,
        text: str,
        conversation_history: Optional[List[Dict[str, str]]]
    ) -> Tuple_Entities:
        """Resolves plant and disease from conversation history when pronouns are used."""
        plant = None
        disease = None
        if not conversation_history:
            return (None, None)

        for turn in reversed(conversation_history[-6:]):
            content = turn.get("content", "")
            h_plant, h_disease = IntentService.extract_entities(content)
            if not plant and h_plant:
                plant = h_plant
            if not disease and h_disease:
                disease = h_disease
            if plant and disease:
                break

        return (plant, disease)

    @classmethod
    def analyze(
        cls,
        question: str,
        language: Optional[str] = "en",
        conversation_history: Optional[List[Dict[str, str]]] = None,
        has_active_scan: bool = False
    ) -> QuestionAnalysis:
        norm_q = cls.normalize_text(question)
        detected_lang = cls.detect_language(norm_q, language)

        # 1. Intent Detection
        intent = IntentService.detect_intent(norm_q)

        # 2. Extract Entities from Query
        q_plant, q_disease = IntentService.extract_entities(norm_q)

        # 3. Follow-up pronoun resolution if entity is missing
        if (not q_plant or not q_disease) and cls.has_referential_pronoun(norm_q):
            h_plant, h_disease = cls.resolve_pronouns_from_history(norm_q, conversation_history)
            if not q_plant and h_plant:
                q_plant = h_plant
            if not q_disease and h_disease:
                q_disease = h_disease

        # 4. Symptoms Extraction
        symptoms: List[str] = []
        norm_lower = norm_q.lower()
        for sym_name, patterns in cls.SYMPTOM_PATTERNS:
            for pat in patterns:
                if re.search(pat, norm_lower):
                    symptoms.append(sym_name)
                    break

        # 5. Pests Extraction
        pests: List[str] = []
        for pest_name, patterns in cls.PEST_PATTERNS:
            for pat in patterns:
                if re.search(pat, norm_lower):
                    pests.append(pest_name)
                    break

        # 6. Growth Stage Extraction
        growth_stage = None
        for stage_name, patterns in cls.GROWTH_STAGE_PATTERNS:
            for pat in patterns:
                if re.search(pat, norm_lower):
                    growth_stage = stage_name
                    break
            if growth_stage:
                break

        # 7. Determine Question Type & Requirements
        question_type = "informational"
        sub_intent = None
        req_info: List[str] = []

        if intent in [AgriculturalIntent.DISEASE_IDENTIFICATION, AgriculturalIntent.SCAN_EXPLANATION]:
            question_type = "diagnostic"
            req_info = ["disease_name", "symptoms", "confidence"]
        elif intent in [AgriculturalIntent.DISEASE_TREATMENT, AgriculturalIntent.DISEASE_PREVENTION, AgriculturalIntent.PEST_MANAGEMENT]:
            question_type = "prescriptive"
            req_info = ["organic_remedies", "chemical_options", "safety_phi"]
        elif intent in [AgriculturalIntent.IRRIGATION, AgriculturalIntent.FERTILIZER, AgriculturalIntent.SOIL, AgriculturalIntent.PLANTING, AgriculturalIntent.HARVESTING]:
            question_type = "agronomic_advisory"
            req_info = [intent.lower()]
        elif intent in [AgriculturalIntent.WEATHER, AgriculturalIntent.WEATHER_DISEASE_RISK]:
            question_type = "risk_assessment"
            req_info = ["weather_impact", "preventive_action"]
        elif intent == AgriculturalIntent.GENERAL:
            question_type = "general"

        # Determine Context Requirements
        # Critical rule: requires_scan_context is ONLY True if the question is diagnostic / scan-based
        requires_scan = intent in [
            AgriculturalIntent.SCAN_EXPLANATION,
            AgriculturalIntent.CONFIDENCE_EXPLANATION,
            AgriculturalIntent.IMAGE_QUERY
        ] or (
            has_active_scan and intent in [
                AgriculturalIntent.DISEASE_IDENTIFICATION,
                AgriculturalIntent.DISEASE_SYMPTOMS
            ] and not q_disease
        )

        requires_weather = intent in [
            AgriculturalIntent.WEATHER,
            AgriculturalIntent.WEATHER_DISEASE_RISK,
            AgriculturalIntent.RAINFALL_IMPACT,
            AgriculturalIntent.HUMIDITY_IMPACT,
            AgriculturalIntent.TEMPERATURE_IMPACT
        ]

        requires_location = requires_weather or intent in [
            AgriculturalIntent.LOCATION_ADVICE,
            AgriculturalIntent.REGIONAL_SUITABILITY
        ]

        requires_safety = intent in [
            AgriculturalIntent.DISEASE_TREATMENT,
            AgriculturalIntent.PEST_MANAGEMENT,
            AgriculturalIntent.SAFETY_ADVICE,
            AgriculturalIntent.FERTILIZER
        ]

        requires_rag = intent != AgriculturalIntent.GENERAL

        requires_multi_source = intent in [
            AgriculturalIntent.DISEASE_TREATMENT,
            AgriculturalIntent.DISEASE_PREVENTION,
            AgriculturalIntent.WEATHER_DISEASE_RISK,
            AgriculturalIntent.PEST_MANAGEMENT,
            AgriculturalIntent.FERTILIZER
        ]

        return QuestionAnalysis(
            original_question=question,
            normalized_question=norm_q,
            language=detected_lang,
            intent=intent,
            sub_intent=sub_intent,
            question_type=question_type,
            plant=q_plant,
            crop=q_plant,
            disease=q_disease,
            symptoms=symptoms,
            pests=pests,
            growth_stage=growth_stage,
            requested_information=req_info,
            requires_scan_context=requires_scan,
            requires_weather=requires_weather,
            requires_location=requires_location,
            requires_web_research=False,
            requires_rag=requires_rag,
            requires_multi_source_verification=requires_multi_source,
            requires_safety_check=requires_safety,
            confidence=0.95 if q_plant or intent != AgriculturalIntent.GENERAL_AGRICULTURE else 0.85
        )

# Helper type annotation
from typing import Tuple as Tuple_Entities
