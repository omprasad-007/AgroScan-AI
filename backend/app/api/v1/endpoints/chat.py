import logging
from typing import List, Any, cast, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.all_models import User, ChatSession, ChatMessage, ScanPrediction, Farm
from app.schemas.schemas import ChatMessageCreate, ChatMessageResponse, ChatSessionResponse, ChatSessionTitleUpdate
from app.api.deps import get_current_user
from app.services.ai_provider_service import AIProviderService
from app.services.agri_rag_service import AgriRAGService

logger = logging.getLogger("agroscan")

router = APIRouter()

def _generate_session_title(message: str, plant: Optional[str] = None) -> str:
    """Generate a clean, readable title for a chat session from user query."""
    clean = (message or "").strip().replace("\n", " ")
    if len(clean) > 40:
        clean = clean[:38] + "..."
    if plant and plant.lower() not in clean.lower():
        return f"{plant}: {clean}"
    return clean or "Agricultural Advisory"

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
        title = _generate_session_title(chat_in.message, chat_in.manual_plant)
        session = ChatSession(user_id=current_user.id, title=title)
        db.add(session)
        db.commit()
        db.refresh(session)
    elif session.title in ["AgroScan AI Advisory", "Agronomy Chat", "New Advisory"]:
        # Update placeholder title with first substantive query
        session.title = _generate_session_title(chat_in.message, chat_in.manual_plant)
        db.commit()

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
        try:
            # Check user profile or latest farm
            farm = db.query(Farm).filter(Farm.user_id == current_user.id).order_by(Farm.created_at.desc()).first()
            if farm and (getattr(farm, "village", None) or getattr(farm, "district", None) or getattr(farm, "latitude", None)):
                location_info = {
                    "village": getattr(farm, "village", None),
                    "taluka": getattr(farm, "taluka", None),
                    "district": getattr(farm, "district", None),
                    "state": getattr(farm, "state", None),
                    "pincode": getattr(farm, "pincode", None),
                    "latitude": getattr(farm, "latitude", None),
                    "longitude": getattr(farm, "longitude", None)
                }
            elif getattr(current_user, "village", None) or getattr(current_user, "district", None):
                location_info = {
                    "village": getattr(current_user, "village", None),
                    "taluka": getattr(current_user, "taluka", None),
                    "district": getattr(current_user, "district", None),
                    "state": getattr(current_user, "state", None),
                    "pincode": getattr(current_user, "pincode", None),
                    "latitude": getattr(current_user, "latitude", None),
                    "longitude": getattr(current_user, "longitude", None)
                }
        except Exception as e:
            logger.warning(f"Failed to fetch farm/user location in chat: {e}")

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
        research_mode=chat_in.research_mode or "auto",
        user_id=str(current_user.id)
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
    """Retrieve all past chat sessions for the logged-in user with summary stats."""
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.created_at.desc()).limit(50).all()

    result = []
    for s in sessions:
        msgs = db.query(ChatMessage).filter(
            ChatMessage.session_id == s.id
        ).order_by(ChatMessage.created_at.asc()).all()
        last_msg = msgs[-1].content if msgs else None
        if last_msg and len(last_msg) > 60:
            last_msg = last_msg[:58] + "..."
        result.append(ChatSessionResponse(
            id=str(s.id),
            title=str(s.title or "AgroScan Advisory"),
            created_at=cast(Any, s.created_at),
            message_count=len(msgs),
            last_message=last_msg,
            messages=[
                ChatMessageResponse(
                    id=str(m.id),
                    session_id=str(m.session_id),
                    sender=str(m.sender),
                    content=str(m.content),
                    created_at=cast(Any, m.created_at)
                ) for m in msgs
            ]
        ))

    return result


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
def get_chat_session_by_id(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a specific past chat session with its full historical conversation transcript."""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found or does not belong to the user"
        )

    msgs = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.created_at.asc()).all()

    last_msg = msgs[-1].content if msgs else None
    return ChatSessionResponse(
        id=str(session.id),
        title=str(session.title or "AgroScan Advisory"),
        created_at=cast(Any, session.created_at),
        message_count=len(msgs),
        last_message=last_msg,
        messages=[
            ChatMessageResponse(
                id=str(m.id),
                session_id=str(m.session_id),
                sender=str(m.sender),
                content=str(m.content),
                created_at=cast(Any, m.created_at)
            ) for m in msgs
        ]
    )


@router.delete("/sessions/{session_id}")
def delete_chat_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a past chat session and all associated messages."""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

    db.delete(session)
    db.commit()

    return {"status": "success", "message": "Chat session deleted", "id": session_id}


@router.patch("/sessions/{session_id}", response_model=ChatSessionResponse)
def update_chat_session_title(
    session_id: str,
    title_in: ChatSessionTitleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update title for a specific chat session."""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

    session.title = title_in.title.strip()[:60]
    db.commit()
    db.refresh(session)

    msgs = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.created_at.asc()).all()

    return ChatSessionResponse(
        id=str(session.id),
        title=str(session.title),
        created_at=cast(Any, session.created_at),
        message_count=len(msgs),
        messages=[
            ChatMessageResponse(
                id=str(m.id),
                session_id=str(m.session_id),
                sender=str(m.sender),
                content=str(m.content),
                created_at=cast(Any, m.created_at)
            ) for m in msgs
        ]
    )
