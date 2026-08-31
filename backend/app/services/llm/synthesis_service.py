"""
AgroScan AI — Synthesis & Prompt Construction Service
Assembles evidence-grounded system prompts and performs deterministic domain synthesis.
"""

from typing import Dict, Any, Optional
from app.services.intent_service import AgriculturalIntent

class SynthesisService:
    """Constructs strict evidence-grounded prompts and fallback domain responses."""

    @classmethod
    def build_system_prompt(
        cls,
        question: str,
        rag_data: Dict[str, Any],
        research_data: Dict[str, Any],
        location_info: Optional[Dict[str, Any]],
        weather_info: Optional[Dict[str, Any]],
        language: str
    ) -> str:
        intent = rag_data["intent"]
        plant_name = rag_data["plant_name"]
        disease_name = rag_data["disease_name"]
        context_source = rag_data["context_source"]
        grounding_text = rag_data["grounding_text"]
        evidence_text = research_data.get("evidence_text", "")

        lang_instruction = (
            "LANGUAGE: Respond fluently and naturally in Marathi (Devanagari script: मराठी). "
            "Exception: Keep chemical/pesticide active ingredients (e.g. 'Copper Oxychloride 50% WP', 'Mancozeb 75% WP', 'Wettable Sulphur 80% WP', 'Neem Oil 3000ppm'), dosages (e.g. '2.5g/L', '4ml/L'), and scientific Latin botanical names in their original Latin/English form."
            if language == "mr"
            else "LANGUAGE: Respond in clear, farmer-friendly, scientifically rigorous English."
        )

        lines = [
            "You are AgroScan AI, a certified multi-source agricultural decision-support agronomist.",
            lang_instruction,
            "",
            "CRITICAL SCIENTIFIC GROUNDING & SAFETY RULES:",
            "1. Answer the user's ACTUAL question directly according to their detected intent.",
            "2. Never invent a scan, plant, disease, weather result, confidence score, location, pesticide dosage, or treatment.",
            "3. If a plant was manually selected by the user, describe it as selected (e.g. 'You selected Mango'), NOT scanned.",
            "4. If a real scan exists, use its actual diagnostic result. If no scan exists, do NOT assume one.",
            "5. Do NOT assume Tomato or Early Blight unless the user or scan explicitly refers to Tomato Early Blight.",
            "6. Do NOT repeat the same generic answer for different questions. Tailor your response strictly to the topic asked.",
            "7. For chemical recommendations, state active ingredients safely and advise following locally approved product labels.",
            "8. If the user asks a general or non-agricultural question (e.g. 'what is photosynthesis', 'what is 2+2'), answer it naturally and accurately.",
            f"DETECTED INTENT: {intent}",
            f"CONTEXT SOURCE: {context_source}"
        ]

        if plant_name:
            lines.append(f"RELEVANT PLANT: {plant_name}")
        if disease_name:
            lines.append(f"RELEVANT DISEASE: {disease_name}")

        if evidence_text:
            lines.append(f"\n{evidence_text}")

        if grounding_text:
            lines.append(f"\n--- LOCAL KNOWLEDGE GROUNDING ---\n{grounding_text}\n---------------------------------")

        if location_info:
            loc_str = f"{location_info.get('village', '')}, {location_info.get('district', '')}, {location_info.get('state', '')}".strip(', ')
            if loc_str:
                lines.append(f"FARM LOCATION: {loc_str}")

        if weather_info and weather_info.get("status") != "partially_available":
            temp = weather_info.get("temperature_c") or weather_info.get("temp_c")
            hum = weather_info.get("humidity_pct")
            rain = weather_info.get("rainfall_mm", 0.0)
            cond = weather_info.get("condition", "Current Weather")
            lines.append(
                f"LIVE LOCAL WEATHER: Condition: {cond} | Temp: {temp}°C | Humidity: {hum}% | Rain: {rain} mm"
            )

        return "\n".join(lines)

    @classmethod
    def synthesize_domain_fallback(
        cls,
        question: str,
        rag_data: Dict[str, Any],
        weather_info: Optional[Dict[str, Any]],
        language: str
    ) -> str:
        intent = rag_data["intent"]
        plant_info = rag_data["plant_info"]
        disease_info = rag_data["disease_info"]
        general_concept = rag_data["general_concept"]
        plant_name = rag_data["plant_name"] or "Crop"
        is_mr = language == "mr"

        if intent == AgriculturalIntent.GENERAL:
            q_clean = question.lower()
            if "2+2" in q_clean or "2 + 2" in q_clean:
                return "2 + 2 = 4."
            return (
                "नमस्कार! मी AgroScan AI कृषी सल्लागार आहे. आपल्या शेती, पीक आरोग्य, खते किंवा रोग व्यवस्थापनाविषयी प्रश्न विचारा."
                if is_mr
                else "Hello! I am AgroScan AI Agronomist. Ask me any question regarding your crops, soil, fertilizers, or disease management."
            )

        if general_concept:
            concept_name = general_concept["concept"]
            if "rotation" in concept_name.lower():
                return (
                    "🌾 **पिकांची फेरपालट (Crop Rotation) माहिती:**\n\n"
                    "**व्याख्या:** एकाच जमिनीत सलग एकच पीक न घेता हंगामानुसार विविध प्रकारची पिके आलटून-पालटून घेण्याच्या पद्धतीला 'पिकांची फेरपालट' म्हणतात.\n\n"
                    "**मुख्य फायदे:** रोग व कीड चक्र खंडित करणे, जमिनीची सुपीकता वाढवणे आणि अन्नद्रव्यांचा संतुलित वापर."
                    if is_mr
                    else "🌾 **Crop Rotation Guide:**\n\n"
                    "**Definition:** Crop rotation is the systematic practice of growing different types of crops sequentially on the same land across seasons.\n\n"
                    "**Key Principles:** Breaks pest and disease cycles, replenishes soil fertility via legumes, and optimizes nutrient stratification."
                )
            if "photosynthesis" in concept_name.lower():
                return (
                    "☀️ **प्रकाशसंश्लेषण (Photosynthesis) प्रक्रिया:**\n\n"
                    "**व्याख्या:** हिरव्या वनस्पती सूर्यप्रकाशाच्या उपस्थितीत हरितद्रव्याच्या साहाय्याने हवेतील CO2 आणि जमिनीतील पाणी वापरून ग्लुकोज (अन्न) तयार करतात आणि ऑक्सिजन बाहेर सोडतात.\n\n"
                    "**समीकरण:** 6 CO2 + 6 H2O + सूर्यप्रकाश ➔ C6H12O6 + 6 O2"
                    if is_mr
                    else "☀️ **Photosynthesis & Crop Physiology:**\n\n"
                    "**Definition:** Photosynthesis is the biological process by which green plants utilize chlorophyll to capture solar energy, converting carbon dioxide (CO2) and water (H2O) into glucose (energy) and releasing oxygen (O2).\n\n"
                    "**Chemical Equation:** 6 CO2 + 6 H2O + Light Energy ➔ C6H12O6 + 6 O2"
                )

        if intent == AgriculturalIntent.SOIL and plant_info:
            cname = plant_info["common_name"]
            return (
                f"🌱 **{cname} पिकासाठी योग्य माती व जमीन:**\n\n"
                f"- **मातीचा प्रकार:** {plant_info['soil']}\n"
                f"- **सामू (pH):** {plant_info['pH']}\n"
                f"- **हवामान:** {plant_info['climate']}"
                if is_mr
                else f"🌱 **Optimal Soil Requirements for {cname}:**\n\n"
                f"- **Soil Type:** {plant_info['soil']}\n"
                f"- **Soil pH Range:** {plant_info['pH']}\n"
                f"- **Climate Suitability:** {plant_info['climate']}"
            )

        if intent == AgriculturalIntent.IRRIGATION and plant_info:
            cname = plant_info["common_name"]
            return (
                f"💧 **{cname} पिकाचे पाणी व्यवस्थापन:**\n\n"
                f"- **सिंचन वेळापत्रक:** {plant_info['irrigation']}\n"
                f"- **पाऊस व गरज:** {plant_info['rainfall']}"
                if is_mr
                else f"💧 **Irrigation Management for {cname}:**\n\n"
                f"- **Irrigation Schedule:** {plant_info['irrigation']}\n"
                f"- **Water Requirement & Rainfall:** {plant_info['rainfall']}"
            )

        if intent in [AgriculturalIntent.FERTILIZER, AgriculturalIntent.NUTRITION] and plant_info:
            cname = plant_info["common_name"]
            return (
                f"🧪 **{cname} खत व्यवस्थापन:**\n\n"
                f"- **खतांचे प्रमाण व वेळापत्रक:** {plant_info['fertilizer']}"
                if is_mr
                else f"🧪 **Fertilizer Protocol for {cname}:**\n\n"
                f"- **Nutrient Schedule:** {plant_info['fertilizer']}"
            )

        if intent == AgriculturalIntent.HARVESTING and plant_info:
            cname = plant_info["common_name"]
            return (
                f"🌾 **{cname} काढणीची वेळ व पद्धत:**\n\n"
                f"- **काढणीची लक्षणे:** {plant_info['harvesting']}\n"
                f"- **साठवणूक:** {plant_info['post_harvest']}"
                if is_mr
                else f"🌾 **Harvesting Guidelines for {cname}:**\n\n"
                f"- **Maturity Indicators:** {plant_info['harvesting']}\n"
                f"- **Post-Harvest & Storage:** {plant_info['post_harvest']}"
            )

        if disease_info:
            dname = disease_info["disease_name"]
            if intent in [AgriculturalIntent.DISEASE_SYMPTOMS, AgriculturalIntent.DISEASE_IDENTIFICATION]:
                return (
                    f"🔍 **{dname} रोगाची लक्षणे:**\n\n{disease_info['symptoms']}"
                    if is_mr
                    else f"🔍 **Symptoms of {dname}:**\n\n{disease_info['symptoms']}"
                )
            if intent == AgriculturalIntent.DISEASE_PREVENTION:
                return (
                    f"🛡️ **{dname} प्रतिबंधक उपाय:**\n\n{disease_info['prevention']}"
                    if is_mr
                    else f"🛡️ **Prevention of {dname}:**\n\n{disease_info['prevention']}"
                )
            if intent == AgriculturalIntent.DISEASE_TREATMENT:
                return (
                    f"💊 **{dname} नियंत्रण व उपचार:**\n\n"
                    f"1. **जैविक उपाय:** {disease_info['biological_control']}\n\n"
                    f"2. **रासायनिक उपाय:** {disease_info['chemical_management']}\n\n"
                    f"3. **सुरक्षा सूचना:** {disease_info['safety_notes']}"
                    if is_mr
                    else f"💊 **Management Protocol for {dname}:**\n\n"
                    f"1. **Biological Control:** {disease_info['biological_control']}\n\n"
                    f"2. **Chemical Management:** {disease_info['chemical_management']}\n\n"
                    f"3. **Safety & Label Notes:** {disease_info['safety_notes']}"
                )

        if is_mr:
            return f"🌾 **AgroScan AI कृषी सल्लागार ({plant_name}):**\n\nतुमच्या प्रश्नानुसार ('{question}'), योग्य मशागत, पाण्याचा निचरा आणि संतुलित खत व्यवस्थापन आवश्यक आहे."
        return f"🌾 **AgroScan AI Agronomist ({plant_name}):**\n\nRegarding your query ('{question}'): For optimal {plant_name} health, ensure balanced soil nutrition, proper irrigation, and regular monitoring."
