import time
import json
import base64
import logging
import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.core.config import settings
from app.services.providers.base_provider import (
    DiseaseDetectionProvider, ProviderDiagnosisResult, PredictionCandidate
)

logger = logging.getLogger("agroscan")

class GeminiVisionProvider(DiseaseDetectionProvider):
    """
    Google Gemini Multimodal Vision AI Diagnostic Provider.
    Analyzes crop leaf photographs to identify the exact plant species (e.g. Mango,
    Sugarcane, Cotton, Soybean, Rice, Wheat, Chilli, Onion, Grape, Banana, Tomato, Potato,
    or any plant in the world), botanical scientific name, family, and pathological health state.
    """

    GEMINI_MODELS = [
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
    ]

    def __init__(self):
        super().__init__(name="gemini_vision", display_name="Google Gemini Vision AI")

    def is_available(self) -> bool:
        return bool(settings.GEMINI_API_KEY) and not getattr(settings, "DEMO_MODE", False)

    async def diagnose(
        self,
        image_bytes: bytes,
        plant_name: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None,
        language: str = "en",
        local_hypothesis: Optional[Dict[str, Any]] = None
    ) -> ProviderDiagnosisResult:
        self.total_calls += 1
        t0 = time.time()

        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return ProviderDiagnosisResult(
                provider=self.name,
                status="not_configured",
                plant="Unknown",
                disease="Unknown",
                disease_code="unconfigured_provider",
                confidence=0.0,
                error="Google Gemini API key is not configured."
            )

        b64_img = base64.b64encode(image_bytes).decode("utf-8")

        prompt = (
            "You are a premier world-class agricultural botanist and plant pathologist.\n"
            "Analyze this crop foliage/leaf photograph with high scientific precision.\n\n"
            "TASK 1 — BOTANICAL CROP IDENTIFICATION (CRITICAL DISCRIMINATION):\n"
            "- Accurately identify the exact plant species and botanical scientific name.\n"
            "- CEREAL & MONOCOT DISCRIMINATION: Pay extreme attention to distinguish between visually similar cereal crops:\n"
            "  * Corn / Maize (Zea mays): Broad, wide blade (>3 cm), thick pale central midrib, wavy undulating margin.\n"
            "  * Wheat (Triticum aestivum): Slender, narrow grass blade (1-2 cm), fine parallel venation, claw-like auricles clasping sheath.\n"
            "  * Rice / Paddy (Oryza sativa): Rough scabrous texture, long acute ligule, erect blade.\n"
            "  * Sugarcane (Saccharum officinarum): Very thick white midvein, micro-serrated margin, arching blade.\n"
            "  * Other crops: Cotton, Soybean, Tomato, Potato, Chilli/Pepper, Onion, Mango, Grape, Banana, Rose, Papaya, Pomegranate, Citrus, etc.\n\n"
            "TASK 2 — HEALTH STATUS & PATHOLOGY ASSESSMENT (HEALTHY vs. DISEASED):\n"
            "- Examine the leaf surface meticulously for genuine active pathological lesions.\n"
            "- If the leaf foliage is green and healthy without fungal pustules, necrotic spots, chlorotic halos, or powdery mildew "
            "(even if natural shadows, surface dust, or mechanical tears exist), YOU MUST CLASSIFY AS HEALTHY: "
            "set 'is_healthy': true and 'disease': 'Healthy Leaf (No Disease Detected)'.\n"
            "- Do NOT diagnose healthy leaves as diseased.\n"
            "- If real disease symptoms are present, specify the exact pathogen/disease name.\n\n"
        )

        if local_hypothesis:
            lh_crop = local_hypothesis.get("crop", "Unknown")
            lh_dis = local_hypothesis.get("disease", "Unknown")
            lh_healthy = local_hypothesis.get("is_healthy", False)
            prompt += (
                f"TASK 3 — PRELIMINARY LOCAL MODEL CROSS-EXAMINATION:\n"
                f"- A preliminary local model hypothesized: Crop='{lh_crop}', Condition='{lh_dis}' (Healthy: {lh_healthy}).\n"
                f"- Validate whether this local hypothesis is correct or erroneous. "
                f"Is the crop truly {lh_crop} or is it another species (e.g. Corn vs Wheat)? Is the condition actually {lh_dis} or is the leaf Healthy?\n"
                f"- State clearly in 'agrees_with_local' (true/false) and 'validation_notes'.\n\n"
            )

        if plant_name and plant_name not in ["Crop", "General", "General Crop", "Unknown", "auto", "Auto-Detect"]:
            prompt += f"Note: The farmer indicated this may be a '{plant_name}' crop.\n\n"

        prompt += (
            "Return STRICT JSON ONLY (no markdown fences, raw JSON):\n"
            "{\n"
            '  "is_plant": true,\n'
            '  "plant": "Exact crop name (e.g. Corn, Wheat, Mango, Rice, Cotton, Sugarcane, Tomato, etc.)",\n'
            '  "scientific_name": "Botanical Latin name",\n'
            '  "disease": "Specific disease name or \'Healthy Leaf (No Disease Detected)\'",\n'
            '  "disease_code": "snake_case_disease_code",\n'
            '  "confidence": 0.95,\n'
            '  "is_healthy": false,\n'
            '  "agrees_with_local": true,\n'
            '  "validation_notes": "Detailed diagnostic notes validating or correcting the leaf health and crop species",\n'
            '  "symptoms": "Brief description of visible leaf surface characteristics"\n'
            "}\n"
        )

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": b64_img
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 400
            }
        }

        urls_to_try = self.GEMINI_MODELS
        last_error = ""

        for url in urls_to_try:
            try:
                async with httpx.AsyncClient(timeout=25.0) as client:
                    res = await client.post(f"{url}?key={api_key}", json=payload)
                    latency = (time.time() - t0) * 1000.0
                    self.last_latency_ms = latency

                    if res.status_code == 200:
                        data = res.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
                            # Clean markdown if present
                            if raw_text.startswith("```"):
                                lines = raw_text.split("\n")
                                if lines[0].startswith("```"):
                                    lines = lines[1:]
                                if lines and lines[-1].startswith("```"):
                                    lines = lines[:-1]
                                raw_text = "\n".join(lines).strip()

                            parsed = json.loads(raw_text)
                            if parsed.get("is_plant") is False:
                                return ProviderDiagnosisResult(
                                    provider=self.name,
                                    status="non_leaf_detected",
                                    plant="Non-Plant",
                                    disease="Non-Plant",
                                    disease_code="non_plant",
                                    confidence=0.0,
                                    latency_ms=round(latency, 1),
                                    error="Gemini Vision detected this image is not a plant."
                                )

                            plant = parsed.get("plant", "General Crop").strip().title()
                            sci_name = parsed.get("scientific_name", "N/A")
                            disease = parsed.get("disease", "Healthy Leaf").strip().title()
                            disease_code = parsed.get("disease_code", "").strip().lower().replace("-", "_").replace(" ", "_")
                            if not disease_code:
                                disease_code = disease.lower().replace(" ", "_").replace("-", "_")

                            confidence = max(0.50, min(0.99, float(parsed.get("confidence", 0.90))))
                            is_healthy = bool(parsed.get("is_healthy", False)) or ("healthy" in disease.lower())

                            alts = []
                            for alt in parsed.get("alternatives", []):
                                if isinstance(alt, dict) and alt.get("disease"):
                                    alts.append(PredictionCandidate(
                                        crop=plant,
                                        disease_name=alt["disease"].strip().title(),
                                        disease_code=alt.get("disease_code", alt["disease"].lower().replace(" ", "_")),
                                        confidence=float(alt.get("confidence", 0.10)),
                                        is_healthy=False
                                    ))

                            self.last_success_at = datetime.now(timezone.utc)
                            raw_ref_meta = {
                                "validation_notes": parsed.get("validation_notes", ""),
                                "agrees_with_local": parsed.get("agrees_with_local", True),
                                "symptoms": parsed.get("symptoms", "")
                            }
                            return ProviderDiagnosisResult(
                                provider=self.name,
                                status="success",
                                plant=plant,
                                scientific_name=sci_name,
                                disease=disease,
                                disease_code=disease_code,
                                confidence=round(confidence, 3),
                                is_healthy=is_healthy,
                                raw_reference=json.dumps(raw_ref_meta),
                                top_predictions=[
                                    PredictionCandidate(
                                        crop=plant,
                                        disease_name=disease,
                                        disease_code=disease_code,
                                        confidence=round(confidence, 3),
                                        is_healthy=is_healthy,
                                        scientific_name=sci_name,
                                        symptoms_summary=parsed.get("symptoms")
                                    ),
                                    *alts
                                ],
                                latency_ms=round(latency, 1),
                                is_demo=False
                            )
                    else:
                        last_error = f"HTTP {res.status_code}: {res.text[:120]}"
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Gemini Vision call failed on {url}: {e}")

        self.failure_count += 1
        return ProviderDiagnosisResult(
            provider=self.name,
            status="error",
            plant="Unknown",
            disease="Unknown",
            disease_code="gemini_error",
            confidence=0.0,
            error=f"Gemini Vision diagnostic failed: {last_error}",
            latency_ms=round((time.time() - t0) * 1000.0, 1)
        )
