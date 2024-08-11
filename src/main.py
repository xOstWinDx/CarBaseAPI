import logging

from fastapi import FastAPI

from src.config import CONFIG
from src.presentation.api import api_router

logging.basicConfig(
    level=CONFIG.LOG_LEVEL,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="[%(asctime)s.%(msecs)03d] %(module)12s:%(lineno)3d %(levelname)-7s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

app = FastAPI(title="Car service", version="1.0.0")

app.include_router(api_router)
