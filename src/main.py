from fastapi import FastAPI

from src.logs import configure_logger
from src.auth import auth_router
from src.cars import cars_router

configure_logger()

app = FastAPI()

app.include_router(auth_router)
app.include_router(cars_router)
