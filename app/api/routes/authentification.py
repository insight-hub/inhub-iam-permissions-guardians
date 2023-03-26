from fastapi import APIRouter, Depends, Form, HTTPException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from app.api.dependenies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.database.errors import EntityDoesNotExist
from app.database.repositories.user import UserRepository
from app.models.domain.user import UserInDB
from app.models.schemas.user import UserInResponse, UserWithToken
from app.services import jwt, security


router = APIRouter(tags=['authentification'])


@router.post('/login', response_model=UserInResponse, name="auth:login")
async def login(
        username: str = Form(),
        password: str = Form(),
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        settings: AppSettings = Depends(get_app_settings)
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail='Incorrect username or password'
    )

    try:
        user = user_repo.get_by_username(username=username)

    except EntityDoesNotExist as excistence_error:
        raise wrong_login_error from excistence_error

    if not security.varify_password(password, user.hashed_password):
        raise wrong_login_error

    token = jwt.create_token_for_user(
        user, settings.secret_key.get_secret_value())

    return UserInResponse(status=HTTP_200_OK,
                          user=UserWithToken(
                              uuid=user.uuid.hex,
                              username=user.username,
                              email=user.email,
                              is_mail_confirmed=user.is_mail_confirmed,
                              token=token
                          ))
