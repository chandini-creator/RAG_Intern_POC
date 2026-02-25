import logging
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import router

setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

app.include_router(router)

@app.on_event("startup")
def on_startup():
    logger.info("Starting app: %s (env=%s)", settings.app_name, settings.env)
