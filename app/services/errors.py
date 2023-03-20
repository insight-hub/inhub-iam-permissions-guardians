from fastapi.responses import JSONResponse
from loguru import logger
from redis import RedisError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


async def redis_error_handler(_, exc: RedisError):
    logger.error(exc)
    return JSONResponse({'status': HTTP_500_INTERNAL_SERVER_ERROR,
                         'detail': 'Texнические шоколадки'})
