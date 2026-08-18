from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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
                "crop_detected": pred.crop_detected,
                "disease_name": pred.disease_name,
                "severity_level": pred.severity_level,
                "severity_percentage": pred.severity_percentage,
                "confidence_score": pred.confidence_score,
                "weather_risk_level": pred.weather_risk_level
            }
    elif chat_in.manual_plant:
        scan_ctx = {
            "crop_detected": chat_in.manual_plant,
            "disease_name": "General Cultivation & Care",
            "severity_level": "None"
        }

    # 4. Resolve confirmed user farm location
    location_info = chat_in.location
    if not location_info:
        # Check user profile or latest farm
        farm = db.query(Farm).filter(Farm.user_id == current_user.id).order_by(Farm.created_at.desc()).first()
        if farm and farm.village:
            location_info = {
                "village": farm.village,
                "taluka": farm.taluka,
                "district": farm.district,
                "state": farm.state,
                "pincode": farm.pincode,
                "latitude": farm.latitude,
                "longitude": farm.longitude
            }
        elif current_user.village:
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
        import asyncio
        lat = location_info.get("latitude")
        lon = location_info.get("longitude")
        city = location_info.get("district") or location_info.get("village") or "Pune"
        try:
            weather_info = WeatherRiskService.fetch_weather_sync(city=city, lat=lat, lon=lon)
        except Exception:
            pass

    # 6. Generate response via AIProviderService with full conversation history
    bot_reply_text = AIProviderService.generate_response(
        message=chat_in.message,
        conversation_history=conv_history,
        scan_context=scan_ctx,
        location_info=location_info,
        weather_info=weather_info,
        language=chat_in.language or "en",
        is_manual=bool(chat_in.manual_plant)
    )

    # 7. Save Assistant Message
    bot_msg = ChatMessage(
        session_id=session.id,
        sender="assistant",
        content=bot_reply_text
    )
    db.add(bot_msg)
    db.commit()
    db.refresh(bot_msg)

    return ChatMessageResponse(
        id=bot_msg.id,
        session_id=session.id,
        sender=bot_msg.sender,
        content=bot_msg.content,
        created_at=bot_msg.created_at
    )


@router.get("/sessions", response_model=List[ChatSessionResponse])
def get_user_chat_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.created_at.desc()).limit(20).all()

    return sessions
