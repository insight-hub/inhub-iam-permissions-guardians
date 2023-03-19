import logging

from app.core.settings.app import AppSettings


class DevSettings(AppSettings):
    debug = True

    log_level = logging.DEBUG
