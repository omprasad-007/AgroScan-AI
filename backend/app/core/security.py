import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from app.core.config import settings

def get_password_hash(password: str) -> str:
    """Generate secure salted PBKDF2-SHA256 password hash (100,000 iterations)."""
    salt = secrets.token_bytes(16)
    salt_hex = salt.hex()
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100_000
    )
    return f"pbkdf2_sha256${salt_hex}${key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against salted PBKDF2 hash, with fallback support for legacy sha256 hashes."""
    if not hashed_password or not plain_password:
        return False

    # Check for salted PBKDF2 format
    if hashed_password.startswith("pbkdf2_sha256$"):
        try:
            parts = hashed_password.split("$")
            if len(parts) != 3:
                return False
            _, salt_hex, expected_hash = parts
            salt = bytes.fromhex(salt_hex)
            key = hashlib.pbkdf2_hmac(
                'sha256',
                plain_password.encode('utf-8'),
                salt,
                100_000
            )
            return hmac.compare_digest(key.hex(), expected_hash)
        except Exception:
            return False

    # Fallback legacy hash format (for pre-existing seed data)
    if hashed_password.startswith("sha256$"):
        legacy_salt = settings.SECRET_KEY.encode('utf-8')
        legacy_hashed = f"sha256${hmac.new(legacy_salt, plain_password.encode('utf-8'), hashlib.sha256).hexdigest()}"
        return hmac.compare_digest(legacy_hashed, hashed_password)

    return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

