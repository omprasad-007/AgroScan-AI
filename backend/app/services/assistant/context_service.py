"""
AgroScan AI — Context Resolution Service
Extracts and isolates verified scan predictions, manual crop inputs, conversation turns, and GPS farm coordinates.
"""

from typing import Dict, Any, Optional, List
from app.services.intent_service import IntentService

class ContextService:
    """Resolves active crop, disease, scan, and geographic context with strict priority."""

    @classmethod
    def resolve(
        cls,
        query: str,
        scan_context: Optional[Dict[str, Any]] = None,
        manual_plant: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        location_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        intent = IntentService.detect_intent(query)
        q_plant, q_disease = IntentService.extract_entities(query)

        resolved_plant = q_plant
        resolved_disease = q_disease
        context_source = "query" if q_plant else "none"

        # 1. Check real scan context
        if not resolved_plant and scan_context and scan_context.get("crop_detected"):
            resolved_plant = scan_context.get("crop_detected")
            if not resolved_disease:
                resolved_disease = scan_context.get("disease_name")
            context_source = "scan"

        # 2. Check manual selection
        if not resolved_plant and manual_plant:
            resolved_plant = manual_plant
            context_source = "manual"

        # 3. Check conversation history
        if not resolved_plant and conversation_history:
            for turn in reversed(conversation_history[-4:]):
                hist_text = turn.get("content", "")
                h_p, h_d = IntentService.extract_entities(hist_text)
                if h_p:
                    resolved_plant = h_p
                    context_source = "conversation_history"
                    if not resolved_disease and h_d:
                        resolved_disease = h_d
                    break

        return {
            "intent": intent,
            "plant_name": resolved_plant,
            "disease_name": resolved_disease,
            "context_source": context_source,
            "has_valid_scan": bool(scan_context and scan_context.get("crop_detected")),
            "is_manual": bool(manual_plant),
            "location": location_info
        }
