import logging

from enum import Enum
from typing import Any, Dict, Tuple
from pydantic import BaseSettings, PostgresDsn


class AppEnvTypes(Enum):
    prod: str = 'prod'
    dev: str = 'dev'
    test: str = 'test'


class AppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.prod
    debug: bool = False
    version: str = '0.0.1'

    db_url: PostgresDsn

    log_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_arguments = True
        env_file = '.env'

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "version": self.version
        }

    def configure_logging(self):
        logging.getLogger().handlers =
