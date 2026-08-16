import logging
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger("agroscan")

class AIProviderService:
    """
    Dual-Provider AI Assistant Service for AgroScan AI.
    Executes primary AI provider (Gemini or OpenAI) with automatic failover to the secondary provider.
    Ensures strict grounding in scan context and localized Agronomist system prompts.
    """

    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    GEMINI_FALLBACK_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    OPENAI_URL = "https://api.openai.com/v1/chat/completions"

    @classmethod
    def generate_response(
        cls,
        message: str,
        scan_context: Optional[Dict[str, Any]] = None,
        language: str = "en",
        is_manual: bool = False
    ) -> str:
        clean_input = (message or "").strip()[:600]
        if not clean_input:
            return "कृपया पीक आरोग्य किंवा रोगाबद्दल प्रश्न विचारा." if language == "mr" else "Please enter a valid question regarding plant disease or crop care."

        system_prompt, user_prompt = cls._build_prompts(clean_input, scan_context, language, is_manual)

        primary = (settings.AI_PROVIDER or "gemini").lower()
        fallback = "openai" if primary == "gemini" else "gemini"

        # 1. Try Primary Provider
        reply, success = cls._call_provider(primary, system_prompt, user_prompt, language)
        if success and reply:
            logger.info(f"AI Assistant message answered by PRIMARY provider [{primary}].")
            return reply

        # 2. Failover to Secondary Provider
        logger.warning(f"Primary AI provider [{primary}] failed or unconfigured. Triggering fallback [{fallback}].")
        reply_fallback, success_fb = cls._call_provider(fallback, system_prompt, user_prompt, language)
        if success_fb and reply_fallback:
            logger.info(f"AI Assistant message answered by FALLBACK provider [{fallback}].")
            return reply_fallback

        # 3. Clean error state when both providers fail
        if language == "mr":
            return (
                "**AgroScan AI कृषी सल्लागार प्रणाली तात्पुरती उपलब्ध नाही.**\n\n"
                "कृपया थोड्या वेळाने पुन्हा प्रयत्न करा. तात्काळ सल्ला मिळवण्यासाठी आपल्या स्थानिक कृषी विज्ञान केंद्राशी संपर्क साधा."
            )
        else:
            return (
                "**AgroScan AI Agronomist Service Temporarily Unavailable.**\n\n"
                "Please try asking your question again in a moment. For urgent crop health issues, consult your local Agricultural Extension Service."
            )

    @classmethod
    def _call_provider(cls, provider: str, system_prompt: str, user_prompt: str, language: str) -> tuple[str, bool]:
        if provider == "gemini":
            return cls._call_gemini(system_prompt, user_prompt)
        elif provider == "openai":
            return cls._call_openai(system_prompt, user_prompt)
        return ("", False)

    @classmethod
    def _call_gemini(cls, system_prompt: str, user_prompt: str) -> tuple[str, bool]:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return ("", False)

        combined_prompt = f"{system_prompt}\n\nUser Question: {user_prompt}"

        for url in [cls.GEMINI_URL, cls.GEMINI_FALLBACK_URL]:
            try:
                with httpx.Client(timeout=10.0) as client:
                    res = client.post(
                        f"{url}?key={api_key}",
                        json={
                            "contents": [{"parts": [{"text": combined_prompt}]}],
                            "generationConfig": {
                                "temperature": 0.35,
                                "maxOutputTokens": 500
                            }
                        }
                    )
                    if res.status_code == 200:
                        data = res.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts and "text" in parts[0]:
                                return (parts[0]["text"].strip(), True)
            except Exception as e:
                logger.warning(f"Gemini API attempt error ({url}): {e}")

        return ("", False)

    @classmethod
    def _call_openai(cls, system_prompt: str, user_prompt: str) -> tuple[str, bool]:
        api_key = settings.OPENAI_API_KEY or settings.OPENROUTER_API_KEY
        if not api_key:
            return ("", False)

        is_openrouter = api_key.startswith("sk-or-v1-")
        target_url = "https://openrouter.ai/api/v1/chat/completions" if is_openrouter else cls.OPENAI_URL
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        if is_openrouter:
            headers["HTTP-Referer"] = "https://agroscan-ai.app"
            headers["X-Title"] = "AgroScan AI"

        model_name = "google/gemini-2.5-flash" if is_openrouter else "gpt-4o-mini"

        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.post(
                    target_url,
                    headers=headers,
                    json={
                        "model": model_name,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.35,
                        "max_tokens": 500
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
            logger.warning(f"OpenAI/OpenRouter API call error: {e}")

        return ("", False)

    @classmethod
    def _build_prompts(
        cls,
        question: str,
        ctx: Optional[Dict[str, Any]],
        language: str,
        is_manual: bool
    ) -> tuple[str, str]:
        lang_str = "Marathi (मराठी). Write responses in natural, clear Marathi suitable for Indian smallholder farmers." if language == "mr" else "English."

        if ctx:
            plant_name = ctx.get("crop_detected") or ctx.get("plantName") or "Crop"
            scientific_name = ctx.get("scientific_name") or ctx.get("scientificName") or "N/A"
            disease_status = ctx.get("disease_name") or ctx.get("diseaseStatus") or "General Health"
            severity = ctx.get("severity_level") or "Standard"
            confidence = ctx.get("confidence_score") or ctx.get("plantConfidence") or "High"
            farm = ctx.get("farmName") or "Local Farm"

            if is_manual:
                context_block = f"User selected plant species: '{plant_name}' ({scientific_name}). Note: This plant was typed/selected manually, NOT scanned."
                system_prompt = (
                    f"You are AgroScan AI, an expert agricultural advisor for Indian farmers.\n"
                    f"Context: {context_block}\n"
                    f"Language requirement: {lang_str}\n"
                    f"Instructions: Explicitly address the user by stating 'You selected {plant_name}'. Do NOT claim that this plant was scanned or diagnosed for diseases."
                )
            else:
                context_block = (
                    f"Scanned Plant: {plant_name} ({scientific_name})\n"
                    f"Diagnostic Disease Status: {disease_status}\n"
                    f"Confidence Probability: {confidence}\n"
                    f"Severity Level: {severity}\n"
                    f"Farm: {farm}"
                )
                system_prompt = (
                    f"You are AgroScan AI, an expert certified Agronomist for Indian smallholder farmers.\n"
                    f"REAL SCAN DIAGNOSTIC DATA:\n{context_block}\n\n"
                    f"Language requirement: {lang_str}\n"
                    f"Instructions:\n"
                    f"1. Ground your answer ONLY in the scanned plant ({plant_name}) and detected condition ({disease_status}).\n"
                    f"2. Provide practical, actionable guidance including organic remedies (e.g. neem oil, compost tea), chemical options, and prevention.\n"
                    f"3. Never assume a different crop or disease than provided in the scan data."
                )
        else:
            system_prompt = (
                f"You are AgroScan AI, a helpful certified Agronomist for Indian farmers.\n"
                f"Language requirement: {lang_str}\n"
                f"Instructions: Provide practical advice on crop care, organic remedies, soil health, and pest management. Do not fabricate scan results."
            )

        return (system_prompt, question)
