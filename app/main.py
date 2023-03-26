from fastapi import FastAPI
from redis import RedisError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_app_settings
from app.api.routes.api import api_router
from app.services.errors import redis_error_handler


def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        # TODO temporary allow all origins
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(RedisError, redis_error_handler)

    application.include_router(api_router)

    return application


app = get_application()
