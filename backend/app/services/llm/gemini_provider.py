"""
AgroScan AI — Gemini Provider
Client interface for Google Gemini 1.5 Flash and Gemini 2.5 Flash.
"""

import logging
import httpx
from typing import List, Dict, Tuple
from app.core.config import settings

logger = logging.getLogger("agroscan")

class GeminiProvider:
    """Invokes Google Gemini API with system instructions and conversation context."""

    GEMINI_15_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    GEMINI_25_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        history: List[Dict[str, str]],
        user_message: str
    ) -> Tuple[str, bool]:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return ("", False)

        contents = []
        for msg in history[-6:]:
            role = "user" if msg.get("role") in ["user", "human"] else "model"
            content = msg.get("content", "").strip()
            if content:
                contents.append({"role": role, "parts": [{"text": content}]})

        contents.append({"role": "user", "parts": [{"text": user_message}]})

        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 750
            }
        }

        for url in [cls.GEMINI_15_URL, cls.GEMINI_25_URL]:
            try:
                with httpx.Client(timeout=12.0) as client:
                    res = client.post(f"{url}?key={api_key}", json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts and "text" in parts[0]:
                                return (parts[0]["text"].strip(), True)
            except Exception as e:
                logger.warning(f"Gemini call error ({url}): {e}")

        return ("", False)
