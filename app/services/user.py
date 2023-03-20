import json
from datetime import datetime
from pydantic import EmailStr

from app.models.schemas.user import UserJoin
from app.services import redis
from app.services.redis import RedisData
from app.services.mail.sender import HTMLEmail, send_html_mail
from app.utils.otp import get_random_pass


async def send_join_otp(user: UserJoin):
    one_time_password = get_random_pass()

    _set_join_otp(user, otp=one_time_password)

    user_email = EmailStr(user.email)
    mail_body = {'username': user.username, 'one_time_pass': get_random_pass()}
    mail = HTMLEmail(subject="Welcome to Insight Hub",
                     to=[user_email], body=mail_body)

    return await send_html_mail(email=mail,
                                template_name='one_time_password.html')


def _set_join_otp(user: UserJoin, *, otp: str):
    timestamp = datetime.now().timestamp()
    user_data = {'timestamp': timestamp,
                 'pass': otp, **user.dict()}
    redis_data = RedisData(key=user.username, value=json.dumps(user_data))
    redis.set_key(data=redis_data)
