import time
import json
import base64
import logging
import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.core.config import settings
from app.services.disease_knowledge_base import get_disease_by_code
from app.services.providers.base_provider import (
    DiseaseDetectionProvider, ProviderDiagnosisResult, PredictionCandidate
)

logger = logging.getLogger("agroscan")

class OpenRouterVisionProvider(DiseaseDetectionProvider):
    """
    OpenRouter / OpenAI Vision AI Diagnostic Provider.
    Executes actual multimodal computer vision disease classification using
    multimodal vision models (Gemini Flash / GPT-4o-mini) via configured OpenRouter/OpenAI API.
    Provides verified plant identification, pathology detection, confidence scoring, and alternatives.
    """

    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    OPENAI_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self):
        super().__init__(name="openrouter_vision", display_name="AgroScan Vision AI Engine")

    def is_available(self) -> bool:
        key = settings.OPENROUTER_API_KEY or settings.OPENAI_API_KEY
        return bool(key) and not getattr(settings, "DEMO_MODE", False)

    async def diagnose(
        self,
        image_bytes: bytes,
        plant_name: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None,
        language: str = "en"
    ) -> ProviderDiagnosisResult:
        self.total_calls += 1
        t0 = time.time()

        api_key = settings.OPENROUTER_API_KEY or settings.OPENAI_API_KEY
        if not api_key:
            return ProviderDiagnosisResult(
                provider=self.name,
                status="not_configured",
                plant="Unknown",
                disease="Unknown",
                disease_code="unconfigured_provider",
                confidence=0.0,
                error="OpenRouter/OpenAI vision API key is not configured."
            )

        is_openrouter = api_key.startswith("sk-or-v1-")
        target_url = self.OPENROUTER_URL if is_openrouter else self.OPENAI_URL
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        if is_openrouter:
            headers["HTTP-Referer"] = "https://agroscan-ai.app"
            headers["X-Title"] = "AgroScan AI"

        model_name = "google/gemini-2.5-flash" if is_openrouter else "gpt-4o-mini"
        b64_img = base64.b64encode(image_bytes).decode("utf-8")

        prompt = (
            "You are an expert plant pathologist and agronomic computer vision model.\n"
            "Analyze this crop leaf photograph carefully and diagnose the plant and disease.\n"
            "Return a strictly valid JSON object ONLY (no markdown formatting, no code fencing, no extra text):\n"
            "{\n"
            '  "is_plant": true,\n'
            '  "is_leaf": true,\n'
            '  "plant": "Exact crop name (e.g. Tomato, Potato, Corn, Cotton, Sugarcane, Soybean, Rice, Wheat, Grapes, Mango)",\n'
            '  "scientific_name": "Latin botanical name",\n'
            '  "disease": "Specific disease name or \'Healthy Leaf (No Disease Detected)\'",\n'
            '  "disease_code": "snake_case_disease_code",\n'
            '  "confidence": 0.92,\n'
            '  "is_healthy": false,\n'
            '  "symptoms": "Brief 1-sentence visible lesion description",\n'
            '  "alternatives": [\n'
            '     {"disease": "Alternative Disease", "disease_code": "alt_code", "confidence": 0.15}\n'
            "  ]\n"
            "}\n"
        )
        if plant_name and plant_name not in ["Crop", "General", "General Crop", "Unknown"]:
            prompt += f"Note: The farmer indicated this is a {plant_name} crop.\n"

        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_img}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.2,
            "max_tokens": 400
        }

        try:
            async with httpx.AsyncClient(timeout=7.5) as client:
                res = await client.post(target_url, headers=headers, json=payload)
                latency = (time.time() - t0) * 1000.0
                self.last_latency_ms = latency

                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices", [])
                    if choices:
                        content = choices[0].get("message", {}).get("content", "").strip()
                        # Strip accidental markdown fencing
                        if content.startswith("```"):
                            lines = content.split("\n")
                            if lines[0].startswith("```"):
                                lines = lines[1:]
                            if lines and lines[-1].startswith("```"):
                                lines = lines[:-1]
                            content = "\n".join(lines).strip()

                        try:
                            parsed = json.loads(content)
                            if parsed.get("is_leaf") is False or parsed.get("is_plant") is False:
                                return ProviderDiagnosisResult(
                                    provider=self.name,
                                    status="non_leaf_detected",
                                    plant="Non-Plant",
                                    disease="Non-Plant",
                                    disease_code="non_plant",
                                    confidence=0.0,
                                    latency_ms=round(latency, 1),
                                    error="Vision AI determined this image does not contain a plant leaf."
                                )

                            plant = parsed.get("plant", "General Crop").strip().title()
                            disease = parsed.get("disease", "Healthy Leaf").strip().title()
                            disease_code = parsed.get("disease_code", "").strip().lower().replace("-", "_").replace(" ", "_")
                            if not disease_code:
                                disease_code = disease.lower().replace(" ", "_").replace("-", "_")
                            
                            confidence = max(0.40, min(0.99, float(parsed.get("confidence", 0.85))))
                            is_healthy = bool(parsed.get("is_healthy", False)) or ("healthy" in disease.lower())
                            sci_name = parsed.get("scientific_name", "N/A")

                            alts = []
                            for alt in parsed.get("alternatives", []):
                                if isinstance(alt, dict) and alt.get("disease"):
                                    alts.append(PredictionCandidate(
                                        crop=plant,
                                        disease_name=alt["disease"].strip().title(),
                                        disease_code=alt.get("disease_code", alt["disease"].lower().replace(" ", "_")),
                                        confidence=float(alt.get("confidence", 0.15)),
                                        is_healthy=False
                                    ))

                            self.last_success_at = datetime.now(timezone.utc)
                            return ProviderDiagnosisResult(
                                provider=self.name,
                                status="success",
                                plant=plant,
                                scientific_name=sci_name,
                                disease=disease,
                                disease_code=disease_code,
                                confidence=round(confidence, 3),
                                is_healthy=is_healthy,
                                top_predictions=[
                                    PredictionCandidate(
                                        crop=plant,
                                        disease_name=disease,
                                        disease_code=disease_code,
                                        confidence=round(confidence, 3),
                                        is_healthy=is_healthy,
                                        scientific_name=sci_name
                                    )
                                ] + alts,
                                latency_ms=round(latency, 1),
                                is_demo=False
                            )
                        except json.JSONDecodeError as jde:
                            logger.warning(f"Failed to decode Vision AI JSON: {jde} | raw: {content[:100]}")

                self.failure_count += 1
                return ProviderDiagnosisResult(
                    provider=self.name,
                    status="error",
                    plant="Unknown",
                    disease="Unknown",
                    disease_code="vision_api_error",
                    confidence=0.0,
                    latency_ms=round(latency, 1),
                    error=f"Vision API returned HTTP {res.status_code}: {res.text[:120]}"
                )
        except Exception as e:
            self.failure_count += 1
            latency = (time.time() - t0) * 1000.0
            self.last_latency_ms = latency
            logger.warning(f"OpenRouterVisionProvider error: {e}")
            return ProviderDiagnosisResult(
                provider=self.name,
                status="error",
                plant="Unknown",
                disease="Unknown",
                disease_code="vision_api_error",
                confidence=0.0,
                latency_ms=round(latency, 1),
                error=f"Vision AI call failed: {e}"
            )
