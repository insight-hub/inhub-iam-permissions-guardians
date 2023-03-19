import logging

from app.core.settings.app import AppSettings


class DevSettings(AppSettings):
    debug = True

    logging_level: int = logging.DEBUG
