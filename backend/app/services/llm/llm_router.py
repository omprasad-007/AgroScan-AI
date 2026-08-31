"""
AgroScan AI — LLM Model Router
Routes requests to the appropriate model based on query complexity and mode.
"""

from typing import Tuple, List, Dict
from app.services.llm.gemini_provider import GeminiProvider
from app.services.llm.secondary_provider import SecondaryProvider

class LLMRouter:
    """Intelligently routes generation between Gemini, Secondary Provider, and fallback."""

    @classmethod
    def execute_reasoning(
        cls,
        system_prompt: str,
        history: List[Dict[str, str]],
        user_message: str,
        complexity: str = "medium"
    ) -> Tuple[str, bool, str]:
        # 1. Primary Attempt: Gemini
        reply, ok = GeminiProvider.generate(system_prompt, history, user_message)
        if ok and reply:
            return (reply, True, "gemini")

        # 2. Secondary Attempt: OpenAI / OpenRouter
        reply_sec, ok_sec = SecondaryProvider.generate(system_prompt, history, user_message)
        if ok_sec and reply_sec:
            return (reply_sec, True, "secondary_llm")

        return ("", False, "offline_fallback")
