"""
AgroScan AI — Gemini Agronomist Service
Wrapper delegating to AIProviderService for unified domain-specific agricultural intelligence.
"""

from typing import Dict, Any, Optional
from app.services.ai_provider_service import AIProviderService

class GeminiAssistantService:
    """
    Service wrapper for Google Gemini AI Agronomist Consultation.
    Delegates to AIProviderService with RAG grounding, intent classification, and multi-turn memory.
    """

    @classmethod
    def generate_chat_response(
        cls, 
        message: str, 
        scan_context: Optional[Dict[str, Any]] = None,
        language: str = "en"
    ) -> str:
        return AIProviderService.generate_response(
            message=message,
            scan_context=scan_context,
            language=language
        )

# Alias for backwards compatibility
GeminiAgronomistService = GeminiAssistantService
