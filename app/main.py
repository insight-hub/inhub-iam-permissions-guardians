from fastapi import FastAPI

from app.core.config import get_app_settings


def get_application() -> FastAPI:
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)

    return application


app = get_application()
