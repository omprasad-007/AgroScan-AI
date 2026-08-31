"""
AgroScan AI — Assistant Master Orchestrator Service
Coordinates Intent Detection, Context Extraction, Source Routing, Multi-Source Research,
Local RAG Retrieval, Multi-Model LLM Reasoning, Contradiction Detection, Safety Fact-Checking,
and Citation Packaging into a unified evidence-grounded response.
"""

from typing import Dict, Any, Optional, List
from app.services.intent_service import IntentService, AgriculturalIntent
from app.services.assistant.context_service import ContextService
from app.services.assistant.conversation_service import ConversationService
from app.services.assistant.response_service import ResponseService
from app.services.research.research_service import ResearchService
from app.services.rag.retrieval_service import RetrievalService
from app.services.llm.llm_router import LLMRouter
from app.services.llm.synthesis_service import SynthesisService
from app.services.verification.fact_checker import FactChecker
from app.services.verification.contradiction_detector import ContradictionDetector
from app.services.verification.confidence_service import ConfidenceService
from app.services.agri_rag_service import AgriRAGService

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
        research_mode: str = "auto"
    ) -> Dict[str, Any]:
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

        # 1. Context & Entity Resolution
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

        # 2. Multi-Source Evidence Research (FAO, ICAR, CABI, Springer, Agri Univs)
        research_data = ResearchService.conduct_research(
            query=clean_input,
            plant_name=plant_name,
            disease_name=disease_name,
            intent=intent,
            research_mode=research_mode
        )

        # 3. Local RAG Retrieval
        rag_data = RetrievalService.retrieve_grounding(
            question=clean_input,
            scan_context=scan_context,
            manual_plant=manual_plant,
            conversation_history=history
        )

        # 4. Check for Contradictions in Evidence
        contra_info = ContradictionDetector.analyze_contradictions(research_data["ranked_evidence"])

        # 5. Build Strict Grounding System Prompt
        system_prompt = SynthesisService.build_system_prompt(
            question=clean_input,
            rag_data=rag_data,
            research_data=research_data,
            location_info=location_info,
            weather_info=weather_info,
            language=language
        )

        # 6. Execute Multi-Model Reasoning
        reply_text, success, model_used = LLMRouter.execute_reasoning(
            system_prompt=system_prompt,
            history=history,
            user_message=clean_input,
            complexity=research_mode
        )

        # Fallback to local domain synthesis if external APIs are unreachable
        if not success or not reply_text:
            reply_text = SynthesisService.synthesize_domain_fallback(
                question=clean_input,
                rag_data=rag_data,
                weather_info=weather_info,
                language=language
            )

        # 7. Run Safety Fact-Checker
        fact_res = FactChecker.verify_and_sanitize_response(
            generated_answer=reply_text,
            evidence_items=research_data["ranked_evidence"],
            plant_name=plant_name or "",
            disease_name=disease_name or ""
        )
        final_answer = fact_res["sanitized_answer"]

        # 8. Compute Confidence Score
        confidence = ConfidenceService.calculate_confidence(
            evidence_items=research_data["ranked_evidence"],
            has_contradictions=contra_info["has_contradiction"]
        )

        # 9. Format Standardized Response Payload
        weather_is_relevant = AgriRAGService.is_weather_relevant(clean_input) and bool(weather_info)
        return ResponseService.build_research_payload(
            answer=final_answer,
            intent=intent,
            sources=research_data["sources"],
            confidence=confidence,
            source_agreement=research_data["source_agreement"],
            context_meta=context_meta,
            weather_used=weather_is_relevant
        )
