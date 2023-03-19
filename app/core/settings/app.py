import logging
import sys

from enum import Enum
from typing import Any, Dict, Tuple
from pydantic import BaseSettings, PostgresDsn
from loguru import logger

from app.core.logging import InterceptHandler


class AppEnvTypes(Enum):
    prod: str = 'prod'
    dev: str = 'dev'
    test: str = 'test'


class AppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.prod
    debug: bool = False
    version: str = '0.0.1'

    db_url: PostgresDsn

    logging_level: int = logging.INFO
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
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [
                InterceptHandler(level=self.logging_level)]

        logger.configure(
            handlers=[{"sink": sys.stderr, "level": self.logging_level}])
