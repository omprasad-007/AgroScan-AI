"""
AgroScan AI — Synthesis & Prompt Construction Service
Assembles evidence-grounded system prompts and performs deterministic domain synthesis
with question-category specific templates in English and Marathi.
"""

from typing import Dict, Any, Optional
from app.services.intent_service import AgriculturalIntent

class SynthesisService:
    """Constructs strict evidence-grounded prompts and multi-template domain responses."""

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
            "8. If the user asks an irrigation, fertilizer, soil, planting, or harvesting question, focus on crop management and do NOT lecture on unrelated diseases.",
            "9. If the user asks a general or non-agricultural question (e.g. 'what is photosynthesis', 'what is 2+2'), answer it naturally and accurately.",
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
        elif intent in [AgriculturalIntent.WEATHER, AgriculturalIntent.WEATHER_DISEASE_RISK]:
            lines.append("NOTE: Real-time weather data is currently unavailable. State this limitation clearly.")

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
        plant_info = rag_data.get("plant_info")
        disease_info = rag_data.get("disease_info")
        general_concept = rag_data.get("general_concept")
        plant_name = rag_data.get("plant_name") or "Crop"
        is_mr = language == "mr"
        q_clean = question.lower().strip()

        # 1. Non-Agri / Math / Greetings
        if intent == AgriculturalIntent.GENERAL:
            if "2+2" in q_clean or "2 + 2" in q_clean:
                return "2 + 2 = 4."
            return (
                "नमस्कार! मी AgroScan AI कृषी सल्लागार आहे. आपल्या शेती, पीक आरोग्य, खते किंवा रोग व्यवस्थापनाविषयी प्रश्न विचारा."
                if is_mr
                else "Hello! I am AgroScan AI Agronomist. Ask me any question regarding your crops, soil, fertilizers, or disease management."
            )

        # 2. Comparative Pathology: Early Blight vs Late Blight
        if ("difference" in q_clean or "तुलना" in q_clean or "फरक" in q_clean) and "early" in q_clean and "late" in q_clean:
            return (
                "🔬 **करपा रोगांचे प्रकार व तुलना (Early Blight vs. Late Blight):**\n\n"
                "1. **अल्टरनेरिया करपा / लवकर येणारा करपा (*Alternaria solani*):** जुन्या पानांवर गडद तपकिरी गोलाकार चक्राकार (concentric rings / target board) डाग पडतात. उबदार हवामानात (२४-२९°C) प्रादुर्भाव वाढतो.\n\n"
                "2. **फायटोफ्थोरा करपा / उशिरा येणारा करपा (*Phytophthora infestans*):** पानांवर जलमय काळे डाग पडतात व पानांच्या खालच्या बाजूस पांढरी बुरशी (downy mildew / mold) दिसते. थंड व दमट हवामानात (१५-२२°C, आर्द्रता >८५%) संपूर्ण पीक काही दिवसांत करपून जाते."
                if is_mr
                else "🔬 **Diagnostic Comparison: Early Blight vs. Late Blight:**\n\n"
                "1. **Early Blight (*Alternaria solani*):** Characterized by dark brown concentric 'target-board' or bullseye rings primarily on older lower leaves. Favors warm temperatures (24-29°C).\n\n"
                "2. **Late Blight (*Phytophthora infestans*):** Characterized by rapid water-soaked, dark greasy lesions with delicate white downy mold on leaf undersides during cool, humid weather (15-22°C, RH>85%). Causes rapid foliar collapse."
            )

        # 3. General Agricultural Science Concepts
        if general_concept:
            concept_name = general_concept.get("concept", "")
            c_low = concept_name.lower()
            if "rotation" in c_low:
                return (
                    "🌾 **पिकांची फेरपालट (Crop Rotation) माहिती:**\n\n"
                    "**व्याख्या:** एकाच जमिनीत सलग एकच पीक न घेता हंगामानुसार विविध प्रकारची पिके आलटून-पालटून घेण्याच्या पद्धतीला 'पिकांची फेरपालट' म्हणतात.\n\n"
                    "**मुख्य फायदे:** रोग व कीड चक्र खंडित करणे, जमिनीची सुपीकता वाढवणे आणि अन्नद्रव्यांचा संतुलित वापर.\n\n"
                    "**शिफारस केलेला क्रम:** सोलानेसी (टोमॅटो/बटाटा) ➔ कडधान्य (सोयाबीन/हरभरा) ➔ तृणधान्य (गहू/मका) ➔ हिरवळीचे खत."
                    if is_mr
                    else "🌾 **Crop Rotation Guide:**\n\n"
                    "**Definition:** Crop rotation is the systematic practice of growing different types of crops sequentially on the same land across seasons.\n\n"
                    "**Key Principles:** Breaks pest and disease cycles, replenishes soil fertility via legumes, and optimizes nutrient stratification.\n\n"
                    "**Recommended Sequence:** Solanaceous (Tomato/Potato) ➔ Legumes (Soybean/Gram) ➔ Cereals (Wheat/Maize) ➔ Green Manure."
                )
            if "photosynthesis" in c_low:
                return (
                    "☀️ **प्रकाशसंश्लेषण (Photosynthesis) प्रक्रिया:**\n\n"
                    "**व्याख्या:** हिरव्या वनस्पती सूर्यप्रकाशाच्या उपस्थितीत हरितद्रव्याच्या साहाय्याने हवेतील CO2 आणि जमिनीतील पाणी वापरून ग्लुकोज (अन्न) तयार करतात आणि ऑक्सिजन बाहेर सोडतात.\n\n"
                    "**समीकरण:** 6 CO2 + 6 H2O + सूर्यप्रकाश ➔ C6H12O6 + 6 O2\n\n"
                    "**शेतीतील महत्त्व:** पानांवरील करपा किंवा डागांमुळे हरितद्रव्य नष्ट झाल्यास प्रकाशसंश्लेषण घटते व उत्पादनात मोठी घट होते."
                    if is_mr
                    else "☀️ **Photosynthesis & Crop Physiology:**\n\n"
                    "**Definition:** Photosynthesis is the biological process by which green plants utilize chlorophyll to capture solar energy, converting carbon dioxide (CO2) and water (H2O) into glucose (energy) and releasing oxygen (O2).\n\n"
                    "**Chemical Equation:** 6 CO2 + 6 H2O + Light Energy ➔ C6H12O6 + 6 O2\n\n"
                    "**Agronomic Importance:** Foliar diseases destroy active leaf area, directly reducing photosynthetic efficiency and crop yield."
                )
            if "integrated" in c_low or "ipm" in c_low:
                return (
                    "🛡️ **एकात्मिक कीड व्यवस्थापन (IPM):**\n\n"
                    "१. **मशागतीय उपाय:** उन्हाळी खोल नांगरट, पिकांची फेरपालट व सापळा पिके.\n"
                    "२. **भौतिक/यांत्रिक उपाय:** पिवळे चिकट सापळे (मावा/पांढरी माशी) व कामगंध सापळे.\n"
                    "३. **जैविक उपाय:** कडुनिंब तेल (Neem Oil), ट्रायकोडर्मा व मित्रकीटकांचे संवर्धन.\n"
                    "४. **रासायनिक उपाय:** किडींनी आर्थिक नुकसान पातळी (ETL) ओलांडल्यासच शिफारशीत कीटकनाशकांचा वापर."
                    if is_mr
                    else "🛡️ **Integrated Pest Management (IPM) Pillars:**\n\n"
                    "1. **Cultural Control:** Deep summer plowing, crop rotation, and trap crops.\n"
                    "2. **Mechanical & Physical:** Yellow sticky traps (aphids/whiteflies) and pheromone traps.\n"
                    "3. **Biological Control:** Beneficial predators, cold-pressed Neem Oil, and bio-agents.\n"
                    "4. **Chemical Control:** Targeted selective pesticides applied only when pests exceed Economic Threshold Levels (ETL)."
                )
            if "natural farming" in c_low or "zbnf" in c_low or "jeevamrut" in c_low:
                return (
                    "🌿 **नैसर्गिक शेती व जीवामृत तयार करण्याची कृती:**\n\n"
                    "**१. जीवामृत साहित्य (२०० लिटर पाण्यासाठी / १ एकर):**\n"
                    "- देशी गायीचे ताजे शेण: १० किलो\n"
                    "- देशी गायीचे गोमूत्र: ५ ते १० लिटर\n"
                    "- गूळ (काळा/सेंद्रिय): २ किलो\n"
                    "- कडधान्याचे पीठ (बेसन): २ किलो\n"
                    "- झाडाखालील/बांधावरील सुपीक सजीव माती: १ मूठ (१०० ग्रॅम)\n\n"
                    "**२. कृती व वापर:** सर्व घटक २०० लिटर पाण्यात सावलीत ढवळावेत; घड्याळाच्या दिशेने दिवसातून २ वेळा २-३ मिनिटे ढवळा. ४८ ते ७२ तासांत जीवामृत तयार होते. ठिबक सिंचनातून किंवा पाटपाण्याने द्यावे.\n\n"
                    "**३. इतर अस्त्रे:** बीजामृत (बीजप्रक्रिया), निमास्त्र/दशपर्णी अर्क (रसशोषक कीड नियंत्रण), ब्रह्मास्त्र/अग्निअस्त्र (अळी नियंत्रण)."
                    if is_mr
                    else "🌿 **Natural Farming (ZBNF) & Jeevamrut Preparation Protocol:**\n\n"
                    "**1. Jeevamrut Recipe (Per Acre / 200 Litres Water):**\n"
                    "- Fresh Desi Cow Dung: 10 kg\n"
                    "- Fresh Desi Cow Urine: 5 to 10 Litres\n"
                    "- Organic Jaggery: 2 kg\n"
                    "- Pulse Flour (Besan/Gram flour): 2 kg\n"
                    "- Forest / Virgin Bund Soil: 1 handful (100g)\n\n"
                    "**2. Preparation & Application:** Mix all ingredients in 200L water in shade. Stir clockwise for 2-3 minutes twice daily. Ferment for 48 to 72 hours. Apply 200L/acre through drip or flood irrigation, or filter and foliar spray at 5-10% concentration.\n\n"
                    "**3. Bio-Formulations:** Beejamrut (seed coating), Neemastra / Dashparni Ark (sucking pest control), Brahmastra / Agniastra (caterpillar/borer control)."
                )
            if "drone" in c_low:
                return (
                    "🚁 **ड्रोन फवारणी मार्गदर्शक सूचना (Kisan Drone SOP):**\n\n"
                    "- **अल्ट्रा-लो व्हॉल्यूम (ULV):** प्रति एकर केवळ ८ ते १० लिटर पाण्यात आवश्यक औषध मिसळून अचूक फवारणी होते.\n"
                    "- **फवारणी उंची:** पिकाच्या शेंड्यापासून १.५ ते २.० मीटर उंची आणि ३ ते ५ मीटर/सेकंद उड्डाण वेग.\n"
                    "- **नोजल व थेंब आकार:** हायड्रॉलिक किंवा सेंट्रीफ्युगल रोटरी अटॉमायझर (Droplet size 100-150 microns).\n"
                    "- **हवामान दक्षता:** वाऱ्याचा वेग १० किमी/तास पेक्षा जास्त असताना किंवा भर उन्हात फवारणी करू नये. सकाळी किंवा संध्याकाळी फवारणी सर्वोत्तम."
                    if is_mr
                    else "🚁 **Kisan Drone Spraying SOP & Technical Guidelines:**\n\n"
                    "- **Ultra-Low Volume (ULV):** Applies agrochemicals uniformly using only 8 to 10 Litres of water per acre.\n"
                    "- **Flight Parameters:** Maintain 1.5 to 2.0 meters above crop canopy at 3 to 5 m/s flight speed.\n"
                    "- **Nozzle & Droplet Dynamics:** Rotary atomizer or flat fan nozzles generating 100-150 micron droplets for electrostatic adherence.\n"
                    "- **Safety Constraints:** Never spray when wind speed exceeds 10 km/h or ambient temperature exceeds 35°C. Morning or late afternoon flights prevent drift and evaporation loss."
                )
            if "salinity" in c_low or "sodic" in c_low:
                return (
                    "🧂 **खारवट व चोपण जमीन सुधारणा पद्धती:**\n\n"
                    "- **जिप्समचा वापर:** चोपण (Sodic/Alkali) जमिनीतील विनिमययोग्य सोडियम हटवण्यासाठी माती परीक्षणानुसार प्रति हेक्टरी २ ते ५ टन कृषी जिप्सम (Gypsum - CaSO4.2H2O) जमिनीत मिसळावे.\n"
                    "- **पाण्याचा निचरा (Leaching):** क्षारयुक्त (Saline) जमिनीत शेतात पाण्याचा निचरा करण्यासाठी चर काढावेत व गोड पाण्याने क्षार धुऊन काढावेत.\n"
                    "- **सेंद्रिय सुधारक:** ढेंचा (Dhaincha) किंवा ताग यांसारखी हिरवळीची खते गाडावीत आणि भरपूर शेणखत वापरावे.\n"
                    "- **क्षार सहनशील पिके:** गहू (KRL-210), बाजरी, मोहरी, कापूस व डाळिंब."
                    if is_mr
                    else "🧂 **Soil Salinity & Sodic Land Reclamation Protocol:**\n\n"
                    "- **Gypsum Amendment:** For alkali/sodic soils (ESP > 15%), incorporate Agricultural Gypsum (CaSO4.2H2O @ 2.5 to 5.0 t/ha) to displace harmful exchangeable sodium (Na+) with calcium (Ca2+).\n"
                    "- **Subsurface Leaching:** For saline soils (EC > 4.0 dS/m), construct drainage trenches to flush dissolved salts below the active crop root zone.\n"
                    "- **Organic Matter & Green Manuring:** Incorporate Dhaincha (*Sesbania aculeata*) or Sunnhemp and apply 15-20 t/ha FYM to enhance soil porosity.\n"
                    "- **Salt-Tolerant Cultivars:** Grow salinity-tolerant crops such as Wheat (KRL-210), Barley, Cotton, Mustard, or Pomegranate."
                )
            if "weed" in c_low or "तण" in c_low:
                return (
                    "🌿 **एकात्मिक तण व्यवस्थापन (Integrated Weed Management):**\n\n"
                    "- **उगवणीपूर्व (Pre-Emergence):** पिकाची पेरणी झाल्यावर व पीक उगवण्यापूर्वी २-३ दिवसांत पेंडीमेथॅलीन ३०% EC (Pendimethalin @ ३.३ लिटर/हे.) ओलित जमिनीवर फवारावे.\n"
                    "- **उगवणीनंतर (Post-Emergence):**\n"
                    "  • सोयाबीन/कापूस: क्विझालोफॉप-इथाईल ५% EC (Quizalofop @ १ लिटर/हे.) गवतवर्गीय तणांसाठी.\n"
                    "  • मका/ऊस: ॲट्राझिन ५०% WP (Atrazine @ २ किलो/हे.) किंवा २,४-डी अमाईन सॉल्ट.\n"
                    "- **मशागतीय उपाय:** मल्चिंग (Mulching), आंतरमशागत (कोळपणी/खुरपणी) आणि आंतरपिके."
                    if is_mr
                    else "🌿 **Integrated Weed Management Protocol (IWM):**\n\n"
                    "- **Pre-Emergence Herbicides:** Spray Pendimethalin 30% EC (@ 3.3 L/ha) within 0-3 days of sowing on moist soil to prevent annual grass and broadleaf weed emergence.\n"
                    "- **Selective Post-Emergence:**\n"
                    "  • In Soybean/Cotton: Quizalofop-p-ethyl 5% EC (@ 1.0 L/ha) for grassy weed control.\n"
                    "  • In Maize/Sugarcane: Atrazine 50% WP (@ 2.0 kg/ha) or 2,4-D Amine salt for broadleaf weeds.\n"
                    "- **Cultural & Mechanical:** Silver-black plastic mulching, inter-row mechanical hoeing, and high seed-rate canopy closure."
                )
            # Generic structured fallback for any other general concept in general_agri_data
            concept_def = general_concept.get("definition", "")
            principles = general_concept.get("key_principles", []) or general_concept.get("management_guidelines", []) or general_concept.get("four_pillars", [])
            p_text = "\n".join(f"- {p}" for p in principles[:4])
            crop_suffix = f" for {plant_name}" if plant_name and plant_name not in ["General", "Crop", "All Crops"] else ""
            crop_suffix_mr = f" ({plant_name})" if plant_name and plant_name not in ["General", "Crop", "All Crops"] else ""
            return (
                f"🌱 **{concept_name}{crop_suffix_mr} (कृषी विज्ञान माहिती):**\n\n"
                f"**माहिती:** {concept_def}\n\n"
                f"**महत्त्वाचे मुद्दे:**\n{p_text}"
                if is_mr
                else f"🌱 **{concept_name}{crop_suffix} Agricultural Science Guide:**\n\n"
                f"**Overview:** {concept_def}\n\n"
                f"**Key Principles & Management:**\n{p_text}"
            )

        # 4. Weather & Outbreak Risk Assessment
        if intent in [AgriculturalIntent.WEATHER, AgriculturalIntent.WEATHER_DISEASE_RISK]:
            if weather_info and (weather_info.get("temperature_c") or weather_info.get("temp_c")):
                temp = weather_info.get("temperature_c") or weather_info.get("temp_c")
                hum = weather_info.get("humidity_pct", 70)
                rain = weather_info.get("rainfall_mm", 0.0)
                is_high_risk = hum >= 80 or rain > 5.0
                if is_mr:
                    return (
                        f"🌦️ **हवामान आणि रोग प्रादुर्भाव जोखीम विश्लेषण ({plant_name}):**\n\n"
                        f"- **सध्याचे हवामान:** तापमान {temp}°C | आर्द्रता {hum}% | पाऊस {rain} mm\n"
                        f"- **जोखीम पातळी:** {'⚠️ उच्च जोखीम (High Risk)' if is_high_risk else '✅ मध्यम/कमी जोखीम (Moderate Risk)'}\n"
                        f"- **विश्लेषण:** ८०% पेक्षा जास्त आर्द्रता आणि ढगाळ वातावरणामुळे बुरशीच्या बीजाणूंची (spores) उगवण वेगाने होते.\n"
                        f"- **शेतकऱ्यांसाठी कृती:**\n"
                        f"  1. शेतात पाण्याचा निचरा योग्य ठेवा आणि संध्याकाळी तुषार सिंचन टाळा.\n"
                        f"  2. प्रतिबंधक उपाय म्हणून कडुनिंब तेल (५ मि.ली./लिटर) किंवा ट्रायकोडर्माची फवारणी करा.\n"
                        f"  3. रोगाची सुरुवातीची लक्षणे दिसताच कृषी विद्यापीठ शिफारशीनुसार उपाययोजना करा."
                    )
                else:
                    return (
                        f"🌦️ **Weather & Disease Outbreak Risk Assessment ({plant_name}):**\n\n"
                        f"- **Current Conditions:** Temp: {temp}°C | Humidity: {hum}% | Rain: {rain} mm\n"
                        f"- **Risk Level:** {'⚠️ High Risk for Fungal Outbreaks' if is_high_risk else '✅ Moderate/Low Risk'}\n"
                        f"- **Epidemiology:** Sustained relative humidity (>80%) and prolonged leaf wetness create optimal conditions for fungal spore germination and foliar blights.\n"
                        f"- **Immediate Farmer Action:**\n"
                        f"  1. Ensure proper drainage and avoid overhead sprinkler watering in the evening.\n"
                        f"  2. Apply a preventive bio-protectant (Neem Oil 3000 ppm @ 4 ml/L or *Trichoderma*).\n"
                        f"  3. Regularly inspect the lower canopy for early water-soaked spots."
                    )
            else:
                return (
                    "🌦️ **हवामान जोखीम माहिती:** सध्याचे हवामान तपशील थेट उपलब्ध नाहीत, परंतु ढगाळ व दमट हवामानात बुरशीजन्य रोगांचा प्रादुर्भाव वेगाने वाढतो. प्रतिबंधात्मक फवारणी व योग्य पाण्याचा निचरा ठेवण्याचा सल्ला दिला जातो."
                    if is_mr
                    else "🌦️ **Weather Risk Guidance:** Real-time weather data is currently unavailable. Generally, persistent overcast skies and high humidity (>80%) accelerate fungal spore development. Maintain canopy aeration and ensure good field drainage."
                )

        # 5. Irrigation & Water Management
        if intent == AgriculturalIntent.IRRIGATION:
            if plant_info:
                cname = plant_info["common_name"]
                return (
                    f"💧 **{cname} पिकाचे पाणी व्यवस्थापन:**\n\n"
                    f"- **सिंचन वेळापत्रक:** {plant_info['irrigation']}\n"
                    f"- **पाण्याची गरज व पाऊस:** {plant_info['rainfall']}\n"
                    f"- **महत्त्वाच्या अवस्था:** फुलधारणा व फळ/दाणे भरण्याच्या काळात पाण्याचा ताण पडू देऊ नये.\n"
                    f"- **पद्धत:** ठिबक सिंचनाचा (Drip Irrigation) वापर केल्यास ४०-५०% पाण्याची बचत होते आणि पानांवर पाणी न पडल्यामुळे बुरशीचा प्रादुर्भाव टळतो."
                    if is_mr
                    else f"💧 **Irrigation Management Protocol for {cname}:**\n\n"
                    f"- **Irrigation Schedule:** {plant_info['irrigation']}\n"
                    f"- **Water Requirement & Rainfall:** {plant_info['rainfall']}\n"
                    f"- **Critical Growth Stages:** Avoid moisture stress during flowering, fruit set, and grain filling.\n"
                    f"- **Recommended Method:** Drip irrigation provides 40-50% water savings, maintains optimal root-zone Vafsa (50% air / 50% water), and avoids foliar wetting that triggers fungal blights."
                )

        # 6. Soil & Land Preparation
        if intent == AgriculturalIntent.SOIL:
            if plant_info:
                cname = plant_info["common_name"]
                return (
                    f"🌱 **{cname} पिकासाठी योग्य जमीन व मातीची आवश्यकता:**\n\n"
                    f"- **मातीचा प्रकार:** {plant_info['soil']}\n"
                    f"- **मातीचा सामू (pH):** {plant_info['pH']}\n"
                    f"- **हवामान अनुकूलता:** {plant_info['climate']}\n"
                    f"- **मशागत सूचना:** शेतात पाणी साचून राहणार नाही याची काळजी घ्या; सेंद्रिय खतांचा (शेणखत/कंपोस्ट) भरपूर वापर करा."
                    if is_mr
                    else f"🌱 **Optimal Soil & Land Requirements for {cname}:**\n\n"
                    f"- **Soil Type:** {plant_info['soil']}\n"
                    f"- **Optimal Soil pH:** {plant_info['pH']}\n"
                    f"- **Climate Suitability:** {plant_info['climate']}\n"
                    f"- **Cultivation Note:** Ensure adequate permeability and root-zone depth; incorporate 15-20 t/ha well-rotted FYM/compost to enhance soil structure and buffering capacity."
                )

        # 7. Fertilizer & Nutrition
        if intent in [AgriculturalIntent.FERTILIZER, AgriculturalIntent.NUTRITION]:
            if plant_info:
                cname = plant_info["common_name"]
                return (
                    f"🧪 **{cname} खत व्यवस्थापन (Fertilizer Protocol):**\n\n"
                    f"- **खतांचे प्रमाण व वेळापत्रक:** {plant_info['fertilizer']}\n"
                    f"- **सेंद्रिय खत:** लागवडीच्या वेळी प्रति हेक्टरी १५-२० टन शेणखत किंवा गांडूळ खत जमिनीत मिसळावे.\n"
                    f"- **सूक्ष्म अन्नद्रव्ये:** झिंक व बोरॉनची कमतरता असल्यास माती परीक्षणानुसार ग्रेड-२ सूक्ष्म अन्नद्रव्यांची फवारणी करावी."
                    if is_mr
                    else f"🧪 **Fertilizer & Nutrition Schedule for {cname}:**\n\n"
                    f"- **Recommended Protocol:** {plant_info['fertilizer']}\n"
                    f"- **Organic Base:** Incorporate 15-20 tonnes/ha well-rotted Farm Yard Manure (FYM) or vermicompost as basal application.\n"
                    f"- **Micronutrient Balance:** Correct Zinc, Boron, or Iron deficiencies with foliar chelates based on soil testing."
                )

        # 8. Harvesting & Post-Harvest
        if intent == AgriculturalIntent.HARVESTING:
            if plant_info:
                cname = plant_info["common_name"]
                return (
                    f"🌾 **{cname} काढणीची वेळ व पद्धत:**\n\n"
                    f"- **पक्वतेची लक्षणे:** {plant_info['harvesting']}\n"
                    f"- **काढणीनंतरची हाताळणी:** {plant_info['post_harvest']}"
                    if is_mr
                    else f"🌾 **Harvesting & Post-Harvest Guidelines for {cname}:**\n\n"
                    f"- **Maturity Indicators:** {plant_info['harvesting']}\n"
                    f"- **Post-Harvest & Storage:** {plant_info['post_harvest']}"
                )

        # 9. Planting & Sowing
        if intent == AgriculturalIntent.PLANTING:
            if plant_info:
                cname = plant_info["common_name"]
                return (
                    f"🌱 **{cname} लागवड व पेरणी पद्धत:**\n\n"
                    f"- **लागवड पद्धत:** {plant_info.get('planting', 'योग्य अंतर राखून पुनर्लागवड किंवा पेरणी करावी.')}\n"
                    f"- **शिफारस केलेले अंतर:** {plant_info.get('spacing', 'पिकाच्या वाणानुसार योग्य अंतर ठेवावे.')}\n"
                    f"- **हवामान:** {plant_info.get('climate', 'उबदार व समशीतोष्ण हवामान')}"
                    if is_mr
                    else f"🌱 **Planting & Sowing Guidelines for {cname}:**\n\n"
                    f"- **Planting Method:** {plant_info.get('planting', 'Transplant seedlings or direct sow in well-prepared beds.')}\n"
                    f"- **Recommended Spacing:** {plant_info.get('spacing', 'Standard recommended row and plant spacing.')}\n"
                    f"- **Climate Suitability:** {plant_info.get('climate', 'Warm and temperate conditions')}"
                )

        # 10. Disease Identification / Symptoms when specific disease is not known yet
        if intent in [AgriculturalIntent.DISEASE_IDENTIFICATION, AgriculturalIntent.DISEASE_SYMPTOMS] and plant_info and not disease_info:
            cname = plant_info["common_name"]
            d_list = plant_info.get("diseases", [])
            if is_mr:
                return (
                    f"🦠 **{cname} पिकावरील प्रमुख रोग व लक्षणे:**\n\n" +
                    "\n".join(f"{i+1}. **{d}**" for i, d in enumerate(d_list)) +
                    "\n\n*विशिष्ट रोगाच्या सविस्तर उपचारासाठी रोगाचे नाव नमूद करा किंवा झाडाचा फोटो स्कॅन करा.*"
                )
            return (
                f"🦠 **Major Diseases Affecting {cname}:**\n\n" +
                "\n".join(f"{i+1}. **{d}**" for i, d in enumerate(d_list)) +
                "\n\n*To get targeted treatments or chemical recommendations, specify the observed symptoms or upload a leaf image.*"
            )

        # 11. Disease Symptoms & Visual Markers
        if disease_info:
            dname = disease_info["disease_name"]
            if intent in [AgriculturalIntent.DISEASE_SYMPTOMS, AgriculturalIntent.DISEASE_IDENTIFICATION, AgriculturalIntent.SCAN_EXPLANATION]:
                return (
                    f"🔍 **{dname} रोगाची लक्षणे व ओळख:**\n\n"
                    f"- **मुख्य लक्षणे:** {disease_info['symptoms']}\n\n"
                    f"- **दृश्य चिन्हे:**\n" + "\n".join(f"  • {s}" for s in disease_info.get('visual_symptoms', []))
                    if is_mr
                    else f"🔍 **Symptoms and Diagnostic Markers of {dname}:**\n\n"
                    f"- **Primary Symptoms:** {disease_info['symptoms']}\n\n"
                    f"- **Visual Markers:**\n" + "\n".join(f"  • {s}" for s in disease_info.get('visual_symptoms', []))
                )

            # 12. Disease Causes / Etiology / Yellowing
            if intent == AgriculturalIntent.DISEASE_CAUSE:
                return (
                    f"🧬 **{dname} रोगाची कारणे व उत्पत्ती:**\n\n"
                    f"- **रोगकारक:** {disease_info.get('causes', 'बुरशीजन्य किंवा जिवाणूजन्य संसर्ग')}\n"
                    f"- **अनुकूल हवामान:** {disease_info.get('favorable_conditions', 'जास्त आर्द्रता व मध्यम तापमान')}\n"
                    f"- **प्रसाराचे माध्यम:** {disease_info.get('spread_conditions', 'हवा, पाणी आणि शेती अवजारे')}"
                    if is_mr
                    else f"🧬 **Etiology & Causes of {dname}:**\n\n"
                    f"- **Pathogen & Causes:** {disease_info.get('causes', 'Fungal / Bacterial infection')}\n"
                    f"- **Favorable Conditions:** {disease_info.get('favorable_conditions', 'High relative humidity and warm temperatures')}\n"
                    f"- **Transmission Vector:** {disease_info.get('spread_conditions', 'Wind-borne spores, rain splash, and contaminated tools')}"
                )

            # 13. Disease Transmission / Spread
            if intent == AgriculturalIntent.DISEASE_TRANSMISSION:
                return (
                    f"💨 **{dname} रोगाचा प्रसार व संसर्ग माहिती:**\n\n"
                    f"- **प्रसाराचे माध्यम:** {disease_info.get('spread_conditions', 'बुरशीचे बीजाणू हवेतून आणि पाण्याच्या थेंबांमधून पसरतात.')}\n"
                    f"- **इतर झाडांना धोका:** होय, शेजारील झाडांवर हवेच्या प्रवाहामुळे किंवा तुषार सिंचनामुळे हा रोग पसरू शकतो.\n"
                    f"- **प्रसार रोखण्यासाठी:** बाधित पाने काढून जाळून टाका, झाडांची योग्य छाटणी करा आणि प्रतिबंधक फवारणी करा."
                    if is_mr
                    else f"💨 **Disease Transmission & Spread Dynamics for {dname}:**\n\n"
                    f"- **Transmission Vector:** {disease_info.get('spread_conditions', 'Fungal spores spread via wind currents, rain splash, and infected crop debris.')}\n"
                    f"- **Can it Spread to Nearby Plants?:** Yes, neighboring plants in the same field are at high risk under humid conditions.\n"
                    f"- **How to Stop Spread:** Roguing and destroying infected lower leaves, avoiding overhead irrigation, and applying protective bio-sprays (Neem Oil / Mancozeb)."
                )

            # 14. Disease Prevention
            if intent == AgriculturalIntent.DISEASE_PREVENTION:
                return (
                    f"🛡️ **{dname} प्रतिबंधक उपाय:**\n\n"
                    f"- **मशागतीय उपाय:** {disease_info.get('prevention', 'पिकांची फेरपालट व स्वच्छता.')}\n"
                    f"- **जैविक प्रतिबंध:** {disease_info.get('biological_control', 'कडुनिंब तेल व ट्रायकोडर्मा.')}"
                    if is_mr
                    else f"🛡️ **Preventive Protocol for {dname}:**\n\n"
                    f"- **Cultural Prevention:** {disease_info.get('prevention', 'Crop rotation, field sanitation, and certified seeds.')}\n"
                    f"- **Prophylactic Bio-Sprays:** {disease_info.get('biological_control', 'Neem Oil and Trichoderma bio-formulations.')}"
                )

            # 15. Disease Treatment & Cure
            if intent == AgriculturalIntent.DISEASE_TREATMENT:
                return (
                    f"💊 **{dname} नियंत्रण व उपचार पद्धती:**\n\n"
                    f"1. **जैविक उपाय:** {disease_info['biological_control']}\n\n"
                    f"2. **रासायनिक उपाय:** {disease_info['chemical_management']}\n\n"
                    f"3. **सुरक्षा व लेबल सूचना:** {disease_info['safety_notes']}"
                    if is_mr
                    else f"💊 **Management & Treatment Protocol for {dname}:**\n\n"
                    f"1. **Biological / Organic Controls:** {disease_info['biological_control']}\n\n"
                    f"2. **Approved Chemical Options:** {disease_info['chemical_management']}\n\n"
                    f"3. **Safety & Label Instructions:** {disease_info['safety_notes']}"
                )

        # 16. General Pests
        if intent in [AgriculturalIntent.PEST, AgriculturalIntent.PEST_MANAGEMENT]:
            if plant_info:
                cname = plant_info["common_name"]
                return (
                    f"🐛 **{cname} पिकावरील कीड व्यवस्थापन (IPM):**\n\n"
                    f"- **प्रमुख किडी:** " + ", ".join(plant_info.get("pests", ["मावा", "तुडतुडे", "पांढरी माशी", "अळी"])) + "\n"
                    f"- **जैविक व यांत्रिक उपाय:** पिवळे चिकट सापळे लावावेत आणि ५ मि.ली./लिटर कडुनिंब तेलाची (Neem Oil) फवारणी करावी.\n"
                    f"- **प्रतिबंध:** {plant_info.get('prevention', 'तण नियंत्रण व नियमित पाहणी.')}"
                    if is_mr
                    else f"🐛 **Integrated Pest Management for {cname}:**\n\n"
                    f"- **Major Pests:** " + ", ".join(plant_info.get("pests", ["Aphids", "Whiteflies", "Thrips", "Caterpillars"])) + "\n"
                    f"- **Mechanical & Bio-Control:** Install yellow sticky traps (15-20/acre) and spray cold-pressed Neem Oil (3000 ppm @ 4 ml/L).\n"
                    f"- **Cultural Prevention:** {plant_info.get('prevention', 'Clean cultivation and regular scouting.')}"
                )

        # 17. Default Question-Targeted Agronomy Response
        if is_mr:
            return f"🌾 **AgroScan AI कृषी सल्लागार ({plant_name}):**\n\nतुमच्या प्रश्नानुसार ('{question}'), योग्य मशागत, पाण्याचा निचरा आणि संतुलित खत व्यवस्थापन आवश्यक आहे. अधिक सविस्तर मार्गदर्शनासाठी पिकाचे किंवा रोगाचे नाव नमूद करा."
        return f"🌾 **AgroScan AI Agronomist ({plant_name}):**\n\nRegarding your query ('{question}'): For optimal {plant_name} health and productivity, ensure balanced nutrition, proper irrigation intervals, and active monitoring."
