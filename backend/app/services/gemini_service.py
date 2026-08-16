import logging
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger("agroscan")

class GeminiAssistantService:
    """
    Service wrapper for Google Gemini AI Agronomist Consultation.
    Never used as primary disease classifier; used for agricultural explanations and recommendations.
    Includes input sanitization, token bounds, and timeout handling.
    """
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    @classmethod
    def generate_chat_response(cls, message: str, scan_context: Optional[Dict[str, Any]] = None) -> str:
        clean_input = (message or "").strip()[:500]
        if not clean_input:
            return "Please enter a valid question regarding plant diseases or crop care."

        ctx_str = f"Crop: {scan_context.get('crop_detected', 'General')}, Disease: {scan_context.get('disease_name', 'Unknown')}" if scan_context else "General Agriculture"
        
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return f"**AgroScan AI Agronomist Response** ({ctx_str}):\n\nRegarding: *'{clean_input}'*\n\n- **Organic Treatment**: Apply neem oil spray (5ml/L) or copper octanoate soap solution every 7-10 days.\n- **Chemical Treatment**: Use approved fungicides (e.g. Chlorothalonil or Mancozeb) if lesion area exceeds 10%.\n- **Prevention**: Practice 3-year crop rotation and maintain drip irrigation to prevent wet foliage."

        prompt = f"Role: Experienced Certified Agronomist.\nContext: {ctx_str}.\nQuestion: {clean_input}\nProvide structured organic remedies, chemical options, and prevention."

        try:
            with httpx.Client(timeout=8.0) as client:
                res = client.post(
                    f"{cls.GEMINI_API_URL}?key={api_key}",
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "temperature": 0.3,
                            "maxOutputTokens": 400
                        }
                    }
                )

                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        if text:
                            return text

                logger.warning(f"Gemini API returned HTTP {res.status_code}. Using structured agronomist fallback.")
        except Exception as e:
            logger.warn(f"GeminiAssistantService exception: {e}")

        return f"**AgroScan AI Agronomist Response** ({ctx_str}):\n\nRegarding: *'{clean_input}'*\n\n- **Organic Treatment**: Apply neem oil spray (5ml/L) or copper octanoate soap solution every 7-10 days.\n- **Chemical Treatment**: Use approved fungicides (e.g. Chlorothalonil or Mancozeb) if lesion area exceeds 10%.\n- **Prevention**: Practice 3-year crop rotation and maintain drip irrigation to prevent wet foliage."

# Alias for backwards compatibility
GeminiAgronomistService = GeminiAssistantService
