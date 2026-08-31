"""
AgroScan AI — Secondary LLM Provider (OpenAI / OpenRouter)
Secondary failover client for GPT-4o-mini and OpenRouter models.
"""

import logging
import httpx
from typing import List, Dict, Tuple
from app.core.config import settings

logger = logging.getLogger("agroscan")

class SecondaryProvider:
    """Invokes OpenAI or OpenRouter as failover/secondary reasoning engine."""

    OPENAI_URL = "https://api.openai.com/v1/chat/completions"
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        history: List[Dict[str, str]],
        user_message: str
    ) -> Tuple[str, bool]:
        api_key = settings.OPENAI_API_KEY or settings.OPENROUTER_API_KEY
        if not api_key:
            return ("", False)

        is_openrouter = api_key.startswith("sk-or-v1-")
        target_url = cls.OPENROUTER_URL if is_openrouter else cls.OPENAI_URL
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        if is_openrouter:
            headers["HTTP-Referer"] = "https://agroscan-ai.app"
            headers["X-Title"] = "AgroScan AI"

        model_name = "google/gemini-2.5-flash" if is_openrouter else "gpt-4o-mini"

        messages = [{"role": "system", "content": system_prompt}]
        for msg in history[-6:]:
            role = "user" if msg.get("role") in ["user", "human"] else "assistant"
            content = msg.get("content", "").strip()
            if content:
                messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": user_message})

        try:
            with httpx.Client(timeout=12.0) as client:
                res = client.post(
                    target_url,
                    headers=headers,
                    json={
                        "model": model_name,
                        "messages": messages,
                        "temperature": 0.3,
                        "max_tokens": 750
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices", [])
                    if choices:
                        content = choices[0].get("message", {}).get("content", "")
                        if content:
                            return (content.strip(), True)
        except Exception as e:
            logger.warning(f"Secondary LLM call error: {e}")

        return ("", False)
