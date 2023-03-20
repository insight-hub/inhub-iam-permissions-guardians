from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependenies.database import get_repository
from app.database.repositories.user import UserRepository
from app.models.schemas.user import UserJoin
from app.utils.auth import check_email_taken, check_username_taken

router = APIRouter()


@router.post('/join')
async def create_user(user: UserJoin = Body(), user_repository: UserRepository = Depends(get_repository(UserRepository))):
    if check_email_taken(email=user.email, repo=user_repository):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Email already taken')

    if check_username_taken(username=user.username, repo=user_repository):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Username already taken')
