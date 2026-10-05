"""
AgroScan AI — Assistant Master Orchestrator Service
Coordinates Question Analysis, Intent Detection, Context Extraction, Source Routing, Multi-Source Research,
Local RAG Retrieval, Multi-Model LLM Reasoning, Contradiction Detection, Safety Fact-Checking,
Response Caching, and Citation Packaging into a unified evidence-grounded response.
"""

import time
import logging
from typing import Dict, Any, Optional, List
from app.services.intent_service import IntentService, AgriculturalIntent
from app.services.assistant.question_analyzer import QuestionAnalyzer, QuestionAnalysis
from app.services.assistant.context_service import ContextService
from app.services.assistant.conversation_service import ConversationService
from app.services.assistant.response_service import ResponseService
from app.services.assistant.response_cache import ResponseCache
from app.services.research.research_service import ResearchService
from app.services.rag.retrieval_service import RetrievalService
from app.services.llm.llm_router import LLMRouter
from app.services.llm.synthesis_service import SynthesisService
from app.services.verification.fact_checker import FactChecker
from app.services.verification.contradiction_detector import ContradictionDetector
from app.services.verification.confidence_service import ConfidenceService
from app.services.agri_rag_service import AgriRAGService

logger = logging.getLogger("agroscan.assistant")

class AssistantService:
    """Master agricultural research assistant service coordinator."""

    @classmethod
    def process_message(
        cls,
        message: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        scan_context: Optional[Dict[str, Any]] = None,
        manual_plant: Optional[str] = None,
        location_info: Optional[Dict[str, Any]] = None,
        weather_info: Optional[Dict[str, Any]] = None,
        language: str = "en",
        research_mode: str = "auto",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        start_time = time.time()
        clean_input = (message or "").strip()[:600]
        history = ConversationService.sanitize_history(conversation_history or [])
        is_mr = language == "mr"

        if not clean_input:
            msg = "कृपया पीक आरोग्य किंवा शेतीविषयी प्रश्न विचारा." if is_mr else "Please ask an agricultural question regarding crop health, soil, pests, or cultivation."
            return ResponseService.build_research_payload(
                answer=msg,
                intent=AgriculturalIntent.GENERAL,
                sources=[],
                confidence=0.50,
                source_agreement="neutral",
                context_meta={},
                weather_used=False
            )

        # 1. Structured Question Analysis & Entity Resolution
        context_meta = ContextService.resolve(
            query=clean_input,
            scan_context=scan_context,
            manual_plant=manual_plant,
            conversation_history=history,
            location_info=location_info
        )
        intent = context_meta["intent"]
        plant_name = context_meta["plant_name"]
        disease_name = context_meta["disease_name"]
        analysis: Optional[QuestionAnalysis] = context_meta.get("analysis")

        # 2. Check Response Cache (if not live weather risk)
        is_weather_intent = intent in [AgriculturalIntent.WEATHER, AgriculturalIntent.WEATHER_DISEASE_RISK]
        cache_key = ResponseCache.generate_cache_key(
            user_id=user_id,
            normalized_question=analysis.normalized_question if analysis else clean_input,
            intent=intent,
            language=language,
            plant_name=plant_name,
            disease_name=disease_name
        )

        if not is_weather_intent:
            cached = ResponseCache.get(cache_key)
            if cached:
                logger.info(f"[CACHE HIT] Intent={intent} | Plant={plant_name} | Q={clean_input[:40]}")
                return cached

        # 3. Multi-Source Evidence Research (FAO, ICAR, CABI, Springer, Agri Univs)
        research_data = ResearchService.conduct_research(
            query=clean_input,
            plant_name=plant_name,
            disease_name=disease_name,
            intent=intent,
            research_mode=research_mode
        )

        # 4. Local Dynamic RAG Retrieval
        rag_data = RetrievalService.retrieve_grounding(
            question=clean_input,
            scan_context=scan_context,
            manual_plant=manual_plant,
            conversation_history=history
        )

        # 5. Check for Contradictions in Evidence
        contra_info = ContradictionDetector.analyze_contradictions(research_data["ranked_evidence"])

        # 6. Build Strict Grounding System Prompt
        system_prompt = SynthesisService.build_system_prompt(
            question=clean_input,
            rag_data=rag_data,
            research_data=research_data,
            location_info=location_info,
            weather_info=weather_info,
            language=language
        )

        # 7. Execute Multi-Model Reasoning
        reply_text, success, model_used = LLMRouter.execute_reasoning(
            system_prompt=system_prompt,
            history=history,
            user_message=clean_input,
            complexity=research_mode
        )

        # Fallback to local domain synthesis if external APIs are unreachable or offline
        if not success or not reply_text:
            reply_text = SynthesisService.synthesize_domain_fallback(
                question=clean_input,
                rag_data=rag_data,
                weather_info=weather_info,
                language=language
            )

        # 8. Run Safety Fact-Checker
        fact_res = FactChecker.verify_and_sanitize_response(
            generated_answer=reply_text,
            evidence_items=research_data["ranked_evidence"],
            plant_name=plant_name or "",
            disease_name=disease_name or ""
        )
        final_answer = fact_res["sanitized_answer"]

        # 9. Compute Confidence Score
        confidence = ConfidenceService.calculate_confidence(
            evidence_items=research_data["ranked_evidence"],
            has_contradictions=contra_info["has_contradiction"]
        )

        # 10. Format Standardized Response Payload
        weather_is_relevant = AgriRAGService.is_weather_relevant(clean_input) and bool(weather_info)
        payload = ResponseService.build_research_payload(
            answer=final_answer,
            intent=intent,
            sources=research_data["sources"],
            confidence=confidence,
            source_agreement=research_data["source_agreement"],
            context_meta=context_meta,
            weather_used=weather_is_relevant
        )

        # 11. Cache response
        ttl = 300 if is_weather_intent else 3600
        ResponseCache.set(cache_key, payload, ttl_seconds=ttl)

        # 12. Structured Debug Logging
        elapsed_sec = round(time.time() - start_time, 3)
        logger.info(
            f"[ASSISTANT] Intent={intent} | Plant={plant_name} | Disease={disease_name} | "
            f"Sources={len(research_data['sources'])} | Model={model_used} | Latency={elapsed_sec}s"
        )

        return payload
