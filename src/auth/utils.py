import bcrypt
import jwt

from src.auth.config import AUTH_CONFIG
from src.auth.schemas import JwtPayloadSchema


def encode_jwt(payload: JwtPayloadSchema) -> str:
    return jwt.encode(
        payload=payload.model_dump(),
        key=AUTH_CONFIG.JWT_SECRET_KEY,
        algorithm=AUTH_CONFIG.JWT_ALGORITHM
    )


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)
