"""
AgroScan AI — Gemini Provider
Client interface for Google Gemini API models (3.5-flash-lite, 3.5-flash, 3.1-flash-lite).
"""

import logging
import httpx
from typing import List, Dict, Tuple
from app.core.config import settings

logger = logging.getLogger("agroscan")

class GeminiProvider:
    """Invokes Google Gemini API with system instructions and conversation context."""

    MODELS = [
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite"
    ]

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
                "maxOutputTokens": 600
            }
        }

        for model in cls.MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            try:
                with httpx.Client(timeout=14.0) as client:
                    res = client.post(url, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts and "text" in parts[0]:
                                text = parts[0]["text"].strip()
                                if text:
                                    return (text, True)
            except Exception as e:
                logger.warning(f"Gemini call error ({model}): {e}")

        return ("", False)
