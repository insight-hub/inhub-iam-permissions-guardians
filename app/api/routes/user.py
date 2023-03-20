from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.api.dependenies.database import get_repository
from app.database.repositories.user import UserRepository
from app.models.schemas.user import UserCreated, UserCreatedRes, UserJoin
from app.services.user import send_join_otp
from app.utils.auth import check_email_taken, check_username_taken

router = APIRouter()


@router.post('/join', response_model=UserCreatedRes)
async def create_user(baskground_task: BackgroundTasks,
                      user: UserJoin = Body(),
                      user_repository: UserRepository = Depends(get_repository(UserRepository))):

    if check_email_taken(email=user.email, repo=user_repository):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Email already taken')

    if check_username_taken(username=user.username, repo=user_repository):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Username already taken')

    db_user = user_repository.create_new_user(user=user)
    user_created = UserCreated(email=db_user.email, username=db_user.username)
    baskground_task.add_task(send_join_otp, user_created)

    return UserCreatedRes(status=HTTP_201_CREATED,
                          user=user_created)
