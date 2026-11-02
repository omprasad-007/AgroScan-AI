"""
AgroScan AI — Context Resolution Service
Extracts and isolates verified scan predictions, manual crop inputs, conversation turns, and GPS farm coordinates.
Prevents cross-topic context pollution (e.g. disease overrides on irrigation queries).
"""

from typing import Dict, Any, Optional, List
from app.services.intent_service import IntentService, AgriculturalIntent
from app.services.assistant.question_analyzer import QuestionAnalyzer, QuestionAnalysis

class ContextService:
    """Resolves active crop, disease, scan, and geographic context with strict priority and intent isolation."""

    @classmethod
    def resolve(
        cls,
        query: str,
        scan_context: Optional[Dict[str, Any]] = None,
        manual_plant: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        location_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        has_valid_scan = bool(
            scan_context and
            scan_context.get("valid_plant_image", True) and
            (scan_context.get("crop_detected") or scan_context.get("plantName"))
        )

        analysis = QuestionAnalyzer.analyze(
            question=query,
            conversation_history=conversation_history,
            has_active_scan=has_valid_scan
        )

        intent = analysis.intent
        q_plant = analysis.plant
        q_disease = analysis.disease

        resolved_plant = q_plant
        resolved_disease = q_disease
        context_source = "query" if q_plant else "none"

        ent_detail = IntentService.extract_entities_detail(query)
        disputed_plant = ent_detail.get("disputed_plant")
        disputed_disease = ent_detail.get("disputed_disease")
        scan_plant = (scan_context.get("crop_detected") or scan_context.get("plantName")) if scan_context else None

        q_clean = query.lower()
        is_recheck_or_dispute = any(w in q_clean for w in ["recheck", "rechake", "rescan", "wrong", "not a", "not an", "is not", "चुकीचे", "पुन्हा तपासा", "नाही"])
        is_disputing_scan_plant = bool(
            scan_plant and (
                (disputed_plant and (disputed_plant.lower() in scan_plant.lower() or scan_plant.lower() in disputed_plant.lower())) or
                (is_recheck_or_dispute and not q_plant)
            )
        )

        if is_disputing_scan_plant:
            resolved_plant = q_plant
            resolved_disease = q_disease
            context_source = "user_scan_dispute"
            intent = AgriculturalIntent.SCAN_EXPLANATION
            has_valid_scan = False
        else:
            # 1. Resolve Plant from Real Scan Context if not in query
            if not resolved_plant and has_valid_scan and scan_context:
                resolved_plant = scan_plant
                context_source = "scan"

            # 2. Resolve Plant from Manual selection if still not found
            if not resolved_plant and manual_plant:
                resolved_plant = manual_plant
                context_source = "manual"

            # 3. Resolve Plant from Conversation History if still not found
            if not resolved_plant and conversation_history:
                for turn in reversed(conversation_history[-4:]):
                    hist_text = turn.get("content", "")
                    h_p, _ = IntentService.extract_entities(hist_text)
                    if h_p and h_p != disputed_plant:
                        resolved_plant = h_p
                        context_source = "conversation_history"
                        break

        # 4. Disease resolution (STRICT INTENT ISOLATION)
        # Only attach disease if query asks about disease OR is diagnostic/symptom/treatment/spread
        is_pathology_intent = intent in [
            AgriculturalIntent.DISEASE_IDENTIFICATION,
            AgriculturalIntent.DISEASE_EXPLANATION,
            AgriculturalIntent.DISEASE_SYMPTOMS,
            AgriculturalIntent.DISEASE_CAUSE,
            AgriculturalIntent.DISEASE_PREVENTION,
            AgriculturalIntent.DISEASE_TREATMENT,
            AgriculturalIntent.DISEASE_TRANSMISSION,
            AgriculturalIntent.WEATHER_DISEASE_RISK,
            AgriculturalIntent.SCAN_EXPLANATION,
            AgriculturalIntent.CONFIDENCE_EXPLANATION
        ]

        if not resolved_disease and is_pathology_intent and not is_disputing_scan_plant:
            if has_valid_scan and scan_context and scan_context.get("disease_name"):
                resolved_disease = scan_context.get("disease_name")
            elif conversation_history:
                for turn in reversed(conversation_history[-4:]):
                    hist_text = turn.get("content", "")
                    _, h_d = IntentService.extract_entities(hist_text)
                    if h_d and h_d != disputed_disease:
                        resolved_disease = h_d
                        break

        # Ensure agronomic queries (irrigation, fertilizer, soil, harvesting, sowing) DO NOT have disease injected
        if intent in [
            AgriculturalIntent.IRRIGATION,
            AgriculturalIntent.FERTILIZER,
            AgriculturalIntent.NUTRITION,
            AgriculturalIntent.SOIL,
            AgriculturalIntent.HARVESTING,
            AgriculturalIntent.PLANTING,
            AgriculturalIntent.GROWTH_STAGE
        ] and not q_disease:
            resolved_disease = None

        return {
            "intent": intent,
            "analysis": analysis,
            "plant_name": resolved_plant,
            "disease_name": resolved_disease,
            "context_source": context_source,
            "has_valid_scan": has_valid_scan and context_source == "scan",
            "is_scan_dispute": is_disputing_scan_plant,
            "disputed_plant": disputed_plant or (scan_plant if is_disputing_scan_plant else None),
            "disputed_disease": disputed_disease,
            "is_manual": bool(manual_plant) and context_source == "manual",
            "location": location_info
        }
