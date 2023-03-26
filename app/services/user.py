from pydantic import EmailStr

from app.services.otp import set_join_otp
from app.services.mail.sender import HTMLEmail, send_html_mail
from app.utils.otp import get_random_pass


async def send_join_otp(email: EmailStr, username: str):
    one_time_password = get_random_pass()

    set_join_otp(username, one_time_password)

    mail_body = {'user': username, 'one_time_pass': one_time_password}
    mail = HTMLEmail(subject="Welcome to Insight Hub",
                     to=[email], body=mail_body)

    return await send_html_mail(email=mail,
                                template_name='one_time_password.html')
