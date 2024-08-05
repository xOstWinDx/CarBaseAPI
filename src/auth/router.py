from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from src.auth.dependencies import get_async_session
from src.auth.dependencies import authentication
from src.auth.repository import AuthPostgresRepository
from src.auth.schemas import UserCreateSchema
from src.auth.service import AuthService

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=201, description="Create new user")
async def register(
        user_data: UserCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        auth_service = AuthService(AuthPostgresRepository(session=session))
        res = await auth_service.register_by_email(
            email=user_data.email,
            name=user_data.name,
            password=user_data.password
        )
        await session.commit()
        return res
    except ValueError:
        raise HTTPException(status_code=409, detail="User already exists")
    except Exception as e:
        await session.rollback()
        raise


@router.post("/login", description="Login user")
async def login(
        response: Response,
        token: str = Depends(authentication)
):
    response.set_cookie("token", token)


@router.post("/logout", description="Logout user")
async def logout(response: Response):
    response.delete_cookie("token")
