from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.all_models import User, ChatSession, ChatMessage, ScanPrediction
from app.schemas.schemas import ChatMessageCreate, ChatMessageResponse, ChatSessionResponse
from app.api.deps import get_current_user
from app.services.gemini_service import GeminiAssistantService

router = APIRouter()

@router.post("", response_model=ChatMessageResponse)
def post_chat_message(
    chat_in: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = None
    if chat_in.session_id:
        session = db.query(ChatSession).filter(ChatSession.id == chat_in.session_id, ChatSession.user_id == current_user.id).first()

    if not session:
        session = ChatSession(user_id=current_user.id, title="AgroScan AI Advisory")
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save User Message
    user_msg = ChatMessage(
        session_id=session.id,
        sender="user",
        content=chat_in.message
    )
    db.add(user_msg)
    db.commit()

    # Retrieve scan context if prediction_id provided (enforce user ownership)
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
                "weather_risk_level": pred.weather_risk_level
            }
    elif chat_in.manual_plant:
        scan_ctx = {
            "crop_detected": chat_in.manual_plant,
            "disease_name": "General Cultivation & Care",
            "severity_level": "None"
        }

    # Generate response via Gemini API proxy safely
    try:
        bot_reply_text = GeminiAssistantService.generate_chat_response(
            message=chat_in.message,
            scan_context=scan_ctx,
            language=chat_in.language or "en"
        )
    except Exception as gemini_err:
        bot_reply_text = (
            "I am currently operating in offline advisory mode. "
            "For standard crop health advice, ensure good soil drainage, inspect leaves regularly for lesions, "
            "and consult your local agricultural extension service."
        )

    # Save Assistant Message
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
        sender=bot_msg.sender,
        content=bot_msg.content,
        created_at=bot_msg.created_at
    )
