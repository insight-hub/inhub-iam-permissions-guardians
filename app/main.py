from fastapi import FastAPI

from app.core.config import get_app_settings
from app.api.routes.api import api_router
from app.database.db import Base, engine

# TODO temp
Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.include_router(api_router)

    return application


app = get_application()
