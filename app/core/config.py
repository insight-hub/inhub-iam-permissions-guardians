from functools import lru_cache
from typing import Dict, Type

from app.core.settings.app import AppEnvTypes, AppSettings
from app.core.settings.development import DevSettings


class ProdSettings(AppSettings):
    pass


class TestSettings(AppSettings):
    pass


envs: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevSettings,
    AppEnvTypes.prod: ProdSettings,
    AppEnvTypes.test: TestSettings
}


@lru_cache
def get_app_settings():
    env = AppSettings().app_env
    config = envs[env]
    return config()
