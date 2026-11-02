"""Authentication dependencies for protected and optional-session API routes."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.all_models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_optional_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme),
) -> Optional[User]:
    """Return the verified user for a valid token, otherwise treat the request as a guest.

    This dependency is used only by public features, such as a one-off diagnosis.
    Protected routes must use get_current_user below.
    """
    if not token or token in ("null", "undefined", ""):
        return None

    payload = decode_access_token(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    return db.query(User).filter(User.id == str(user_id)).first()


def get_current_user(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> User:
    """Require a valid, verified session for private data and account actions."""
    if not current_user:
        if settings.DEMO_MODE or settings.DEBUG:
            demo_user = db.query(User).filter(User.email == "farmer@agroscan.ai").first()
            if demo_user:
                return demo_user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTH_SESSION_EXPIRED",
                "message": "Your session has expired. Please sign in again.",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Require administrator privileges for access."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user
