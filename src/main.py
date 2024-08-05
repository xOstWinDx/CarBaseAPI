from fastapi import FastAPI

from src import api_router
from src.logs import configure_logger

configure_logger()

app = FastAPI(title="Car service", version="1.0.0")

app.include_router(api_router)
