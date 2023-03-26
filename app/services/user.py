import json
from datetime import datetime
from pydantic import EmailStr

from app.services import redis
from app.services.redis import RedisData
from app.services.mail.sender import HTMLEmail, send_html_mail
from app.utils.otp import get_random_pass


async def send_join_otp(email: EmailStr, username: str):
    one_time_password = get_random_pass()

    _set_join_otp(username, one_time_password)

    mail_body = {'user': username, 'one_time_pass': one_time_password}
    mail = HTMLEmail(subject="Welcome to Insight Hub",
                     to=[email], body=mail_body)

    return await send_html_mail(email=mail,
                                template_name='one_time_password.html')


def _set_join_otp(id: str, otp: str):
    timestamp = datetime.now().timestamp()
    user_otp = {'timestamp': timestamp,
                'pass': otp,
                'id': id,
                'is_used': False}
    redis_data = RedisData(key=id, value=json.dumps(user_otp))
    redis.set_key(data=redis_data)
