from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException
from pydantic import EmailStr
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.api.dependenies.database import get_repository
from app.database.repositories.user import UserRepository
from app.models.schemas.user import UserCreated, UserCreatedRes, UserInResponse, UserInUpdate
from app.services import user as userService, otp as otpService
from app.utils.auth import check_email_taken, check_username_taken

router = APIRouter()


@router.post('/join', response_model=UserCreatedRes)
async def create_user(baskground_task: BackgroundTasks,
                      username: str = Form(),
                      email: EmailStr = Form(),
                      password: str = Form(),
                      user_repository: UserRepository = Depends(
                          get_repository(UserRepository))):

    if check_email_taken(user_repository, email):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Email already taken')

    if check_username_taken(user_repository, username):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Username already taken')

    db_user = user_repository.create_new_user(
        username=username, email=email, password=password)

    baskground_task.add_task(userService.send_join_otp, email, username)

    return UserCreatedRes(status=HTTP_201_CREATED,
                          user=UserCreated(id=db_user.uuid,
                                           username=db_user.username,
                                           email=db_user.email))


@router.post('/otp')
async def check_one_time_password(username: str = Form(),
                                  otp: str = Form(),
                                  user_repository: UserRepository = Depends(
                                      get_repository(UserRepository))):
    try:
        if not otpService.check_otp(username, otp):
            return

        db_user = user_repository.update_user(
            user=UserInUpdate(username=username, is_mail_confirmed=True))

        return {'user': db_user}

    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail=str(e))


@router.put('/otp')
async def update_one_time_password(username: str = Form()):
    try:
        otpService.update_otp(username)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
