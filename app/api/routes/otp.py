from fastapi import APIRouter, Depends, Form, HTTPException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from app.api.dependenies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.database.repositories.user import UserRepository
from app.models.domain.user import User
from app.models.schemas.user import (
    UserInResponse,
    UserInUpdate,
    UserWithToken
)
from app.services.otp import check_otp, update_otp
from app.services.jwt import create_token_for_user

router = APIRouter(tags=["One time password"])


@ router.post('', response_model=UserInResponse, name="otp:check")
async def check_one_time_password(
        username: str = Form(max_length=30),
        otp: str = Form(max_length=10),
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        settings: AppSettings = Depends(get_app_settings)
):
    try:
        check_otp(username, otp)
    try:
        db_user = user_repo.update_user(
            user=UserInUpdate(username=username, is_mail_confirmed=True))

        user = User(
            id=db_user.uuid.hex,
            username=db_user.username,
            email=db_user.email,
            is_mail_confirmed=db_user.is_mail_confirmed
        )

        token = create_token_for_user(
            user=user,
            secret_key=settings.secret_key.get_secret_value()
        )

        return UserInResponse(
            status=HTTP_200_OK,
            user=UserWithToken(
                id=user.id,
                username=user.username,
                email=user.email,
                is_mail_confirmed=user.is_mail_confirmed,
                token=token
            ))


@ router.put('', name='otp:update')
async def update_one_time_password(
        username: str = Form(min_length=4, max_length=30)
):
    # TODO send new otp email
    update_otp(username)
