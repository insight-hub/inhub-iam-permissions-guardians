import httpx
from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException
from pydantic import EmailStr
from sqlalchemy import except_
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
from app.api.dependenies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.database.errors import EntityDoesNotExist
from app.database.repositories.user import UserRepository
from app.models.schemas.user import (
    UserCreated,
    UserCreatedRes,
    UserInResponse,
    UserWithToken
)
from app.services import jwt, security, user
from app.utils.auth import check_email_taken, check_username_taken


router = APIRouter(tags=['Authentification'])


@router.post('/login', response_model=UserInResponse, name="auth:login")
async def login(
    username: str = Form(min_length=4, max_length=30),
    password: str = Form(max_length=100),
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

    return UserInResponse(
        status=HTTP_200_OK,
        user=UserWithToken(
            id=user.uuid.hex,
            username=user.username,
            email=user.email,
            is_mail_confirmed=user.is_mail_confirmed,
            token=token
        ))


@router.post('/join', response_model=UserCreatedRes, name="auth:join")
async def create_user(
    baskground_task: BackgroundTasks,
    username: str = Form(),
    email: EmailStr = Form(),
    password: str = Form(),
    user_repo: UserRepository = Depends(get_repository(UserRepository))
):

    if check_email_taken(user_repo, email):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Email already taken')

    if check_username_taken(user_repo, username):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Username already taken')

    db_user = user_repo.create_new_user(
        username=username, email=email, password=password)

    baskground_task.add_task(user.send_join_otp, email, username)

    return UserCreatedRes(
        status=HTTP_201_CREATED,
        user=UserCreated(
            id=db_user.uuid,
            username=db_user.username,
            email=db_user.email
        ))


@router.post('/recaptcha')
async def human_verify(
        token: str = Form(),
        settings: AppSettings = Depends(get_app_settings)):

    params = {'secret': settings.recaptcha_secret, 'response': token}
    try:
        result = httpx.post(
            'https://www.google.com/recaptcha/api/siteverify',
            params=params
        )

    except HTTPException:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="GO AWAY ROBOT"
        )

    return {'status': result.status_code, 'is_human': True}
