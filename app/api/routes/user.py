from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException
from pydantic import EmailStr
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.api.dependenies.database import get_repository
from app.database.repositories.user import UserRepository
from app.models.schemas.user import UserCreated, UserCreatedRes
from app.services.user import send_join_otp
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

    baskground_task.add_task(send_join_otp, email, username)

    return UserCreatedRes(status=HTTP_201_CREATED,
                          user=UserCreated(username=db_user.username,
                                           email=db_user.email))
