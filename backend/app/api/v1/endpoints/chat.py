from typing import List, Any, cast
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.all_models import User, ChatSession, ChatMessage, ScanPrediction, Farm
from app.schemas.schemas import ChatMessageCreate, ChatMessageResponse, ChatSessionResponse
from app.api.deps import get_current_user
from app.services.ai_provider_service import AIProviderService
from app.services.agri_rag_service import AgriRAGService

router = APIRouter()

@router.post("", response_model=ChatMessageResponse)
def post_chat_message(
    chat_in: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = None
    if chat_in.session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == chat_in.session_id,
            ChatSession.user_id == current_user.id
        ).first()

    if not session:
        session = ChatSession(user_id=current_user.id, title="AgroScan AI Advisory")
        db.add(session)
        db.commit()
        db.refresh(session)

    # 1. Build accumulated conversation history from DB session and/or incoming request
    db_messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.created_at.asc()).all()

    conv_history = []
    for msg in db_messages:
        conv_history.append({
            "role": "user" if msg.sender == "user" else "assistant",
            "content": msg.content
        })

    # If incoming request passed explicit history (e.g. client session), merge non-duplicate messages
    if chat_in.conversation_history and len(chat_in.conversation_history) > len(conv_history):
        conv_history = [
            {"role": m.get("role", "user"), "content": m.get("content", "")}
            for m in chat_in.conversation_history
            if m.get("content", "").strip() and m.get("content", "").strip() != chat_in.message.strip()
        ]

    # 2. Save Current User Message to DB
    user_msg = ChatMessage(
        session_id=session.id,
        sender="user",
        content=chat_in.message
    )
    db.add(user_msg)
    db.commit()

    # 3. Retrieve scan context if prediction_id provided (enforce strict user ownership)
    scan_ctx = None
    if chat_in.prediction_id:
        pred = db.query(ScanPrediction).filter(
            ScanPrediction.id == chat_in.prediction_id,
            ScanPrediction.user_id == current_user.id
        ).first()
        if pred:
            scan_ctx = {
                "scan_id": pred.id,
                "crop_detected": pred.crop_detected,
                "disease_name": pred.disease_name,
                "severity_level": pred.severity_level,
                "severity_percentage": pred.severity_percentage,
                "confidence_score": pred.confidence_score,
                "weather_risk_level": pred.weather_risk_level,
                "created_at": str(pred.created_at)
            }

    # 4. Resolve confirmed user farm location (Priority: Current Request -> Farm -> Profile -> None)
    location_info = chat_in.location
    if not location_info:
        # Check user profile or latest farm
        farm = db.query(Farm).filter(Farm.user_id == current_user.id).order_by(Farm.created_at.desc()).first()
        if farm and (farm.village or farm.district or farm.latitude):
            location_info = {
                "village": farm.village,
                "taluka": farm.taluka,
                "district": farm.district,
                "state": farm.state,
                "pincode": farm.pincode,
                "latitude": farm.latitude,
                "longitude": farm.longitude
            }
        elif current_user.village or current_user.district:
            location_info = {
                "village": current_user.village,
                "taluka": current_user.taluka,
                "district": current_user.district,
                "state": current_user.state,
                "pincode": current_user.pincode,
                "latitude": current_user.latitude,
                "longitude": current_user.longitude
            }

    # 5. Fetch weather conditionally only when relevant to question
    weather_info = None
    if AgriRAGService.is_weather_relevant(chat_in.message) and location_info:
        from app.services.weather_service import WeatherRiskService
        lat = location_info.get("latitude")
        lon = location_info.get("longitude")
        city_val = location_info.get("district") or location_info.get("village")
        city_str = str(city_val) if city_val else ""
        if city_str or (lat and lon):
            try:
                weather_info = WeatherRiskService.fetch_weather_sync(city=city_str, lat=lat, lon=lon)
            except Exception:
                pass

    # 6. Generate multi-source response via AIProviderService with full conversation history & research
    manual_crop = chat_in.manual_plant
    if not manual_crop and chat_in.context:
        manual_crop = chat_in.context.get("plant") or chat_in.context.get("plant_name")

    res_payload = AIProviderService.generate_structured_research_response(
        message=chat_in.message,
        conversation_history=conv_history,
        scan_context=scan_ctx,
        manual_plant=manual_crop,
        location_info=location_info,
        weather_info=weather_info,
        language=chat_in.language or "en",
        research_mode=chat_in.research_mode or "auto"
    )

    bot_reply_text = str(res_payload.get("answer", ""))

    # 7. Save Assistant Message
    bot_msg = ChatMessage(
        session_id=str(session.id),
        sender="assistant",
        content=bot_reply_text
    )
    db.add(bot_msg)
    db.commit()
    db.refresh(bot_msg)

    return ChatMessageResponse(
        id=str(bot_msg.id),
        session_id=str(bot_msg.session_id) if bot_msg.session_id else None,
        sender=str(bot_msg.sender),
        content=str(bot_msg.content),
        answer=str(bot_msg.content),
        intent=res_payload.get("intent"),
        sources=res_payload.get("sources", []),
        evidence_confidence=res_payload.get("evidence_confidence", 0.92),
        source_agreement=res_payload.get("source_agreement", "high"),
        context_used=res_payload.get("context_used", {}),
        created_at=cast(Any, bot_msg.created_at)
    )

@router.post("/research", response_model=ChatMessageResponse)
def post_assistant_research(
    chat_in: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Direct research endpoint for deep multi-source agricultural inquiries."""
    chat_in.research_mode = "deep_research"
    return post_chat_message(chat_in=chat_in, db=db, current_user=current_user)


@router.get("/sessions", response_model=List[ChatSessionResponse])
def get_user_chat_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.created_at.desc()).limit(20).all()

    return sessions
