import jwt
from fastapi import Depends
from jwt import PyJWTError
from pydantic import ValidationError
from starlette.requests import Request

from src.domain.users import User
from src.domain.users.service import UserService
from src.infrastructure.uow.user import SqlAlchemyUserUnitOfWork
from src.presentation.api.v1.auth.config import AUTH_CONFIG
from src.presentation.api.v1.auth.exceptions import UnknownUserAuthExc, InvalidTokenAuthExc
from src.presentation.api.v1.auth.schemas import JwtPayloadSchema
from src.presentation.api.v1.exceptions import ForbiddenAuthExc


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
        user_service = UserService(uow=SqlAlchemyUserUnitOfWork())
        user = await user_service.get_one_or_none(id=payload.id)
        if not user:
            raise UnknownUserAuthExc
        if is_admin and not user.is_admin:
            raise ForbiddenAuthExc
        return user

    return inner


authorization_user = authorization(is_admin=False)
authorization_admin = authorization(is_admin=True)
