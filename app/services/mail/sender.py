from pathlib import Path
from typing import Any, Dict, List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi_mail.connection import ConnectionErrors
from loguru import logger
from pydantic import BaseModel, EmailStr

from app.core.config import get_app_settings

settings = get_app_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    # TODO different departments
    MAIL_FROM_NAME=f'InsightHub Security',
    MAIL_PORT=465,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates'
)


class EmailSchema(BaseModel):
    subject: str
    to: List[EmailStr]


class HTMLEmail(EmailSchema):
    body: Dict[str, Any]


async def send_html_mail(email: HTMLEmail, *, template_name: str):
    message = MessageSchema(
        subject=email.subject,
        recipients=email.to,
        template_body=email.body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    try:
        await fm.send_message(message, template_name)
        logger.info(
            f'Mail has been sended to {email.to}')

    except ConnectionErrors as e:
        logger.error(e)
