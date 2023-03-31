from typing import Optional
from pydantic import BaseModel
from redis import Redis

from app.core.config import get_app_settings

# TODO


class RedisData(BaseModel):
    key: bytes | str
    value: bytes | str


settings = get_app_settings()

redis_client = Redis().from_url(url=settings.redis_url)


def set_key(data: RedisData, *, is_transaction: bool = False) -> None:
    with redis_client.pipeline(transaction=is_transaction) as pipe:
        pipe.set(data.key, data.value)
        pipe.execute()


def get_by_key(key: str) -> Optional[bytes]:
    return redis_client.get(key)


def delete_by_key(key: str) -> int:
    return redis_client.delete(key)
