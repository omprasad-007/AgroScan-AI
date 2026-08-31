"""
AgroScan AI — AI Provider Service Facade
Provides unified interface routing to modular AssistantService, ResearchService, and RAG.
"""

from typing import Dict, Any, Optional, List
from app.services.assistant.assistant_service import AssistantService

class AIProviderService:
    """Facade for the modular AgroScan AI multi-source assistant system."""

    @classmethod
    def generate_response(
        cls,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        scan_context: Optional[Dict[str, Any]] = None,
        manual_plant: Optional[str] = None,
        location_info: Optional[Dict[str, Any]] = None,
        weather_info: Optional[Dict[str, Any]] = None,
        language: str = "en",
        research_mode: str = "auto"
    ) -> str:
        payload = cls.generate_structured_research_response(
            message=message,
            conversation_history=conversation_history,
            scan_context=scan_context,
            manual_plant=manual_plant,
            location_info=location_info,
            weather_info=weather_info,
            language=language,
            research_mode=research_mode
        )
        return payload["answer"]

    @classmethod
    def generate_structured_research_response(
        cls,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        scan_context: Optional[Dict[str, Any]] = None,
        manual_plant: Optional[str] = None,
        location_info: Optional[Dict[str, Any]] = None,
        weather_info: Optional[Dict[str, Any]] = None,
        language: str = "en",
        research_mode: str = "auto"
    ) -> Dict[str, Any]:
        return AssistantService.process_message(
            message=message,
            conversation_history=conversation_history,
            scan_context=scan_context,
            manual_plant=manual_plant,
            location_info=location_info,
            weather_info=weather_info,
            language=language,
            research_mode=research_mode
        )
