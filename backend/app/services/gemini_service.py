import google.generativeai as genai
from app.core.config import settings

class GeminiAssistantService:
    """
    Backend service proxy for Google Gemini API.
    Provides conversational agronomic advice while strictly respecting decision-support disclaimers.
    """

    @staticmethod
    def generate_chat_response(user_message: str, scan_context: dict = None) -> str:
        if not settings.GEMINI_API_KEY:
            return GeminiAssistantService._fallback_response(user_message, scan_context)

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')

            system_instruction = (
                "You are AgroScan AI Agronomist, a helpful smart farming assistant. "
                "Provide clear, practical advice for crop disease control, soil health, and weather risks. "
                "Strictly adhere to approved organic remedies and standard chemical treatments without inventing custom dosages. "
                "Always add a brief note encouraging farmers to check local product labels."
            )

            context_prompt = ""
            if scan_context:
                context_prompt = (
                    f"Current Scan Context:\n"
                    f"- Crop: {scan_context.get('crop_detected')}\n"
                    f"- Detected Disease: {scan_context.get('disease_name')}\n"
                    f"- Severity: {scan_context.get('severity_level')} ({scan_context.get('severity_percentage')}%)\n"
                    f"- Weather Risk: {scan_context.get('weather_risk_level')}\n\n"
                )

            full_prompt = f"{system_instruction}\n\n{context_prompt}Farmer Question: {user_message}"
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return GeminiAssistantService._fallback_response(user_message, scan_context, str(e))

    @staticmethod
    def _fallback_response(user_message: str, scan_context: dict = None, error: str = None) -> str:
        if scan_context and scan_context.get("disease_name"):
            disease = scan_context.get("disease_name")
            return (
                f"**AgroScan AI Assistant (Offline Mode)**:\n\n"
                f"For **{disease}**, we recommend:\n"
                f"1. **Immediate Step**: Remove severely infected leaves to halt spore spread.\n"
                f"2. **Organic Option**: Apply copper-based fungicide or neem oil spray.\n"
                f"3. **Prevention**: Avoid overhead watering during evening hours and ensure proper plant spacing.\n\n"
                f"*Note: For custom questions, configure your GEMINI_API_KEY in the backend `.env` file.*"
            )
        return (
            "**AgroScan AI Assistant**: Welcome to AgroScan AI! Ask me any question regarding crop diseases, organic remedies, or weather risks. "
            "For full conversational capabilities, ensure your backend `.env` includes a valid GEMINI_API_KEY."
        )
