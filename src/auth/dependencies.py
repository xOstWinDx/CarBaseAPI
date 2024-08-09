import jwt
from fastapi import Depends
from jwt import PyJWTError
from pydantic import ValidationError
from starlette.requests import Request

from src.auth.config import AUTH_CONFIG
from src.auth.service import AuthService
from src.auth.unit_of_work import SqlAlchemyUnitOfWork
from src.auth.utils import encode_jwt

from src.auth.exceptions import InvalidCredentialsAuthExc, UnknownUserAuthExc, InvalidTokenAuthExc
from src.exceptions import ForbiddenAuthExc
from src.auth.schemas import UserAuthSchema, JwtPayloadSchema
from src.auth.models import User


async def authentication(user_auth: UserAuthSchema) -> str:
    auth_service = AuthService(uow=SqlAlchemyUnitOfWork())
    user = await auth_service.get_one_or_none(email=user_auth.email)
    if not user or not user.check_password(user_auth.password):
        raise InvalidCredentialsAuthExc
    return encode_jwt(payload=JwtPayloadSchema(id=user.id, name=user.name))


def decode_jwt(request: Request) -> JwtPayloadSchema:
    cookie_token = request.cookies.get("token")
    try:
        payload = jwt.decode(
            jwt=cookie_token,  # type: ignore
            key=AUTH_CONFIG.JWT_SECRET_KEY,
            algorithms=[AUTH_CONFIG.JWT_ALGORITHM]
        )
        return JwtPayloadSchema(**payload)
    except (PyJWTError, ValidationError):
        raise InvalidTokenAuthExc


def authorization(is_admin: bool = False):
    async def inner(payload: JwtPayloadSchema = Depends(decode_jwt)) -> User:
        auth_service = AuthService(uow=SqlAlchemyUnitOfWork())
        user = await auth_service.get_one_or_none(id=payload.id)
        if not user:
            raise UnknownUserAuthExc
        if is_admin and not user.is_admin:
            raise ForbiddenAuthExc
        return user

    return inner


authorization_user = authorization(is_admin=False)
authorization_admin = authorization(is_admin=True)
