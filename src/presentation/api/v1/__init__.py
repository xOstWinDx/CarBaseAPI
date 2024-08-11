from fastapi import APIRouter
from .auth.router import router as auth_router
from .cars.router import router as cars_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(cars_router)
