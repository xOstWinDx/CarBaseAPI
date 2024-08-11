from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response

from src.infrastructure.uow.user import SqlAlchemyUserUnitOfWork
from src.presentation.api.v1.auth.dependencies import authentication
from src.presentation.api.v1.auth.schemas import UserCreateSchema
from src.domain.users.service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, description="Create new user")
async def register(user_data: UserCreateSchema):
    try:
        user_service = UserService(uow=SqlAlchemyUserUnitOfWork())
        res = await user_service.register_by_email(
            email=user_data.email,
            name=user_data.name,
            password=user_data.password
        )
        return res
    except ValueError:
        raise HTTPException(status_code=409, detail="User already exists")


@router.post("/login", description="Login user")
async def login(
        response: Response,
        token: str = Depends(authentication)
):
    response.set_cookie("token", token)


@router.post("/logout", description="Logout user")
async def logout(response: Response):
    response.delete_cookie("token")
