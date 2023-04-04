import json
from datetime import datetime, timedelta
from fastapi import HTTPException

from pydantic import BaseModel
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.services import redis
from app.services.redis import RedisData
from app.utils.otp import get_random_pass

OTP_EXPIRED_SECONDS = 60 * 10


class UserOTP(BaseModel):
    timestamp: float
    pwd: str
    id: str
    is_used: bool


def set_join_otp(id: str, otp: str):
    timestamp = datetime.now().timestamp()
    user_otp = UserOTP(timestamp=timestamp, pwd=otp, id=id, is_used=False)
    redis_data = RedisData(key=id, value=json.dumps(user_otp.dict()))
    redis.set_key(data=redis_data)


def check_otp(id: str, otp: str):
    # TODO refactor
    user_otp = UserOTP(**json.loads(redis.get_by_key(id)))

    if not user_otp:
        raise Exception("User does not exist")

    timestamp = datetime.now().timestamp()
    time_diff = timedelta(
        seconds=timestamp - user_otp.timestamp)

    pwd_expired = time_diff >= timedelta(seconds=OTP_EXPIRED_SECONDS)

    if pwd_expired:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                'status': HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'There is error on check one time password',
                'details': {
                    'otp': 'One time password expired'
                }
            })

    if user_otp.is_used:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                'status': HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'There is error on check one time password',
                'details': {
                    'otp': 'One time password is already used'
                }
            })

    if user_otp.pwd != otp:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                'status': HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'There is error on check one time password',
                'details': {
                    'otp': 'One time password is not mutch with sended'
                }
            })

    return True


def update_otp(id: str):
    user_otp = UserOTP(**json.loads(redis.get_by_key(id)))
    if not user_otp:
        raise Exception("User does not exist")

    user_otp.is_used = False
    user_otp.pwd = get_random_pass()
    user_otp.timestamp = datetime.now().timestamp()

    redis.set_key(RedisData(key=id, value=json.dumps(user_otp.dict())))
