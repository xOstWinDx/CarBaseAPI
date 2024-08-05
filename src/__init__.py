from fastapi import APIRouter
from .cars import cars_router
from .auth import auth_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(cars_router)

__all__ = ["api_router"]