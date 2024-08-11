import jwt

from src.domain.users import UserService
from src.infrastructure.uow.user import SqlAlchemyUserUnitOfWork

from src.presentation.api.v1.auth.exceptions import InvalidCredentialsAuthExc

from src.presentation.api.v1.auth.config import AUTH_CONFIG
from src.presentation.api.v1.auth.schemas import JwtPayloadSchema, UserAuthSchema


async def authentication(user_auth: UserAuthSchema) -> str:
    user_service = UserService(uow=SqlAlchemyUserUnitOfWork())
    user = await user_service.get_one_or_none(email=user_auth.email)
    if not user or not user.check_password(user_auth.password):
        raise InvalidCredentialsAuthExc
    return encode_jwt(payload=JwtPayloadSchema(id=user.id, name=user.name))


def encode_jwt(payload: JwtPayloadSchema) -> str:
    return jwt.encode(
        payload=payload.model_dump(),
        key=AUTH_CONFIG.JWT_SECRET_KEY,
        algorithm=AUTH_CONFIG.JWT_ALGORITHM
    )
